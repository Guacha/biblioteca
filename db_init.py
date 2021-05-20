import csv
import math, random
from db_functions import db
from db_functions.functions import *

db.create_all()

with open("main_dataset.csv") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    total_count = 0
    added_count = 0
    for row in csvreader:
        if total_count == 0:
            pass # Faire rien
        else:
            online_picture_route = row[0]
            book_name = "N/A" if row[1] == "" else row[1]
            author_name = "N/A" if row[2] == "" else row[2]
            book_format = "Poster/Stationary" if row[3] == "" else row[3]
            book_rating = float(row[4])
            try:
                book_price = math.ceil((float(row[5])*3000)/1000)*1000
            except ValueError:
                book_price = math.ceil((float(row[5][3:])*3000)/100)*100
            book_isbn = row[8]
            book_category = row[9]
            book_img_path = row[10]
            
            book = db.session.query(Book).filter((Book.isbn == book_isbn) | ((Book.format == book_format) & (Book.title == book_name))).first()
            
            if book is None:
                author = db.session.query(Author).filter(Author.name == author_name).first()
                if author:
                    book = create_book(
                        book_name,
                        author,
                        random.randint(1, 10),
                        book_isbn,
                        book_category,
                        book_price,
                        book_rating,
                        book_format,
                        online_picture_route,
                        local_picture_route=book_img_path
                    )
                else:
                    book = create_book(
                        book_name,
                        author_name,
                        random.randint(1, 10),
                        book_isbn,
                        book_category,
                        book_price,
                        book_rating,
                        book_format,
                        online_picture_route,
                        local_picture_route=book_img_path
                    )
            
                print(f"Added Book: {book}")
                added_count += 1
            else:
                print(f"Skipping over existing book: {book}")
                
        total_count += 1
            
        
        
print(f"Processed books: {total_count}")
print(f"Skipped over books (Repeats): {total_count-added_count} ({(total_count-added_count)/total_count*100}%)")
db.session.commit()
