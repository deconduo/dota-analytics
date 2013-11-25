from os import environ
import os
from flask import Flask, make_response, render_template, request, url_for
import settings
from celery import Celery
from tasks import celeryData

app = Flask(__name__)
app.config.from_object(settings)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processing', methods=['POST'])
def getData():
    steamID = request.form['steamid']
    x = 0
    res = celeryData.apply_async((steamID, x))
    return res.task_id

@app.route('/graph/<task_id>')
def graph(task_id):
    cleanData = celeryData.AsyncResult(task_id).get(timeout=1.0)
    return render_template('graph.html', cleanData = cleanData)

if __name__ == '__main__':
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
