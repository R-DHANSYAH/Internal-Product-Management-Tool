import os
from flask import Flask, request, render_template, redirect, url_for, flash
from models import db, InternalUser, Category, Attribute, Product, AttributeValue

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Ensure instance folder exists
if not os.path.exists('instance'):
    os.makedirs('instance')

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    if not InternalUser.query.first():
        demo_user = InternalUser(name="Admin", email="admin@example.com", role="category_manager")
        db.session.add(demo_user)
        db.session.commit()

def get_demo_user():
    return InternalUser.query.first()

# ---------------- CATEGORY ROUTES ----------------
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    categories = Category.query.paginate(page=page, per_page=5)
    return render_template('add_category.html', categories=categories)

@app.route('/add_category', methods=['POST'])
def add_category():
    name = request.form['name']
    description = request.form['description']
    user = get_demo_user()
    user.createCategory(name, description)
    flash("Category added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/edit_category/<int:id>', methods=['GET','POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method=='POST':
        category.name = request.form['name']
        category.description = request.form['description']
        db.session.commit()
        flash("Category updated!", "success")
        return redirect(url_for('index'))
    return render_template('edit_category.html', category=category)

@app.route('/delete_category/<int:id>')
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash("Category deleted!", "success")
    return redirect(url_for('index'))

# ---------------- ATTRIBUTE ROUTES ----------------
@app.route('/attributes')
def attributes():
    page = request.args.get('page', 1, type=int)
    attributes = Attribute.query.paginate(page=page, per_page=5)
    categories = Category.query.all()
    return render_template('add_attribute.html', existing_attributes=attributes, categories=categories)

@app.route('/add_attribute', methods=['POST'])
def add_attribute():
    name = request.form['name']
    data_type = request.form['data_type']
    category_id = request.form['category']
    category = Category.query.get(category_id)
    user = get_demo_user()
    user.createAttribute(name, data_type, category)
    flash("Attribute added successfully!", "success")
    return redirect(url_for('attributes'))

@app.route('/edit_attribute/<int:id>', methods=['GET','POST'])
def edit_attribute(id):
    attr = Attribute.query.get_or_404(id)
    categories = Category.query.all()
    if request.method=='POST':
        attr.name = request.form['name']
        attr.data_type = request.form['data_type']
        attr.category_id = request.form['category']
        db.session.commit()
        flash("Attribute updated!", "success")
        return redirect(url_for('attributes'))
    return render_template('edit_attribute.html', attribute=attr, categories=categories)

@app.route('/delete_attribute/<int:id>')
def delete_attribute(id):
    attr = Attribute.query.get_or_404(id)
    db.session.delete(attr)
    db.session.commit()
    flash("Attribute deleted!", "success")
    return redirect(url_for('attributes'))

# ---------------- PRODUCT ROUTES ----------------
@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=5)
    categories = Category.query.all()
    return render_template('add_product.html', products=products, categories=categories)

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = float(request.form['price'])
    stock = int(request.form['stock'])
    category_id = request.form['category']
    category = Category.query.get(category_id)
    user = get_demo_user()
    user.createProduct(name, price, category, stock)
    flash("Product added successfully!", "success")
    return redirect(url_for('products'))

@app.route('/edit_product/<int:id>', methods=['GET','POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    categories = Category.query.all()
    if request.method=='POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.category_id = request.form['category']
        db.session.commit()
        flash("Product updated!", "success")
        return redirect(url_for('products'))
    return render_template('edit_product.html', product=product, categories=categories)

@app.route('/delete_product/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted!", "success")
    return redirect(url_for('products'))

# ---------------- ATTRIBUTE VALUE ROUTES ----------------
@app.route('/values')
def values():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    all_products = Product.query.paginate(page=page, per_page=per_page)
    return render_template('assign_values.html', products=all_products)

@app.route('/assign_value', methods=['POST'])
def assign_value():
    product_id = int(request.form['product'])
    
    # handle multiple attributes per product
    for key, value_text in request.form.items():
        if key.startswith("value_"):
            attribute_id = int(key.split("_")[1])
            if value_text.strip():
                existing = AttributeValue.query.filter_by(product_id=product_id, attribute_id=attribute_id).first()
                if existing:
                    existing.value = value_text
                else:
                    attr_value = AttributeValue(product_id=product_id, attribute_id=attribute_id, value=value_text)
                    db.session.add(attr_value)
    db.session.commit()
    flash("Attribute values saved successfully!", "success")
    return redirect(url_for('values'))

if __name__ == "__main__":
    app.run(debug=True)
