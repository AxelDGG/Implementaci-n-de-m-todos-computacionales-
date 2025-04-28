# app.py
from flask import Flask, render_template, request, url_for
from regex_to_nfa import regex_to_nfa
from nfa_to_dfa import nfa_to_dfa
from visualize_automata import draw_dfa

app = Flask(__name__)
dfa_data = {}

@app.route("/", methods=["GET", "POST"])
def index():
    sigma_txt = ""
    regex = ""
    image = False
    result = None
    accepted = False

    if request.method == "POST":
        sigma_txt = request.form["sigma"]
        sigma = [s.strip() for s in sigma_txt.split(",") if s.strip()]
        regex = request.form["regex"]

        # Si no envío test_str, genero el DFA
        if "test_str" not in request.form:
            nfa = regex_to_nfa(regex)
            trans, start, accept = nfa_to_dfa(nfa, sigma)
            draw_dfa(trans, start, accept, filename="static/resultado_dfa")
            dfa_data.update(trans=trans, start=start, accept=accept)
            image = True
        else:
            # Si envío test_str, pruebo la palabra
            w = request.form["test_str"]
            cur = dfa_data["start"]
            for c in w:
                cur = dfa_data["trans"].get(cur, {}).get(c)
                if cur is None:
                    break
            accepted = (cur in dfa_data["accept"])
            result = "ACEPTADA ✅" if accepted else "RECHAZADA ❌"
            image = True

    return render_template(
        "index.html",
        sigma=sigma_txt,
        regex=regex,
        image=image,
        result=result,
        accepted=accepted,
    )

if __name__ == "__main__":
    app.run(debug=True)
