from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.book_library import Base, Author, Book
from datetime import datetime, date

def seed_data():
    engine = create_engine('sqlite:///book_library.db')

    Base.metadata.bind = engine

    Session = sessionmaker(bind=engine)
    session = Session()

    author1 = Author(
        first_name="Jack",
        last_name="Canfield",
        birth_date=date(1944, 8, 19),
        nationality="American"
    )

    author2 = Author(
        first_name="Mark",
        last_name="Crutcher",
        birth_date=date(1969, 9, 10),
        nationality="British"
    )

    session.add_all([author1, author2])
    session.commit()

    book1 = Book(
        title="The Lightning Thief",
        isbn="0553497448",
        publication_year=1990,  # Corrected the data type to integer
        genre="Fiction",
        read_status=False,  # Assuming it hasn't been read yet
        author=author1  # Assigning the author to the book
    )

    book2 = Book(
        title="The one who laughs",
        isbn="1234567890",
        publication_year=2005,
        genre="Non-Fiction",
        read_status=True,  # Assuming this book has been read
        author=author2
    )

    session.add_all([book1, book2])
    session.commit()

    print("Sample data added to the database.")
    
if __name__ == '__main__':
    seed_data()
