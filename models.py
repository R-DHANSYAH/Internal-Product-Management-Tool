from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class InternalUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    role = db.Column(db.String(50))

    def createCategory(self, name, description):
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()

    def createAttribute(self, name, data_type, category):
        attr = Attribute(name=name, data_type=data_type, category=category)
        db.session.add(attr)
        db.session.commit()

    def createProduct(self, name, price, category, stock):
        prod = Product(name=name, price=price, category=category, stock=stock)
        db.session.add(prod)
        db.session.commit()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    attributes = db.relationship('Attribute', backref='category', lazy=True)
    products = db.relationship('Product', backref='category', lazy=True)

class Attribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    data_type = db.Column(db.String(20))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    attribute_values = db.relationship('AttributeValue', backref='product', lazy=True)

class AttributeValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    attribute_id = db.Column(db.Integer, db.ForeignKey('attribute.id'))
    value = db.Column(db.String(50))
