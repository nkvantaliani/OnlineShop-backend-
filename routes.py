from itertools import product
from os import path
from flask import render_template, redirect,session
from flask_login import login_user, logout_user, current_user, login_required

from ext import app,db
from forms import RegisterForm, ProductForm, LoginForm
from models import Product, User

from uuid import uuid4

@app.route('/')
def index():
    products = Product.query.all()
    user_role = session.get('role', 'user')
    return render_template("index.html",products=products,user_role=user_role)



@app.route('/create', methods=["GET", "POST"])
def create():
    form = ProductForm()
    user_role = session.get('role', 'user')
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data)
        image = form.img.data
        image_extension = image.filename.split('.')[-1].lower()
        random_image_name = str(uuid4()) + '.' + image_extension
        directory = path.join(app.root_path, "static", "images", random_image_name)
        image.save(directory)
        new_product.img = random_image_name
        new_product.save()
        return redirect("/")
    return render_template("create.html",form=form, user_role=user_role)


@app.route('/login',methods=["GET", "POST"])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user =User.query.filter(User.username == username).first()
        if user and user.password == password:
            login_user(user)

            if username == 'admin':
                session['role'] = 'admin'
            else:
                session['role'] = 'user'
            return redirect('/')
        else:
            return render_template("login.html",form=form, is_incorrect='true')

    return render_template("login.html",form=form, is_incorrect='false')

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect ('/')

@app.route('/contact')
def contact():
    user_role = session.get('role', 'user')
    return render_template("contact.html", user_role=user_role)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    user_role = session.get('role', 'user')

    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        new_user.save()
        return redirect('/login')

    return render_template("register.html", form=form, user_role=user_role)

@app.route('/product_details/<int:product_id>')
def product_details(product_id):
    product = Product.query.get(product_id)
    user_role = session.get('role', 'user')
    return render_template("product_details.html", product=product, user_role=user_role)

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/')

@app.route('/edit_product/<int:product_id>', methods=["GET", "POST"])
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price)
    if form.validate_on_submit():
        db.session.commit()

        product.name = form.name.data
        product.price = form.price.data
        image = form.img.data
        image_extension = image.filename.split('.')[-1].lower()
        random_image_name = str(uuid4()) + '.' + image_extension
        directory = path.join(app.root_path, "static", "images", random_image_name)
        image.save(directory)
        product.img = random_image_name
        product.save()
        return redirect("/")
    return render_template("create.html", form=form)

@app.route("/bought")
def bought():
    return render_template("bought.html")

