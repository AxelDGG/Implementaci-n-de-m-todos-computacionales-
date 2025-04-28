# nfa_to_dfa.py
# Conversión AFN → AFD mediante algoritmo de subconjuntos

from collections import deque

def epsilon_closure(states):
    """Cierra un conjunto de estados por ε-transiciones."""
    stack = list(states)
    closure = set(states)
    while stack:
        state = stack.pop()
        for nxt in state.epsilon:
            if nxt not in closure:
                closure.add(nxt)
                stack.append(nxt)
    return closure

def move(states, symbol):
    """Devuelve el conjunto de estados alcanzables con 'symbol'."""
    result = set()
    for s in states:
        for dest in s.transitions.get(symbol, []):
            result.add(dest)
    return result

def nfa_to_dfa(nfa, alphabet):
    """Construye un AFD a partir de un AFN y su alfabeto."""
    start_closure = frozenset(epsilon_closure([nfa.start]))
    dfa_states = {start_closure: 0}
    dfa_trans = {}
    accepting = set()
    queue = deque([start_closure])

    while queue:
        current = queue.popleft()
        idx = dfa_states[current]
        dfa_trans[idx] = {}
        if nfa.accept in current:
            accepting.add(idx)
        for sym in alphabet:
            # transición en subconjuntos
            target = frozenset(epsilon_closure(move(current, sym)))
            if not target:
                continue
            if target not in dfa_states:
                dfa_states[target] = len(dfa_states)
                queue.append(target)
            dfa_trans[idx][sym] = dfa_states[target]

    return dfa_trans, 0, accepting
