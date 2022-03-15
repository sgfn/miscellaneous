def parser():
    template = input()
    data = {}
    pairs_data = {}
    _ = input()
    a = input()

    while a != '':
        t = a.split()
        data.setdefault(t[0][0], {})
        data[t[0][0]][t[0][1]] = t[2]
        pairs_data.setdefault(t[0], {})
        pairs_data[t[0]]['cnt'] = 0
        pairs_data[t[0]]['upd_cnt'] = 0
        pairs_data[t[0]]['into'] = [t[0][0]+t[2], t[2]+t[0][1]]
        a = input()

    for key in data:
        data[key]['cnt'] = 0

    for i in range(len(template)-1):
        pairs_data[template[i]+template[i+1]]['cnt'] += 1
    
    return template, data, pairs_data


def d14p1(pol, data):
    for el in pol:
        data[el]['cnt'] += 1

    for st in range(10):
        new_pol = ''
        # print(f'st={st} pol={pol}')
        for i in range(len(pol)-1):
            new_pol += pol[i]
            addition = data[pol[i]][pol[i+1]]
            new_pol += addition
            data[addition]['cnt'] += 1
        new_pol += pol[-1]
        pol = new_pol
    
    mx = -1
    mn = 10**100
    # print(len(pol))
    for key in data:
        mx = max(mx, data[key]['cnt'])
        mn = min(mn, data[key]['cnt'])
    print(mx-mn)


def d14p2(pol, data, pairs_data):
    for el in pol:
        data[el]['cnt'] += 1

    for st in range(40):
        for pair in pairs_data:
            tl = pairs_data[pair]['into']
            for npair in tl:
                pairs_data[npair]['upd_cnt'] += pairs_data[pair]['cnt']
            data[tl[0][1]]['cnt'] += pairs_data[pair]['cnt']
            pairs_data[pair]['cnt'] = 0
        
        for pair in pairs_data:
            pairs_data[pair]['cnt'] = pairs_data[pair]['upd_cnt']
            pairs_data[pair]['upd_cnt'] = 0
    
    mx = -1
    mn = 10**100
    # print(len(pol))
    for key in data:
        mx = max(mx, data[key]['cnt'])
        mn = min(mn, data[key]['cnt'])
    print(mx-mn)    


if __name__ == '__main__':
    pol, data, pairs_data = parser()
    # d14p1(pol, data)
    d14p2(pol, data, pairs_data)
