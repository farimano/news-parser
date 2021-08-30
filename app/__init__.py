import io
from flask import Flask, Response, render_template, request

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

from .main_model import *

class KeyWord(object):
    key_word = None

KW = KeyWord()

app = Flask(__name__)

@app.route("/plot")
def some_plot():
    key_word = KW.key_word
    if type(key_word) == str:
        fig = main_model.model(n=4, key_word=key_word)
        KW.key_word = None
        output = io.BytesIO()
        FigureCanvasAgg(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')


@app.route("/", methods=['GET', 'POST'])
def template():
    out = None
    if request.method == 'POST':
        key_word = request.form.get('key_word')
        KW.key_word = key_word
        out = '/plot'
    return render_template('base.html', title='temp', out=out)