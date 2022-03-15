class Stack:
    def __init__(self, s_size):
        self.s_size = s_size
        self.stack = [None for _ in range(s_size)]
        self.curr = -1

    def push(self, obj):
        if self.curr < self.s_size-1:
            self.curr += 1
            self.stack[self.curr] = obj
        else:
            raise OverflowError('Stack overflow')

    def empty(self):
        return True if self.curr == -1 else False

    def top(self):
        return self.stack[self.curr] if self.curr != -1 else None

    def pop(self):
        if self.curr > -1:
            self.curr -= 1
            return self.stack[self.curr+1]
        else:
            raise IndexError('Stack is empty')

    def setempty(self):
        self.curr = -1
