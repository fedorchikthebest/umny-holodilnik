from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Список для хранения товаров (можно позже заменить на базу данных)
products = []


@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        
        product = {
            'name': name,
            'price': price,
            'description': description
        }
        products.append(product)
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/korzina')
def korzina():
    return render_template('korzina.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
