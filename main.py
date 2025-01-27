from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash
import db_operations
from rss import gen_rss
import os
from werkzeug.utils import secure_filename
import proc_img
import json


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
        count = int(request.form.get('mass', 0))
        mass_id = request.form.get('productCategory')
        start_date = request.form['startDate']
        B = int(request.form.get('proteinsG', 0))
        J = int(request.form.get('fatsG', 0))
        U = int(request.form.get('carbsG', 0))

        pid = db_operations.add_product(name, class_name, stop_date, count, mass_id,
                                  start_date, B, J, U)
        print(request.form['stopDate'], request.form['startDate'])

        return redirect(url_for('infabout', pid=pid))

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


@app.route('/api/get_analytics/<int:start_date>/<int:stop_date>')
def send_analytics(start_date, stop_date):
    return jsonify({"products": db_operations.get_products_stamp(start_date, stop_date), "deleted": db_operations.get_deleted_stamp(start_date, stop_date)}) 


@app.route('/infabout', methods=['GET', 'POST'])
def infabout():
    if request.method == 'POST':
        try:
            UPLOAD_FOLDER = "imageQR"
            app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    
            file = request.files["image"]
    
            filename = secure_filename(file.filename)
    
            file.save("PNG.png")
            dst = proc_img.decode_qr_from_image("PNG.png")
    
            if dst[0] == '{':
                product = json.loads(dst)
                pid = db_operations.add_product(product.get('product_name'), product.get('class'),
                                product.get('stop_date'), product.get('count'), product.get('is_kg'),
                                product.get('start_date'), product.get('B'), product.get('J'), product.get('U'))
                return redirect(f'/infabout?pid={pid}')
            else:
                d = db_operations.get_product(dst)
            b64add = proc_img.generate_qr_base64(json.dumps(d))
            b64 = proc_img.generate_qr_base64(dst)
            return render_template('infabout.html', d=d, b64=b64, b64add=b64add)
        except Exception as e:
            print(e)
            return render_template('infabout.html', d={})

    if request.args.get('pid') is not None:
        d = db_operations.get_product(request.args.get('pid'))
        b64 = proc_img.generate_qr_base64(request.args.get('pid'))
        b64add = proc_img.generate_qr_base64(json.dumps(d))
        return render_template('infabout.html', d=d, b64=b64, flag=True, b64add=b64add)
    return render_template('infabout.html')



@app.route('/api/delete/<int:id>')
def api_de(id):
    db_operations.delete_product(id)
    return 'ok'


@app.route('/api/add_same/<int:id>')
def api_add_s(id):
    product = db_operations.get_product(id)
    print(product)
    db_operations.add_product(product.get('product_name'), product.get('class'),
                              product.get('stop_date'), product.get('count'), product.get('is_kg'),
                              product.get('start_date'), product.get('B'), product.get('J'), product.get('U'))
    return 'ok'


@app.route('/api/delete_buy/<int:bid>')
def api_del_buy(bid):
    db_operations.delete_buy(bid)
    return "ok"


@app.route('/api/add_buy/<int:pid>')
def api_add_buy(pid):
    db_operations.add_buy(pid)
    return "ok"


@app.route('/api/get_deleted')
def get_deleted():
    return jsonify(db_operations.get_deleted())


@app.route("/api/get_buys")
def get_buys():
    return jsonify(db_operations.get_buys())


@app.route("/analytics")
def analytics_page():
    return render_template("analytics.html")


@app.route('/buys')
def show_buys():
    return render_template("buys.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
