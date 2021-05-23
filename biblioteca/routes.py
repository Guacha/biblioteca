from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, current_user

from biblioteca import app
from biblioteca.models import *
from biblioteca.forms import *
from biblioteca.crypt import hash, dehash


@app.route('/')
def home():
    return render_template('index.html')
    
    
@app.route("/search", methods=["POST"])
def search():
    if "simple_search" in request.form:
        if request.form["simple_search"] == "":
            return redirect(url_for('home'))
        else:
            return redirect(url_for('results', title=request.form["simple_search"]))
    else:
        
        return redirect(url_for('results', title=request.form["title"], author=request.form["author"], isbn=request.form["isbn"]))
        

@app.route("/results")
def results():
    page = request.args.get('page', 1, type=int)
    params = ""
    books = db.session.query(Book)
    if not request.args.get("title", "") == "":
        books = books.filter(Book.title.ilike(f"%{request.args['title']}%"))
        params += f"- Nombre: {request.args['title']} "
    
    if not request.args.get("author", "") == "":
        books = books.join(Author).filter(Author.name.ilike(f"%{request.args['author']}%"))
        params += f"- Autor: {request.args['author']} "
    
    if not request.args.get("isbn", "") == "":
        books = books.filter(Book.isbn == request.args["isbn"])
        params += f"- ISBN: {request.args['author']} "
    
    if len(books.all()) == 0:
        books = None
    else:
        books = books.paginate(page=page, per_page=12)
    return render_template("results.html", books=books, search_params=params)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        u = db.session.query(User).filter_by(num_id=form.num_doc.data).first()
        if u:
            login_user(u)
            flash(f"Bienvenido, {u.fname}", "Inicio de sesión correcto")
            return redirect(url_for("home"))
        else:
            flash("Revisa los datos ingresados, e intenta nuevamente", "Error de inicio de sesión")
    
    return render_template("login.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegisterForm()
    if form.validate_on_submit():
        
        pw_hash = hash(form.pw.data)
        
        u = User.registerUser(
            form.num_doc.data,
            form.fname.data,
            form.lname.data,
            form.email.data,
            pw_hash,
            form.phone.data
        )
        login_user(u)
        flash(f"Cuenta para {form.fname.data} creada satisfactoriamente", "Éxito")
        
        return redirect(url_for('home'))
    
    print(form.fname.errors)
    flash("Información inválida, intenta nuevamente", "Error")
    return render_template("register.html", form=form)

@app.route('/user')
def user():
    return render_template('user.html')