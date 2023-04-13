import math

class Evaluate:
    @staticmethod
    def factorial(n):
        if n <= 2:
            return n
        else:
            return n * Evaluate.factorial(n - 1)

    @staticmethod
    def eval_(expr):
        output_queue = []
        operator_stack = []
        operators = {
            "+": (1, lambda a1, b1: a1 + b1),
            "-": (1, lambda a1, b1: a1 - b1),
            "*": (2, lambda a1, b1: a1 * b1),
            "/": (2, lambda a1, b1: a1 / b1),
            "^": (3, lambda a1, b1: a1 ** b1),
            "functions_": (4,
                           {"sqrt": math.sqrt,
                            "cbrt": lambda x: math.pow(x, 1 / 3),
                            "sin": lambda x: math.sin(math.radians(x)),
                            "cos": lambda x: math.cos(math.radians(x)),
                            "tan": lambda x: math.tan(math.radians(x)),
                            "log": math.log10,
                            "sinh": lambda x: math.sinh(math.radians(x)),
                            "cosh": lambda x: math.cosh(math.radians(x)),
                            "tanh": lambda x: math.tanh(math.radians(x)),
                            "fact": lambda x: Evaluate.factorial(x),
                            "abs": abs,
                            "ceil": math.ceil,
                            "floor": math.floor,
                            "round": round
                            })
        }

        tokens = expr.replace(" ", "")
        i = 0
        while i < len(tokens):
            token = ""
            if tokens[i].isdigit() or tokens[i] == ".":
                while i < len(tokens) and (tokens[i].isdigit() or tokens[i] == "."):
                    token += tokens[i]
                    i += 1
                output_queue.append(float(token))
                continue
            elif tokens[i].isalpha():
                while i < len(tokens) and tokens[i].isalpha():
                    token += tokens[i]
                    i += 1
                if token in operators["functions_"][1]:
                    operator_stack.append(operators["functions_"][1][token])
                else:
                    raise ValueError(f"Unknown function: {token}")
                continue
            elif tokens[i] in operators:
                op1 = tokens[i]
                while len(operator_stack) > 0 and operator_stack[-1] in operators:
                    op2 = operator_stack[-1]
                    if (operators[op1][0] == operators[op2][0] and op1 == "^") or \
                            operators[op1][0] < operators[op2][0]:
                        output_queue.append(operator_stack.pop())
                    else:
                        break
                operator_stack.append(op1)
            elif tokens[i] == "(":
                operator_stack.append(tokens[i])
            elif tokens[i] == ")":
                while len(operator_stack) > 0 and operator_stack[-1] != "(":
                    output_queue.append(operator_stack.pop())
                if len(operator_stack) == 0:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()
            else:
                raise ValueError(f"Unknown token: {tokens[i]}")
            i += 1

        while len(operator_stack) > 0:
            op = operator_stack.pop()
            if op == "(":
                raise ValueError("Mismatched parentheses")
            output_queue.append(op)

        stack = []
        for token in output_queue:
            if isinstance(token, float):
                stack.append(token)
            elif callable(token):
                if len(stack) < 1:
                    raise ValueError("Not enough arguments for function")
                a = stack.pop()
                stack.append(token(a))
            else:
                if len(stack) < 2:
                    raise ValueError("Not enough operands")
                b = stack.pop()
                a = stack.pop()
                if token in ('+', '-'):
                    if isinstance(a, tuple) and a[1] > operators[token][0]:
                        a = a[0](a[1:])
                    if isinstance(b, tuple) and b[1] > operators[token][0]:
                        b = b[0](b[1:])
                result = operators[token][1](a, b)
                if token in ('*', '/'):
                    if isinstance(a, tuple):
                        stack.append((operators[token][1], a[1:], b))
                    elif isinstance(b, tuple):
                        stack.append((operators[token][1], a, b[1:]))
                    else:
                        stack.append(result)
                else:
                    stack.append(result)
        return stack.pop()


clas = Evaluate()
print(clas.eval_("-(5*6)+(3^2)"))
