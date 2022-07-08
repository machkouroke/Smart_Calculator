from collections import deque

variable = {}
priority = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2}
operations = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b,
    '^': lambda a, b: a ** b,
}
UNKNOWN = 'Unknown Variable'
INVALID_ASSIGN = 'Invalid assignment'
INVALID_EX = 'Invalid Expression'
INVALID_ID = 'Invalid identifier'
RIGHT_EX = 'Right Expression'


def name_validator(name):
    """
    Checks if a number of variable
    is valid then returns true or false
    :param name: a string to check
    :return: the boolean value of checking
    """
    return bool(name.isalpha())


def str_to_number(string):
    """
    Converts a string of the form '(+/-)1' * n
    into a list where the digits are dissociated
    :param string: string of '(+/-)1' * n
    :return: list where the digits are dissociated
    """
    x = 0
    number = []
    while x < len(string):
        if string[x] == '-':
            number.append(-1)
            x += 2
            continue
        number.append(string[x])
        x += 1
    return number


def variable_substitute(expression):
    """
    Replace variables with their values
    :param expression:
    :return:
    """
    for x in range(len(expression)):
        if expression[x].isalpha() and expression[x] in variable:
            expression[x] = str(variable[expression[x]])
        elif expression[x].isalpha() and expression[x] not in variable:
            return UNKNOWN
        elif (not expression[x].isalpha()) and (not expression[x].isdigit()) and (
                expression[x] not in {'+', '*', '-', '/', '^', '(', ')'}):
            return INVALID_ASSIGN
    return expression


def sign_eval(sgn_list):
    """
    Evaluate signs and return their equivalent sign
    :param sgn_list: sign list
    :return: list of equivalent signs
    """
    signe = {'+': 1, '-': -1}
    new_sgn_list = []
    for x in sgn_list:
        if '*' in x or '/' in x or '^' in x:
            new_sgn_list.append(x)
        else:
            x_num = x
            for a, b in signe.items():
                x_num = x_num.replace(a, str(b))
            x_num = str_to_number(x_num)
            s = 1
            for k in x_num:
                s *= int(k)
            new_sgn_list.append('+') if s == 1 else new_sgn_list.append('-')
    return new_sgn_list


def string_dissociator(s):
    """
    Separates the expression in tuple of sign and number
    :param s: expression
    :return: the tuple containing the list of signs and the list of numbers
    """
    signs, number, x = [], [], 0
    while x < len(s):
        if s[x] in operations:
            sig = []
            for _ in range(x, len(s)):
                if s[x] in operations:
                    sig += s[x]
                    x += 1
                    continue
                break
            signs.append(''.join(sig))
        else:
            if x == 0:
                signs.append('')
            num = []
            for _ in range(x, len(s)):
                if s[x] not in operations:
                    num += s[x]
                    x += 1
                    continue
                break
            number.append(''.join(num))
    signs = sign_eval(signs)
    return signs, number


def expression_validator(expression, mode='simple'):
    """
    Return True if the expression is valid and false else
    :param mode:
    :param expression:
    :return: Boolean True or False
    """
    brackets = deque()
    for x in expression:
        if x == '(':
            brackets.append(x)
        elif x == ')':
            try:
                brackets.pop()
            except IndexError:
                return INVALID_EX
    if len(brackets) != 0 or expression[-1] in {'+', '-', '*', '/', '^', '='}:
        return INVALID_EX
    if expression.find('=') != -1:
        return 'Affectation'
    find = [expression.find(x) for x in operations]
    if find == [-1 for _ in range(4)]:
        if expression.find(' ') != -1:
            return INVALID_EX
        elif expression.find(' ') == -1:
            if mode != 'affectation':
                if expression.isdigit():
                    return RIGHT_EX
                elif expression.isalpha():
                    return RIGHT_EX if expression in variable else UNKNOWN
                elif not expression.isalpha() and not expression.isdigit():
                    return INVALID_ID

    return RIGHT_EX


def variable_add(expression):
    if expression.count('=') > 1:
        print(INVALID_ASSIGN)
        return
    a = expression.replace(' ', '').split('=')
    if not name_validator(a[0]):
        print(INVALID_ID)
        return
    elif expression_validator(a[1], 'affectation') in [INVALID_EX, INVALID_ID]:
        print(INVALID_ASSIGN)
        return
    elif expression_validator(a[1], 'affectation') == UNKNOWN:
        print(UNKNOWN)
        return
    variable[a[0]] = infix_to_posfix(infix_dissociator(a[1]))
    if variable[a[0]] in [UNKNOWN, INVALID_ASSIGN]:
        print(variable[a[0]])
    else:
        variable[a[0]] = posfix_o_answer(variable[a[0]])


def infix_dissociator(infix):
    a, b = string_dissociator(infix)
    new_infix = []
    for x, y in zip(a, b):
        new_infix.append(x)
        if not y.isdigit():
            if '(' in y:
                new_infix.extend(list('(' * y.count('(')))
            new_infix.append(y.replace('(', '').replace(')', ''))
            if ')' in y:
                new_infix.extend(list(')' * y.count(')')))
        else:
            new_infix.append(y)
    return new_infix[1:]


def infix_to_posfix(infix):
    op_stack = deque()
    posfix = []
    infix = variable_substitute(infix)
    if infix in [UNKNOWN, INVALID_ASSIGN]:
        return infix
    for x in infix:
        if x.isdigit():
            posfix.append(x)
        elif x == '(':
            op_stack.append(x)
        elif len(op_stack) == 0 and x != ')':
            op_stack.append(x)
        elif x == ')':
            while 1:
                if op_stack[-1] == '(':
                    op_stack.pop()
                    break
                x = op_stack.pop()
                posfix.append(x)
                if op_stack[-1] == '(':
                    op_stack.pop()
                    break
        elif op_stack[-1] == '(' or priority[op_stack[-1]] < priority[x]:
            op_stack.append(x)
        else:
            while 1:
                if len(op_stack) > 0:
                    if op_stack[-1] == '(' or priority[x] > priority[op_stack[-1]]:
                        op_stack.append(x)
                        break
                    else:
                        y = op_stack.pop()
                        posfix.append(y)
                else:
                    op_stack.append(x)
                    break
    while 1:
        try:
            posfix.append(op_stack.pop())
        except IndexError:
            break

    return posfix


def posfix_o_answer(expression):
    answer = deque()

    for x in expression:
        if x.isdigit():
            answer.append(int(x))
        elif x in operations:
            b, a = [answer.pop() for _ in range(2)]
            try:
                answer.append(operations[x](a, b))
            except ZeroDivisionError:
                print('Division by zero ')
                return
    return int(answer[0])


def main():
    while 1:
        expression = ''.join(input("Veuillez saisir votre expression: ").split(' '))
        if expression != "":
            if expression[0] == '/':
                if expression == '/exit':
                    print('Bye!')
                    break
                elif expression == '/help':
                    print("""Le programme évalue des expressions données puis renvoie un résultat.
Vous pouviez y ajouter des variables et affecter des valeurs à ces variables
Exemple:
> a = 2
> b = 3
> a + b
5
                    """)
                else:
                    print('Unknown command')
            elif expression_validator(expression) == 'Affectation':
                variable_add(expression)
            elif expression_validator(expression) != RIGHT_EX:
                print(expression_validator(expression))
            else:
                answer = infix_dissociator(expression)
                if answer != 'Unknown':
                    answer = infix_to_posfix(answer)
                    if answer in [UNKNOWN, INVALID_ASSIGN]:
                        print(answer)
                    else:
                        print(posfix_o_answer(answer))


if __name__ == '__main__':
    main()
