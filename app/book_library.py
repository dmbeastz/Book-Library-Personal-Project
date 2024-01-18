from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
import datetime
import click

engine = create_engine('sqlite:///book_library.db')
Base = declarative_base()
Base.metadata.bind = engine


class Author(Base):
    __tablename__ = 'authors'
    author_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date)
    nationality = Column(String)

    # Establishing a one-to-many relationship with books
    books = relationship('Book', back_populates='author')


class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.author_id'), nullable=False)
    publication_year = Column(Integer)
    isbn = Column(String, unique=True)
    genre = Column(String)
    read_status = Column(Boolean, default=False)

    # Establishing a many-to-one relationship with authors
    author = relationship('Author', back_populates='books')


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


@click.group()
def cli():
    pass


@cli.command()
def main_menu():
    while True:
        click.echo("Book Library Management System")
        click.echo("1. Add Author")
        click.echo("2. Delete Author")
        click.echo("3. List Authors")
        click.echo("4. Search Author")
        click.echo("5. Add Book")
        click.echo("6. Delete Book")
        click.echo("7. List Books")
        click.echo("8. Search Book")
        click.echo("9. Exit")

        choice = click.prompt("Enter your choice (1-9)", type=int)

        if choice == 1:
            add_author()
        elif choice == 2:
            delete_author()
        elif choice == 3:
            list_authors()
        elif choice == 4:
            search_author_menu()
        elif choice == 5:
            add_book()
        elif choice == 6:
            delete_book()
        elif choice == 7:
            list_books()
        elif choice == 8:
            search_book_menu()
        elif choice == 9:
            click.echo("Exiting. Goodbye!")
            break
        else:
            click.echo("Invalid choice. Please enter a number between 1 and 9.")


def search_author_menu():
    click.echo("Search Author Options:")
    click.echo("1. Search by First Name")
    click.echo("2. Search by Last Name")
    click.echo("3. Back to Main Menu")

    choice = click.prompt("Enter your choice (1-3)", type=int)

    if choice == 1:
        first_name = click.prompt("Enter the first name to search")
        search_author(first_name=first_name)
    elif choice == 2:
        last_name = click.prompt("Enter the last name to search")
        search_author(last_name=last_name)
    elif choice == 3:
        click.echo("Returning to the main menu.")
    else:
        click.echo("Invalid choice. Please enter a number between 1 and 3.")


def search_book_menu():
    click.echo("Search Book Options:")
    click.echo("1. Search by Title")
    click.echo("2. Search by Publication Year")
    click.echo("3. Back to Main Menu")

    choice = click.prompt("Enter your choice (1-3)", type=int)

    if choice == 1:
        title = click.prompt("Enter the title to search")
        search_book(title=title)
    elif choice == 2:
        publication_year = click.prompt("Enter the publication year to search", type=int)
        search_book(publication_year=publication_year)
    elif choice == 3:
        click.echo("Returning to the main menu.")
    else:
        click.echo("Invalid choice. Please enter a number between 1 and 3.")


def search_author(first_name=None, last_name=None):
    query = session.query(Author)

    if first_name:
        query = query.filter(Author.first_name.ilike(f'%{first_name}%'))

    if last_name:
        query = query.filter(Author.last_name.ilike(f'%{last_name}%'))

    authors = query.all()

    if authors:
        click.echo("List of Matching Authors:")
        for author in authors:
            click.echo(f"{author.author_id}. {author.first_name} {author.last_name}")
    else:
        click.echo("No matching authors found.")


def search_book(title=None, publication_year=None):
    query = session.query(Book)

    if title:
        query = query.filter(Book.title.ilike(f'%{title}%'))

    if publication_year:
        query = query.filter(Book.publication_year == publication_year)

    books = query.all()

    if books:
        click.echo("List of Matching Books:")
        for book in books:
            click.echo(f"{book.book_id}. {book.title} - {book.author.first_name} {book.author.last_name}")
    else:
        click.echo("No matching books found.")


@cli.command()
@click.option('--first-name', prompt='First Name', help='First name of the author.')
@click.option('--last-name', prompt='Last Name', help='Last name of the author.')
@click.option('--birth-date', prompt='Birth Date', type=click.DateTime(formats=['%Y-%m-%d']), help='Birth date of the author (YYYY-MM-DD).')
@click.option('--nationality', prompt='Nationality', help='Nationality of the author.')
def add_author(first_name, last_name, birth_date, nationality):
    author = Author(
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        nationality=nationality
    )
    session.add(author)
    session.commit()
    click.echo(f"Author {first_name} {last_name} added successfully.")

@cli.command()
@click.option('--id', prompt='Author ID', type=int, help='ID of the author to delete.')
def delete_author(id):
    author = session.query(Author).get(id)
    if author:
        session.delete(author)
        session.commit()
        click.echo(f"Author with ID {id} deleted successfully.")
    else:
        click.echo(f"No author found with ID {id}.")

@cli.command()
def list_authors():
    authors = session.query(Author).all()
    if authors:
        click.echo("List of Authors:")
        for author in authors:
            click.echo(f"{author.author_id}. {author.first_name} {author.last_name}")
    else:
        click.echo("No authors found.")


@cli.command()
@click.option('--title', prompt='Title', help='Title of the book.')
@click.option('--isbn', prompt='ISBN', help='International Standard Book Number of the book.')
@click.option('--publication-year', prompt='Publication Year', type=int, help='Year the book was published.')
@click.option('--genre', prompt='Genre', help='Genre of the book.')
@click.option('--read-status', prompt='Read Status', type=click.BOOL, default=False, help='Read status of the book.')
@click.option('--author-id', prompt='Author ID', type=int, help='ID of the author of the book.')
def add_book(title, isbn, publication_year, genre, read_status, author_id):
    author = session.get(Author, author_id)
    if author:
        book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            genre=genre,
            read_status=read_status,
            author=author
        )
        session.add(book)
        session.commit()
        click.echo(f"Book '{title}' added successfully.")
    else:
        click.echo(f"No author found with ID {author_id}.")


@cli.command()
@click.option('--id', prompt='Book ID', type=int, help='ID of the book to delete.')
def delete_book(id):
    book = session.query(Book).get(id)
    if book:
        session.delete(book)
        session.commit()
        click.echo(f"Book with ID {id} deleted successfully.")
    else:
        click.echo(f"No book found with ID {id}.")

@cli.command()
def list_books():
    books = session.query(Book).all()
    if books:
        click.echo("List of Books:")
        for book in books:
            click.echo(f"{book.book_id}. {book.title} - {book.author.first_name} {book.author.last_name}")
            click.echo(f"   Genre: {book.genre}")
            click.echo(f"   Read Status: {'Read' if book.read_status else 'Not Read'}")
    else:
        click.echo("No books found.")

if __name__ == '__main__':
    main_menu()