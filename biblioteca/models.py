from datetime import date

from sqlalchemy.sql.expression import column
from flask_login import UserMixin

from biblioteca import db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

relacion_usuario_favoritos = db.Table(
    'usuario_favoritos',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
)
class Book(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", back_populates="books_written")
    amount_total = db.Column(db.Integer, nullable=False)
    amount_available = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(15), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    rating = db.Column(db.Float(), nullable=False)
    local_picture_route = db.Column(db.String(128))
    online_picture_route = db.Column(db.String(255))
    format = db.Column(db.String(50), nullable=False)
    loans = db.relationship("Loan", back_populates="loaned_book")
    users_liked = db.relationship("User", secondary=relacion_usuario_favoritos, back_populates="liked_books")
    
    @property
    def author_name(self):
        return self.author.name
    
    def __repr__(self):
        return f"<Book: {self.title} by {self.author.name}>"
    

class Author(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    books_written = db.relationship("Book", back_populates="author")
    
    def __repr__(self):
        return f"<Author: {self.name}>"
    
    @property
    def amount_books_written(self):
        return len(self.books_written)
   
        
class Loan(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    loan_code = db.Column(db.String(8), nullable=False, unique=True)
    loaner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    loaner = db.relationship("User", back_populates="loans")
    loaned_book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    loaned_book = db.relationship("Book", back_populates="loans")
    takeout_date = db.Column(db.Date, nullable=False)
    returned = db.Column(db.Boolean(), default=False)
    return_date = db.Column(db.Date)
    
    
    @property
    def loaner_document(self):
        return self.loaner.num_id
    

class User(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key=True)
    num_id = db.Column(db.BigInteger, nullable=False, unique=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.BigInteger)
    password = db.Column(db.String(90), nullable=False)
    loans = db.relationship("Loan", back_populates="loaner")
    liked_books = db.relationship("Book", secondary=relacion_usuario_favoritos, back_populates="users_liked")
    
    @property
    def current_loans(self):
        return [loan for loan in self.loans if not loan.returned]
    
    @staticmethod
    def registerUser(num_id: int, fname: str, lname: str, email: str, password: str, phone: int = None):
        u = User(num_id=num_id, fname=fname, lname=lname, email=email, password=password, phone=phone)
        db.session.add(u)
        db.session.commit()
        return u
    
        

class Employee(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    numdoc = db.Column(db.Integer, nullable=False)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(90), nullable=False)
    
    
    

    
    
    