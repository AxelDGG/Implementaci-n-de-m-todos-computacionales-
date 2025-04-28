# regex_to_nfa.py
# Construcción de AFN (Thompson) con Shunting-Yard para manejar paréntesis y concatenación

class State:
    def __init__(self):
        self.transitions = {}  # símbolo → [estados]
        self.epsilon = []      # ε-transiciones

class NFA:
    def __init__(self, start: State, accept: State):
        self.start = start
        self.accept = accept

def add_concat(regex: str) -> str:
    """Inserta explícitamente '.' donde haya concatenación implícita."""
    result = []
    prev = None
    ops = {'|', '*', '.'}
    for c in regex:
        if prev is not None:
            # si prev no es operador ni '(', y c no es operador ni ')', inserto '.'
            if prev not in ops and prev != '(' and c not in ops and c != ')':
                result.append('.')
        result.append(c)
        prev = c
    return ''.join(result)

def infix_to_postfix(regex: str) -> list[str]:
    """Convierte infija → postfix con precedencia: * (3), . (2), | (1)."""
    prec = {'*': 3, '.': 2, '|': 1}
    out = []
    stack: list[str] = []
    for c in regex:
        if c == '(':
            stack.append(c)
        elif c == ')':
            # vaciar hasta '('
            while stack and stack[-1] != '(':
                out.append(stack.pop())
            stack.pop()
        elif c in prec:
            # mientras haya operador de mayor o igual precedencia (salvo '*' que es right-assoc)
            while stack and stack[-1] != '(' and (
                prec[stack[-1]] > prec[c] or
                (prec[stack[-1]] == prec[c] and c != '*')
            ):
                out.append(stack.pop())
            stack.append(c)
        else:
            # operando (símbolo)
            out.append(c)
    # vaciar pila
    while stack:
        out.append(stack.pop())
    return out

def regex_to_nfa(regex: str) -> NFA:
    """Punto de entrada: toma R en infija, genera AFN."""
    # 1) añado concatenaciones implícitas
    regex = add_concat(regex)
    # 2) convierto a postfix
    postfix = infix_to_postfix(regex)
    # 3) Thompson
    stack: list[NFA] = []
    for token in postfix:
        if token == '*':
            nfa1 = stack.pop()
            start = State(); accept = State()
            start.epsilon += [nfa1.start, accept]
            nfa1.accept.epsilon += [nfa1.start, accept]
            stack.append(NFA(start, accept))

        elif token == '.':
            nfa2 = stack.pop(); nfa1 = stack.pop()
            nfa1.accept.epsilon.append(nfa2.start)
            stack.append(NFA(nfa1.start, nfa2.accept))

        elif token == '|':
            nfa2 = stack.pop(); nfa1 = stack.pop()
            start = State(); accept = State()
            start.epsilon += [nfa1.start, nfa2.start]
            nfa1.accept.epsilon.append(accept)
            nfa2.accept.epsilon.append(accept)
            stack.append(NFA(start, accept))

        else:
            # símbolo literal
            start = State(); accept = State()
            start.transitions[token] = [accept]
            stack.append(NFA(start, accept))

    return stack.pop()
