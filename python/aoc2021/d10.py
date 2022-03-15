class StackNode():
    def __init__(self, val=None):
        self.val = val
        self.prev = None


class ListNode():
    def __init__(self, val=None):
        self.val = val
        self.next = None


def checks(line):
    score = 0
    brackets_data = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>',
        ')': {
            'left': '(',
            'c_points': 3,
            'i_points': 1
        },
        ']': {
            'left': '[',
            'c_points': 57,
            'i_points': 2
        },
        '}': {
            'left': '{',
            'c_points': 1197,
            'i_points': 3
        },
        '>': {
            'left': '<',
            'c_points': 25137,
            'i_points': 4
        },
    }
    left_brackets = ('(', '[', '{', '<')

    last = StackNode()

    for char in line:
        if char in left_brackets:
            p = StackNode(char)
            p.prev = last
            last = p

        elif last.val == brackets_data[char]['left']:
            p = last
            last = last.prev
            del p

        else:
            return brackets_data[char]['c_points'], True
    
    completion_string = ''
    while last.prev != None:
        completion_string += brackets_data[last.val]
        p = last
        last = last.prev
        del p
    for char in completion_string:
        score = score*5 + brackets_data[char]['i_points']
    return score, False


def parser():
    data = []
    a = input()
    while a:
        data.append(a)
        a = input()
    return data


def d10p1(data):
    ans = 0
    for line in data:
        tmpval, tmpbool = checks(line)
        if tmpbool:
            ans += tmpval
    return ans


def d10p2(data):
    counter = 0
    first = ListNode()
    for line in data:
        tmpval, tmpbool = checks(line)
        if not tmpbool:
            counter += 1
            p = ListNode(tmpval)
            q = first
            while q.next != None and q.next.val < tmpval:
                q = q.next
            p.next = q.next
            q.next = p
    q = first
    for _ in range(counter//2):
        q = q.next
    return q.next.val

if __name__ == '__main__':
    data = parser()
    print(d10p1(data))
    print(d10p2(data))