import argparse
import logging
import math
import operator
import pprint
import string


logging.basicConfig(level=logging.DEBUG)

operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '**': operator.pow,
}

memory = {
    'pi': math.pi,
    'e': math.e,
}

errmsg = 'SYNTAX ERROR'
okmsg  = 'OK'

def clearmemory():
    global memory
    memory = {}
    return okmsg
def showmemory():
    return pprint.pformat(memory)

commands = {
    'clrmem': clearmemory,
    'mem': showmemory,
}

def isnumber(x):
    try:
        return float(x)
    except ValueError:
        return None

def isunit(x:str):
    s = 0
    for i, l in enumerate(x):
        if not(l.isdigit() or l == '.'):
            s = i
            break
    if s > 0:
        unit = x[s:]
        num = x[:s]
        return float(num), unit
    else:
        num = isnumber(x)
        return num, None



def evaluate(expression):
    ops = []
    nums = []
    res = 0
    sub = 0
    tba = False

    logging.debug(f'Received expression with terms: {expression}')


    if len(expression) >= 3 and expression[1] == '=':
        tba, _ = expression.pop(0), expression.pop(0)

    for term in expression:

        number, unit = isunit(term)
        if number is not None:
            if unit is not None:
                if unit not in memory.keys():
                    logging.error(f'Unrecognized unit: {unit}')
                    return errmsg
                number *= memory[unit]
            nums.append(number)
        
        elif term in memory.keys():
            nums.append(memory[term])

        elif term in operators.keys():
            if not len(nums) % 2 == 0:
                logging.error('Syntax error: odd number of terms before and operator')
                return errmsg
            t2, t1 = nums.pop(), nums.pop()
            sub = operators[term](t1, t2)
            nums.append(sub)
        elif term in commands:
            return commands[term]()
        else:
            logging.error(f'Unrecognized term: {term}')
            return errmsg

    res = nums[0]

    if tba:
        memory[tba] = res
        print(memory)

    return res


def entry():
    interactive = False
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        dest='verbose',
                        help='Verbose Output'
                        )
    parser.add_argument('expression',
                        nargs='*',
                        help='The expression to be evaluated')
    parser.add_argument('-i', '--interactive',
                        action='store_true',
                        dest='interactive',
                        help='Start an interactive shell')

    args = parser.parse_args()
    expression = args.expression

    # initiate an interactive shell if needed
    if len(expression) == 0 or args.interactive:
        while True:
            expression = input('$ ')
            if expression.strip() not in ['q', 'quit', 'exit']:
                result = evaluate(expression.split(' '))
                print('=', result)
            else:
                break

    elif len(expression) == 1 and ' ' in expression[0]:
        expression = expression[0].split(' ')

        result = evaluate(expression)
        print('\n=', result)

    print('Farewell, stargazer.')


if __name__ == '__main__':
    entry()
