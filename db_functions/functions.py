from db_functions import *

def create_author(author_name, self_commit=True):
    a = Author(name=author_name)
    db.session.add(a)
    if self_commit:
        db.session.commit()
    return a

def create_book(title, author, amount, isbn, category, price, rating, format, online_picture_route, local_picture_route=None, self_commit=False):
    if isinstance(author, str):
        author = create_author(author, self_commit=False)
        
    b = Book(
        title=title, 
        author=author,
        amount_total=amount,
        amount_available=amount,
        isbn=isbn,
        category=category,
        price=price,
        rating=rating,
        format=format,
        online_picture_route=online_picture_route,
        local_picture_route=local_picture_route,
        )
    db.session.add(b)
    db.session.commit()
    return b


