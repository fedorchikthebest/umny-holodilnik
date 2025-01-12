from flask import Flask, render_template, request, redirect, url_for, jsonify
import db_operations

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
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/korzina')
def korzina():
    return render_template('korzina.html',
                           products=db_operations.get_products())


@app.route('/api')
def api():
    return jsonify(db_operations.get_products())


if __name__ == '__main__':
    app.run(debug=True)
