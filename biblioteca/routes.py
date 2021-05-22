from flask import request, render_template, redirect, url_for, flash
from biblioteca import app
from biblioteca.models import *
from biblioteca.forms import *
from biblioteca.crypt import hash, dehash


@app.route('/')
def home():
    flash("Hola Mundo", "Notoficación!")
    return render_template('index.html')


@app.route("/books")
def books():
    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page=page, per_page=5)
    return render_template("books.html", books=books)


@app.route("/author/<author_name>")
def author_page(author_name):
    author = Author.query.filter(Author.name == author_name).first()
    if author:
        page = request.args.get('page', 1, type=int)
        books = Book.query.filter(Book.author == author).paginate(page=page, per_page=5)
        return render_template("author.html", author=author, books=books)
    
    
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


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        
        pw_hash = hash(form.pw.data)
        
        u = User.registerUser(
            form.fname.data,
            form.lname.data,
            form.email.data,
            pw_hash,
            form.phone.data
        )
        
        
        return redirect(url_for('home'))
    
    
    return render_template("register.html", form=form)

@app.route('/user')
def user():
    return render_template('user.html')