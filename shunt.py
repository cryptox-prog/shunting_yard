class MathFunctions:
    pi = 3.141592653589793
    straight_angle_deg = 180

    @staticmethod
    def deg_to_rad(x):
        return (MathFunctions.pi / MathFunctions.straight_angle_deg) * x

    @staticmethod
    def exp(x):
        result = 0
        term = 1
        n = 0
        while abs(term) > 1e-15:
            result += term
            n += 1
            term *= x / n
        return result

    @staticmethod
    def sqrt(x):
        return x ** 0.5

    @staticmethod
    def sin(x):
        # Using Taylor Series with the accuracy of 1*10^-15
        x = x % (2 * MathFunctions.pi)  # Since Period is 2pi
        result = 0
        term = x
        n = 1
        while abs(term) > 1e-15:
            result += term
            term *= -x ** 2 / ((n + 1) * (n + 2))
            n += 2
        return result

    @staticmethod
    def cos(x):
        return MathFunctions.sin((MathFunctions.pi / 2) - x)

    @staticmethod
    def tan(x):
        cos_x = MathFunctions.cos(x)
        if abs(cos_x) < 1e-15:
            raise ZeroDivisionError
        else:
            return MathFunctions.sin(x) / cos_x

    @staticmethod
    def gamma(x):
        # Using Lanczos Approximation
        pi = MathFunctions.pi
        p = [676.5203681218851, -1259.1392167224028, 771.32342877765313,
             -176.61502916214059, 12.507343278686905, -0.13857109526572012,
             9.9843695780195716e-6, 1.5056327351493116e-7]
        g = 7
        if x < 0.5:
            return MathFunctions.pi / (MathFunctions.sin(pi * x) * MathFunctions.gamma(1 - x))
        else:
            x -= 1
            a = 0.99999999999980993
            for i in range(g):
                a += p[i] / (x + i + 1)
            t = x + g + 0.5
            return MathFunctions.sqrt(2 * pi) * t ** (x + 0.5) * MathFunctions.exp(-t) * a

    @staticmethod
    def factorial(x):
        return MathFunctions.gamma(x + 1)

    @staticmethod
    def newton(f, df, x0, tol=1e-15):
        # Using Newton-Raphson
        x = x0
        while abs(f(x)) > tol:
            x -= f(x) / df(x)
        return x

    @staticmethod
    def asin(x):
        if x < -1 or x > 1:
            raise ValueError("The input must be in the range [-1, 1].")
        f = lambda y: MathFunctions.sin(y) - x
        df = MathFunctions.cos
        if x > 0:
            return MathFunctions.newton(f, df, 0)
        elif x < 0:
            return MathFunctions.newton(f, df, -MathFunctions.pi / 2)
        else:
            return 0

    @staticmethod
    def acos(x):
        if x < -1 or x > 1:
            raise ValueError("The input must be in the range [-1, 1].")
        return MathFunctions.asin(MathFunctions.sqrt(1 - x ** 2))

    @staticmethod
    def atan(x):
        return MathFunctions.asin(x / MathFunctions.sqrt(x ** 2 + 1))

    @staticmethod
    def bisect(f, a, b, tol=1e-15):
        fa, fb = f(a), f(b)
        if fa * fb >= 0:
            raise ValueError("The function must have opposite signs at a and b.")
        while (b - a) / 2 > tol:
            c = (a + b) / 2
            fc = f(c)
            if fc == 0:
                return c
            elif fa * fc < 0:
                b, fb = c, fc
            else:
                a, fa = c, fc
        return (a + b) / 2

    @staticmethod
    def ln(x):
        if x <= 0:
            raise ValueError("The input must be positive.")
        f = lambda y: MathFunctions.exp(y) - x
        return MathFunctions.bisect(f, 0, x)

    @staticmethod
    def log(x, b):
        if x <= 0 or b <= 0 or b == 1:
            raise ValueError("The inputs must be positive.")
        return MathFunctions.ln(x) / MathFunctions.ln(b)

    @staticmethod
    def floor(x):
        if x >= 0:
            if x.is_integer():
                return int(x)
            else:
                return int(x)
        else:
            return int(x) - 1

    @staticmethod
    def ceil(x):
        if x >= 0:
            return int(x) + 1
        else:
            return int(x)


class Evaluate:

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
            "functions": (4,
                          {"sqrt": lambda x: MathFunctions.sqrt(x),
                           "cbrt": lambda x: x ** (1 / 3),
                           "sin": lambda x: MathFunctions.sin(MathFunctions.deg_to_rad(x)),
                           "cos": lambda x: MathFunctions.cos(MathFunctions.deg_to_rad(x)),
                           "tan": lambda x: MathFunctions.tan(MathFunctions.deg_to_rad(x)),
                           "log": lambda x: MathFunctions.log(x, 10),
                           "asin": lambda x: MathFunctions.asin(x),
                           "acos": lambda x: MathFunctions.acos(x),
                           "atan": lambda x: MathFunctions.atan(x),
                           "fact": lambda x: MathFunctions.factorial(x),
                           "abs": abs,
                           "ceil": lambda x: MathFunctions.ceil(x),
                           "floor": lambda x: MathFunctions.floor(x),
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
print(clas.eval_("3-2"))
