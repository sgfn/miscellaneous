import sys
from math import pi, tan, atan
from random import randint
from time import sleep

import pygame as pgm

class Graph:
    def __init__(self) -> None:
        pgm.init()
        self.screen = pgm.display.set_mode( (1600, 900) )
        pgm.display.set_caption('draw_graph')

        self.vertices = []
        self.edges = []
        self.picked_up = None
    
    def load_g(self, G, s) -> None:
        n = 0
        for fr, to, _ in G:     n = max( n, max(fr, to) )
        n += 1
        for city_num in range(n):
            curr_left, curr_top = randint(10, 1540), randint(10, 840)
            special = city_num == s
            self.vertices.append( CitySprite(self, city_num, curr_left, curr_top, special) )

        for road_num, (fr, to, wt) in enumerate(G):
            self.edges.append( RoadSprite(self, self.vertices[fr], self.vertices[to], wt) )
        
        # for city_num, city_obj in enumerate(self.vertices):
        #     for rd in G[city_num][0]:
        #         if city_num < rd:
        #             city_obj.create_road( self.vertices[rd], True,  city_num in G[rd][0] )
        #     for rd in G[city_num][1]:
        #         if city_num < rd:
        #             city_obj.create_road( self.vertices[rd], False, city_num in G[rd][0] )

    def run_vis(self):
        while True:
            self._check_events()
            self._update_screen()
            sleep(0.03)

    def _check_events(self):
        for event in pgm.event.get():
            if   event.type == pgm.QUIT:      sys.exit()
            elif event.type == pgm.MOUSEBUTTONDOWN:
                self._check_mbd_events(event, pgm.mouse.get_pos())
            elif event.type == pgm.MOUSEBUTTONUP:
                self._check_mbu_events(event)

    def _check_mbd_events(self, event, mouse_pos):
        if self.picked_up is not None:
            self.picked_up = None
            return None
        for c_num, city_spr in enumerate(self.vertices):
            if city_spr.rect.collidepoint(mouse_pos):
                self.picked_up = c_num
                return None
        self.picked_up = None

    def _check_mbu_events(self, event):
        pass
        
    def _update_screen(self):
        self.screen.fill('#CCCCCC')
        if self.picked_up is not None:
            left, top = pgm.mouse.get_pos()
            self.vertices[self.picked_up].update_pos(left, top)

        for rd in self.edges:         rd.blitme()
        for ct in self.vertices:      ct.blitme()
        pgm.display.flip()


class Sprite:
    def __init__(self, graph) -> None:
        self.screen = graph.screen
        self.screen_rect = self.screen.get_rect()


class CitySprite(Sprite):
    def __init__(self, graph, number, left=0, top=0, special=False) -> None:
        super().__init__(graph)

        self.graph = graph
        self.screen = graph.screen
        self.colour = '#DDDD00' if special else '#009999'
        self.number = number
        self.left, self.top = left, top
        self.rect = pgm.Rect(left, top, 50, 50)
        self.text = TextSprite(graph, str(number),
                             '#333333' if special else '#FFFFFF', left+5, top+2)
    
    def blitme(self):
        pgm.draw.rect(self.screen, self.colour, self.rect)
        self.text.blitme()

    # def create_road(self, city_to, from_north, to_north):
    #     self.roads.append( RoadSprite(self.graph, self, city_to, from_north, to_north) )

    def update_pos(self, left, top):
        self.left, self.top = left, top
        self.rect = pgm.Rect(left, top, 50, 50)
        self.text.rect = pgm.Rect(left+5, top+2, 0, 0)
        # for road in self.graph.edges:
        #     if road.city1 == self or road.city2 == self:    road.bezier_points = None


class RoadSprite(Sprite):
    def __init__(self, graph, city_from, city_to, weight) -> None:
        super().__init__(graph)
        
        self.screen = graph.screen
        
        self.city_from, self.city_to = city_from, city_to
        self.weight = weight

        self.text = TextSprite(graph, str(weight), '#000000', 5, 2, font='Arial')

        # self.bezier_points = None
        self.colour = (randint(0, 200), randint(0, 200), randint(100, 200))

    def cubic_bezier(self, p_0, p_1, p_2, p_3, iters=10, pcs=5):
        def bsearch(x):
            N = len(cumul_dist_LUT)
            i = N//2
            step = N//4
            while True:
                if i+1 < N and cumul_dist_LUT[i] <= x and cumul_dist_LUT[i+1] > x:
                    return i if x-cumul_dist_LUT[i] < cumul_dist_LUT[i+1]-x else i+1
                elif cumul_dist_LUT[i] > x:   i -= step
                elif cumul_dist_LUT[i] < x:   i += step
                else:   print('weird')
                step = step//2 if step > 1 else step
        P = lambda t, c0, c1, c2, c3: (-t**3+3*t**2-3*t+1)*c0 + (3*t**3-6*t**2+3*t)*c1 + (-3*t**3+3*t**2)*c2 + (t**3)*c3
        dist = lambda p1, p2: ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
        cumul_dist_LUT = [0]
        prev_point, prev_dist = p_0, 0
        for i in range(1, iters+1):
            point = (P(i/iters, p_0[0], p_1[0], p_2[0], p_3[0]), P(i/iters, p_0[1], p_1[1], p_2[1], p_3[1]))
            # print(f't={i/iters} point={point}')
            cumul_dist_LUT.append(dist(point, prev_point) + prev_dist)
            prev_point, prev_dist = point, cumul_dist_LUT[-1]
        # print(cumul_dist_LUT)

        draw_points = [p_0]
        d = prev_dist/(pcs+1)
        for i in range(pcs):
            t = bsearch(d*(i+1))/iters
            point = (P(t, p_0[0], p_1[0], p_2[0], p_3[0]), P(t, p_0[1], p_1[1], p_2[1], p_3[1]))
            # print(t, point)
            draw_points.append(point)
        draw_points.append(p_3)
        return draw_points

    def blitme(self):
        line_data = [(self.city_from.left+25, self.city_from.top+25),
                     (self.city_to.left+25, self.city_to.top+25)]
        pgm.draw.lines( self.screen, self.colour, False, line_data, 3 )
        avg = lambda x, y: (x+y)//2
        slope = lambda l: (l[1][1]-l[1][0]) / (l[0][1]-l[0][0]) if l[0][1] != l[0][0] else (float)('inf')
        alpha = atan(slope(line_data))
        dir_1, dir_2 = tan(alpha+(pi/4)), tan(alpha-(pi/4))
        c_left, c_top = avg(self.city_from.left+25, self.city_to.left+25), avg(self.city_from.top+25, self.city_to.top+25)
        line_1 = [(c_left, c_top), (c_left+5*dir_1, c_top+5*dir_1)]
        line_2 = [(c_left, c_top), (c_left+5*dir_1, c_top+5*dir_2)]
        pgm.draw.lines( self.screen, self.colour, False, line_1, 3 )
        pgm.draw.lines( self.screen, self.colour, False, line_2, 3 )
        self.text.rect = pgm.Rect(c_left, c_top-20, 0, 0)
        self.text.blitme()
        # if self.bezier_points is None:
        #     p_0 = (self.city1.left+25, self.city1.top+25)
        #     p_1 = (randint(0, 1599), randint(0, 899))
        #     p_2 = (900, 470)
        #     p_3 = (self.city2.left+25, self.city2.top+25)
        #     self.bezier_points = self.cubic_bezier( p_0, p_1, p_2, p_3, iters=100, pcs=100 )
        # pgm.draw.lines( self.screen, self.colour, False, self.bezier_points, 3 )


class TextSprite(Sprite):
    def __init__(self, graph, string, clr, left, top, font='Arial Black') -> None:
        super().__init__(graph)

        self.screen = graph.screen
        self.rect = pgm.Rect(left, top, 0, 0)
        self.image = pgm.font.SysFont(font, 16).render(string, True, clr)

    def blitme(self):
        self.screen.blit(self.image, self.rect)


# def describe_graph( G ):
#     for ct, (con_n, con_s) in enumerate( G ):
#         print(f'city {ct}:\n\tnorth gate:')
#         for con_to in con_n:
#             print(f'\t\t-> {con_to} ({"N" if ct in G[con_to][0] else "S"})')

#         print(f'\tsouth gate:')
#         for con_to in con_s:
#             print(f'\t\t-> {con_to} ({"N" if ct in G[con_to][0] else "S"})')
#         print()

# def cubic_bezier(p_0, p_1, p_2, p_3, iters=10, pcs=5):
#         def bsearch(x):
#             N = len(cumul_dist_LUT)
#             i = N//2
#             step = N//4
#             while True:
#                 if i+1 < N and cumul_dist_LUT[i] <= x and cumul_dist_LUT[i+1] > x:
#                     return i if x-cumul_dist_LUT[i] < cumul_dist_LUT[i+1]-x else i+1
#                 elif cumul_dist_LUT[i] > x:   i -= step
#                 elif cumul_dist_LUT[i] < x:   i += step
#                 else:   print('weird')
#                 step = step//2 if step > 1 else step
#         P = lambda t, c0, c1, c2, c3: (-t**3+3*t**2-3*t+1)*c0 + (3*t**3-6*t**2+3*t)*c1 + (-3*t**3+3*t**2)*c2 + (t**3)*c3
#         dist = lambda p1, p2: ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
#         cumul_dist_LUT = [0]
#         prev_point, prev_dist = p_0, 0
#         for i in range(1, iters+1):
#             point = (P(i/iters, p_0[0], p_1[0], p_2[0], p_3[0]), P(i/iters, p_0[1], p_1[1], p_2[1], p_3[1]))
#             # print(f't={i/iters} point={point}')
#             cumul_dist_LUT.append(dist(point, prev_point) + prev_dist)
#             prev_point, prev_dist = point, cumul_dist_LUT[-1]
#         # print(cumul_dist_LUT)

#         draw_points = [p_0]
#         d = prev_dist/(pcs+1)
#         for i in range(pcs):
#             t = bsearch(d*(i+1))/iters
#             point = (P(t, p_0[0], p_1[0], p_2[0], p_3[0]), P(t, p_0[1], p_1[1], p_2[1], p_3[1]))
#             # print(t, point)
#             draw_points.append(point)
#         draw_points.append(p_3)
#         return draw_points
        

if __name__ == '__main__':
    G = [(0,1,7),(0,3,3),(1,3,4),(1,4,6),(2,0,9),(2,3,7),(2,5,9),
         (3,4,9),(3,6,2),(5,3,3),(5,6,4),(6,4,8)]
    s = 2
    graphvis = Graph()
    graphvis.load_g(G, s)
    graphvis.run_vis()
