from flask import Blueprint, request

from src.api.utils.responses import response_with
from src.api.utils import responses as resp
from src.api.utils.database import db
from src.api.models.book import Book, BookSchema

book_routes = Blueprint("book_routes", __name__)

# POST new books
@book_routes.route('/', methods=['POST'])
def create_book():
    try:
        data = request.get_json()
        book_schema = BookSchema()
        book = book_schema.load(data)
        result = book_schema.dump(book.create())

        return response_with(resp.SUCCESS_201, value={"book": result})
    except Exception as error:
        print(e)

        return response_with(resp.INVALID_INPUT_422)

# GET books list
@book_routes.route('/', methods=['GET'])
def get_books_list():
    fetched_books = Book.query.all()
    book_schema = BookSchema(many=True)
    books = book_schema.dump(fetched_books)

    return response_with(resp.SUCCESS_200, value={"books": books})

# GET a book
@book_routes.route('/<int:book_id>', methods=['GET'])
def get_book_detail(book_id):
    fetched_book = Book.query.get_or_404(book_id)
    book_schema = BookSchema()
    book = book_schema.dump(fetched_book)

    return response_with(resp.SUCCESS_200, value={"book": book})

# PUT current book's data
# @book_routes.route('/<int:book_id>', methods=['PUT'])
# def update_book_detail(book_id):
#     data = request.get_json()
#     get_book = Book.query.get_or_404(book_id)
#     get_book.title = data['title']
#     get_book.year = data['year']

#     db.session.add(get_book)
#     db.session.commit()

#     book_schema = BookSchema()
#     book = book_schema.dump(get_book)
    