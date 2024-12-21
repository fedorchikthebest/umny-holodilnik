from flask import Flask, render_template, request, redirect, url_for, jsonify
import db_operations

app = Flask(__name__)

# Список для хранения товаров (можно позже заменить на базу данных)
products = []

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route("/add", methods=['GET', 'POST'])
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

@app.route('/api')
def api():
    return jsonify(db_operations.get_products())



from flask import Flask, render_template, request

app = Flask(__name__)

# Главная страница с формой
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Получаем данные из формы
    product_name = request.form.get('product_name')
    product_class = request.form.get('product_class')
    category = request.form.get('category')
    manufacture_date = request.form.get('manufacture_date')
    expiry_date = request.form.get('expiry_date')
    weight = request.form.get('weight')
    volume = request.form.get('volume')
    proteins = request.form.get('proteins')
    fats = request.form.get('fats')
    carbs = request.form.get('carbs')

    print(f"Название продукта: {product_name}")
    print(f"Класс: {product_class}")
    print(f"Категория: {category}")
    print(f"Дата изготовления: {manufacture_date}")
    print(f"Дата истечения: {expiry_date}")
    print(f"Масса кг: {weight}")
    print(f"Объём л: {volume}")
    print(f"Белки г: {proteins}")
    print(f"Жиры г: {fats}")
    print(f"Углеводы г: {carbs}")

    return 'Форма успешно отправлена!'

if __name__ == '__main__':
    app.run(debug=True)







if __name__ == '__main__':
    app.run(debug=True)
