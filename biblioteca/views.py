from flask_admin.base import AdminIndexView
from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from biblioteca import db
from biblioteca.models import *

class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        book_amount = len(Book.query.all())
        current_loans = len(Loan.query.filter(not Loan.returned).all())
        unavailable_books = len(Book.query.filter(Book.amount_available == 0).all())
        return self.render('admin/index.html', b_amt=book_amount, current_loans=current_loans, unavailable_books=unavailable_books)

class BookView(ModelView):
    column_list = ('author_name', 'title', 'isbn', 'amount_total', 'amount_available', 'format', 'category')
    column_searchable_list = ['title', 'isbn']
    column_filters = ['author']
    column_labels = {
        'author_name': 'Autor',
        'title': 'Título',
        'amount_total': 'Cantidad ejemplares',
        'amount_available': 'Ejemplares disponibles',
        'isbn': 'ISBN',
        'category': 'Categoría',
        'rating': 'Calificación',
        'format': 'Formato'
    }
    page_size = 30

class LoanView(ModelView):
    column_filters = ['returned', 'loaner']
    column_list = ('loaner_document', 'loaned_book', 'takeout_date', 'returned')
    can_create = False
    can_delete = False
    column_labels = {
        'loaner_document': 'Documento del prestante',
        'loaned_book': 'Libro prestado',
        'takeout_date': 'Fecha de prestamo',
        'returned': 'Prestamo retornado'
    }