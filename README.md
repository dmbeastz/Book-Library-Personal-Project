 # Book Library Personal Project
 ### Author Dave Mutisya 

This project is a personal project to create a simple book library management system using Python. The goal of this project is to provide a basic understanding of how to create a simple database application using Python and to practice writing clean and efficient code.

### Prerequisites

To run this project, you will need the following:

* Python 3.10 
* A text editor (such as Visual Studio Code)
* A basic understanding of Python programming


### Getting Started

To get started, clone the repository to your local machine:

```
git clone git@github.com:dmbeastz/Book-Library-Personal-Project.git
```

Once the repository is cloned, open the `Book-Library-Personal-Project` folder in your text editor.

**Running the Application:**
To run the application, follow these steps:

1. **Install Dependencies:**
   Ensure that the necessary Python libraries are installed. You can do this by running the following command in your terminal:
   ```
   pipenv install
   ```
2. **Activate Virtual Environment:**
   ```
   pipenv shell
   ```

3. **Run the Application:**
   Navigate to the project directory and run the following command:
   ```
   python app/book_library.py
   ```
   This will start the application.

### Project Structure

The project is structured as follows:

* `book_library.py`: This is the main Python script that contains the code for the book library management system.

* `README.md`: This is the project README file that you are currently reading.

### Code Overview

The `book_library.py` script contains the following functions:

* `add_book()`: This function adds a new book to the library.
* `delete_book()`: This function deletes a book from the library.
* `edit_book()`: This function edits the details of a book in the library.
* `search_book()`: This function searches for a book in the library by title or author.
* `list_books()`: This function lists all the books in the library.

### Using the Project

To run the project, simply open the `python app/book_library.py` script in your text editor and click the "Run" button. The script will start running and will display a menu of options. You can select an option by entering the corresponding number and pressing Enter.

### Code Snippets

Here are some code snippets from the `book_library.py` script:

```python
# Add a new book to the library
def add_book():
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    isbn = input("Enter the ISBN of the book: ")

    
