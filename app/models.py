from sqlalchemy import create_engine, Column, Integer, String , Date, ForeignKey,Boolean
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
    else:
        click.echo("No books found.")

if __name__ == '__main__':
    cli()
