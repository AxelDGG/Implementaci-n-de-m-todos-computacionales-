# visualize_automata.py
# Dibuja el AFD usando graphviz

from graphviz import Digraph

def draw_dfa(transitions, start, accepting, filename='dfa'):
    """Genera un gráfico .png del AFD."""
    dot = Digraph(format='png')
    # Estados
    for q in transitions:
        shape = 'doublecircle' if q in accepting else 'circle'
        dot.node(str(q), shape=shape)
    dot.node('', shape='none')  # nodo invisible para flecha inicial
    dot.edge('', str(start))

    # Transiciones
    for q, moves in transitions.items():
        for sym, r in moves.items():
            dot.edge(str(q), str(r), label=sym)

    dot.render(filename, cleanup=True)
    print(f"DFA guardado como {filename}.png")
