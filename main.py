from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add')
def buy():
    return render_template('add.html')


@app.route('/korzina')
def abort():
    return render_template('korzina.html')


if __name__ == '__main__':
    app.run(port=60000, host='0.0.0.0')
