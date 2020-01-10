import os
import random as rdn
import spacy
from graphviz import Digraph
from flask import Flask, Markup, request, redirect, render_template

app = Flask(__name__)


@app.route('/index') # call index from another page
@app.route("/") # when directly root called, run the index function
def index():
    # open the index.html page
    for filename in os.listdir("static/"):
        os.remove("static/"+filename)
    return render_template('index.html')

# when the result url hit with a post request, show result function
@app.route('/output', methods=['POST'])
def result():
    sentence = request.form['sentence'] # receive the user input
    nlp = spacy.load("pt_core_news_sm")
    doc = nlp(sentence)
    graph = Digraph('G', filename='sentence.gv', format='png', node_attr={'shape': 'plaintext'})
    triplets = []
    for d in doc:
        triple = []
        main_pos = ["NOUN", "PROPN", "VERB"]
        if (d.dep_ == "nsubj" or d.dep_ == "nsubj:pass") and d.pos_ in main_pos:
            if d.head.pos_ == "VERB" and d.head.pos_ in main_pos:
                triple.append(d)
                triple.append(d.head)
                d2 = [d_ for d_ in doc if d_.head.i == d.head.i and d_ != d.head and d_ not in triple]
                if d2 != [] and triple != [] and d2[0].pos_ in main_pos:
                    triple.append(d2[0])


            elif d.head.pos_ in main_pos:
                triple.append(d)
                triple.append(d.head)
                d2 = [d_ for d_ in doc if d_.head.i == d.head.i and d_ != d.head and d_ not in triple and d_.pos_ == "VERB"]
                if d2 != [] and triple != []:
                    triple.append(d2[0])

        triple = [x for _, x in sorted(zip([t.i for t in triple], triple))]
        text = [tkn.text for tkn in triple]
        if len(triple) == 3:
            dependency = ["flat:name", "case", "nmod", "obj", "appos", "amod", "advmod", "acl:relcl", "obl", "conj", "xcomp"]
            t_ids = [(t.i, t.i+1) for t in triple]
            for tid, t in enumerate(triple):
                c1 = [d_ for d_ in doc if d_.head == t and d_ not in triple  and d_.dep_ in dependency]
                c2 = c1
                while c2 != []:
                    c2 = ([d_ for d_ in doc if d_ not in c1  and d_.head in c1 and d_.dep_ in dependency])
                    c1 = c1 + c2

                complements = c1
                if complements != []:
                    complements.append(t)
                    limits = (min([c.i for c in complements]), max([c.i for c in complements])+1)

                    ini, end = limits
                    if tid < 2 and end > t_ids[tid+1][0]:
                        end = t_ids[tid+1][0]
                    if tid > 0 and ini <= t_ids[tid-1][1]:
                        ini = t_ids[tid-1][1]

                    while doc[ini].dep_ == "punct": ini = ini+1

                    limits = (ini, end)
                    t_ids[tid] = limits

                    text[tid] = " ".join([doc[wi].text for wi in range(limits[0], limits[1])])

            triplets.append(text)

    graph_name = ""
    if triplets != []:
        for w1, rel, w2 in triplets:
            graph.node(str(w1))
            graph.node(str(w2))
            graph.edge(str(w1), str(w2), label=str(rel))
        graph_name = str(int(rdn.random()*1000))
        graph.render("static/"+graph_name)
    html = spacy.displacy.render(doc, style="dep", page=False)
    dependency = html

    relex = "<br>".join(["- "+str(w1)+" : "+str(rel)+" : "+str(w2)+"\n" for w1, rel, w2 in triplets])
    # send results for output.html render_template
    return render_template('output.html', phrase=sentence, graph=graph_name+".png", dependency=Markup(dependency), relations=relex)


if __name__ == "__main__":
    app.run(host='0.0.0.0')