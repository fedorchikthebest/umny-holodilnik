from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash
import db_operations
from rss import gen_rss
import os
from werkzeug.utils import secure_filename
import proc_img
import dircr
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


@app.route('/infabout', methods=['GET', 'POST'])
def infabout():
    if request.method == 'POST':
        try:
            UPLOAD_FOLDER = "imageQR"
            app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

            file = request.files["image"]

            filename = secure_filename(file.filename)

            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            file.save(file_path)
            dst = proc_img.decode_qr_from_image(file_path)

            if dst[0] == '{':
                flag = False
                d = json.loads(dst)
            else:
                flag=True
                d = db_operations.get_product(dst)



            b64 = proc_img.generate_qr_base64(dst)
            return render_template('infabout.html', d=d, b64=b64, flag=flag)
        except Exception:
            return render_template('infabout.html', d={})
    print(request.args)
    if request.args.get('pid') is not None:
        d = db_operations.get_product(request.args.get('pid'))
        b64 = proc_img.generate_qr_base64(request.args.get('pid'))
        return render_template('infabout.html', d=d, b64=b64, flag=True)
    return render_template('infabout.html')



@app.route('/api/delete/<int:id>')
def api_de(id):
    db_operations.delete_product(id)
    return 'ok'





if __name__ == '__main__':
    dircr.creat_DIR_img()
    app.run(debug=True)
    dircr.del_DIR_img()