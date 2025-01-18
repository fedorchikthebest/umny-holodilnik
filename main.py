from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash
import db_operations
from rss import gen_rss
import os
from werkzeug.utils import secure_filename
import f

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', products=db_operations.get_products())


@app.route("/add", methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['productName']
        class_name = request.form['productClass']
        stop_date = request.form['stopDate']
        count = 1
        mass_id = 0
        start_date = request.form['startDate']
        B = int(request.form.get('proteinsG', 0))
        J = int(request.form.get('fatsG', 0))
        U = int(request.form.get('carbsG', 0))

        db_operations.add_product(name, class_name, stop_date, count, mass_id,
                                  start_date, B, J, U)
        print(request.form['stopDate'], request.form['startDate'])

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/korzina')
def korzina():
    return render_template('korzina.html',
                           products=db_operations.get_products())


@app.route("/rss")
def rss():
    r = make_response(gen_rss())
    r.headers.set('Content-Type', 'application/rss+xml')
    return r


@app.route('/api')
def api():
    return jsonify(db_operations.get_products())


@app.route('/delite', methods=['GET', 'POST'])
def delite():
    if request.method == 'POST':
        UPLOAD_FOLDER = "static"
        app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

        if request.method == "POST":
            file = request.files["image"]

            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    return render_template('delite.html')


if __name__ == '__main__':
    app.run(debug=True)
