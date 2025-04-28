# main.py
# Interfaz de línea de comandos para usar los módulos anteriores

from regex_to_nfa import regex_to_nfa
from nfa_to_dfa import nfa_to_dfa
from visualize_automata import draw_dfa

def parse_alphabet(inp):
    """Lee alfabeto separado por comas."""
    return [s.strip() for s in inp.split(',') if s.strip()]

def main():
    print("=== Generador de AFD desde Expresión Regular === 🌟")
    sigma = parse_alphabet(input("Ingresa el alfabeto Σ (ej: 0,1,a,b): "))
    regex = input("Ingresa la expresión regular (usa . para concatenar): ")
    nfa = regex_to_nfa(regex)
    dfa_trans, dfa_start, dfa_accept = nfa_to_dfa(nfa, sigma)
    draw_dfa(dfa_trans, dfa_start, dfa_accept, filename='resultado_dfa')

    # Pruebas de reconocimiento
    while True:
        w = input("Ingresa una palabra para probar (ENTER para salir): ")
        if not w:
            break
        current = dfa_start
        for c in w:
            current = dfa_trans.get(current, {}).get(c, None)
            if current is None:
                break
        resultado = "ACEPTADA ✅" if current in dfa_accept else "RECHAZADA ❌"
        print(f"Palabra '{w}': {resultado}\n")

if __name__ == "__main__":
    main()
