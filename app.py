from flask import Flask, render_template, abort, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/{}'.format(app.root_path, 'auction.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'b2de7FkqvkMyqzNFzxCkgnPKIGP6i4Rc'

db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.Text, nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('Product', lazy=True))
    title = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(100), nullable=False)

db.create_all()

# categories = {
#     "collectables": {
#         "products": [{
#             "title": "Honus Wagner - 2009 Topps (PSA GEM MT 10)",
#             "img": "img/card.jpg",
#             "description": "2009 TOPPS T-206 HONUS WAGNER PSA GEM MT 10. Shipped with USPS First Class.",
#             "price": "$259,000.00",
#         },],
#         "title": "Collectibles & Art",
#         "subtitle": "Discover coins, stamps, comics, and more.",
#         "route": "collectables",
#     },
#     "electronics": {
#         "products": [{}],
#         "title": "Electronics",
#         "subtitle": "Discover computers, cameras, TVs, and more.",
#         "route": "electronics",
#     },
# }

@app.route("/")
def index():
    categories = Category.query.all()
    return render_template("index.html", categories=categories)

@app.route("/category/<name>")
def category(name):
    category = Category.query.filter(Category.name == name).first()
    products = Product.query.join(Category).filter(Category.name == name)
    return render_template("category.html", category=category, products=products)

@app.route("/<category>/product/<int:id>")
def product(category, id):
    product = Product.query.get(id)
    return render_template("product.html", product=product)

@app.route('/admin')
@app.route('/admin/categories')
def admin_categories():
    categories = Category.query.all()
    return render_template('admin/category.html', categories=categories)

@app.route('/admin/products')
def admin_products():
    return render_template("admin/product.html", product=product)

@app.route('/admin/create/category', methods=('GET', 'POST'))
def create_category():
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        subtitle = request.form['subtitle']

        error = None
        
        if not name:
            error = 'Name is required.'
            
        if error is None:
            category = Category(name=name, title=title, subtitle=subtitle)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('admin_categories'))
    
        flash(error)

    categories = Category.query.all()
    return render_template('admin/category_form.html', categories=categories)

@app.route('/admin/edit/category/<id>', methods=('GET', 'POST'))
def edit_category(id):
    category = Category.query.get_or_404(id)

    if request.method == 'POST':
        category.name = request.form['name']
        category.title = request.form['title']
        category.subtitle = request.form['subtitle']

        error = None
        
        if not request.form['name']:
            error = 'Name is required.'
            
        if error is None:
            db.session.commit()
            return redirect(url_for('admin_categories'))
    
        flash(error)

    return render_template('admin/category_form.html', name=category.name, title=category.title, subtitle=category.subtitle)
