from stack import Stack


def infix_to_rpn(expr):
    ops = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '(': 10, ')': -10}
    st = Stack(100)
    l_ind = 0
    previous_was_op = False
    for ind, char in enumerate(expr):
        if char in ops:
            if not previous_was_op: # prev is digit, curr is op
                num_str = expr[l_ind:ind]
                l_ind = ind+1
                st.push(float(num_str) if '.' in num_str else int(num_str))
            else: # prev is op, curr is op e.g. +(x/y)*
                l_ind += 1
                pass
            previous_was_op = True
        else: # prev is digit, curr is digit
            previous_was_op = False
    # to do: implement unary minus as well as everything else


def rpn_calc():
    operators = ('+', '-', '*', '/', '^')
    st = Stack(100)
    while True:
        u_input = input()
        try:
            if '.' in u_input:
                val = float(u_input)
            else:
                val = int(u_input)
            st.push(val)
        except ValueError:
            if u_input == 'c':
                st.setempty()
            elif u_input == 'p':
                if st.empty():
                    print('Error: Stack is empty')
                else:
                    print(st.top())
            elif u_input == 'P':
                if st.empty():
                    print('Error: Stack is empty')
                else:
                    print(st.pop())
            elif u_input in operators:
                if st.empty():
                    print('Error: Stack is empty')
                else:
                    operand_2 = st.pop()
                    if st.empty():
                        print('Error: Stack is empty')
                        st.push(operand_2)
                    else:
                        operand_1 = st.top()
                        if u_input == '+':
                            value = operand_1 + operand_2
                        elif u_input == '-':
                            value = operand_1 - operand_2
                        elif u_input == '*':
                            value = operand_1 * operand_2
                        elif u_input == '^':
                            if 0 == operand_1 == operand_2:
                                print('Error: 0^0 is undefined')
                                st.push(operand_2)
                                continue
                            elif operand_1 < 0 and int(operand_2) != operand_2:
                                print(
                                    'Error: Non-integer power of a negative number')
                                st.push(operand_2)
                                continue
                            else:
                                value = operand_1 ** operand_2
                        elif u_input == '/':
                            if operand_2 == 0:
                                print('Error: Division by zero')
                                st.push(operand_2)
                                continue
                            else:
                                value = operand_1 / operand_2
                        st.pop()
                        st.push(value)
            else:
                print('Error: Unknown operator/command')
        except OverflowError:
            print('Error: Stack is full')


if __name__ == '__main__':
    rpn_calc()
