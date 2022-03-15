from stack import Stack


def ack(a, b, mem):
    if (a, b) in mem:
        return mem[(a, b)]
    if a == 0:
        r = b+1
    elif b == 0:
        r = ack(a-1, 1, mem)
    else:
        r = ack(a-1, ack(a, b-1, mem), mem)
    mem[(a, b)] = r
    return r


def ackermann(a, b, mem):
    st = Stack(100000)
    m_a = a
    m_b = b
    st.push(a)
    while not st.empty():
        a = st.pop()
        if a == 0:
            b += 1
        elif a == 1:
            b += 2
        elif a == 2:
            b = b*2 + 3
        elif (a, b) in mem:
            b = mem[(a, b)]
        elif b == 0:
            st.push(a-1)
            b = 1
        else:
            st.push(a-1)
            st.push(a)
            b -= 1
    if m_a > 2:
        mem[(m_a, m_b)] = b
    return b


if __name__ == '__main__':
    pass
