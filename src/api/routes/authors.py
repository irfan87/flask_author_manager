from flask import Blueprint, request

from src.api.utils.database import db
from src.api.utils.responses import response_with
from src.api.utils import responses as resp
from src.api.models.author import Author, AuthorSchema

author_routes = Blueprint('author_routes', __name__)

# POST new author
@author_routes.route('/', methods=['POST'])
def create_author():
    try:
        data = request.get_json()
        author_schema = AuthorSchema()
        author = author_schema.load(data)
        result = author_schema.dump(author.create())
        
        return response_with(resp.SUCCESS_201, value={"author": result})
    except Exception as error:
        print(error)

        return response_with(resp.INVALID_INPUT_422)

# GET authors list
@author_routes.route('/', methods=['GET'])
def get_authors():
    fetched_authors = Author.query.all()
    author_schema = AuthorSchema(many=True)
    authors = author_schema.dump(fetched_authors)

    return response_with(resp.SUCCESS_200, value={"authors": authors})

# GET an author
@author_routes.route('/<int:author_id>', methods=['GET'])
def get_authors_by_id(author_id):
    fetched_author = Author.query.get_or_404(author_id)
    author_schema = AuthorSchema()
    author = author_schema.dump(fetched_author)

    return response_with(resp.SUCCESS_200, value={"author": author})

# PUT all data of current author
@author_routes.route('/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    # get author id from json
    data = request.get_json()
    get_author = Author.query.get_or_404(author_id)
    get_author.first_name = data['first_name']
    get_author.last_name = data['last_name']

    db.session.add(get_author)
    db.session.commit()

    # dump up the schema
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)

    return response_with(resp.SUCCESS_200, value={"author": author})

# PATCH one of the author's data that need to be changed
@author_routes.route('/<int:author_id>', methods=['PATCH'])
def modify_author(author_id):
    data = request.get_json()
    get_author = Author.query.get_or_404(author_id)

    if data.get('first_name'):
        get_author.first_name = data['first_name']

    if data.get('last_name'):
        get_author.last_name = data['last_name']

    db.session.add(get_author)
    db.session.commit()

    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)

    return response_with(resp.SUCCESS_200, value={"author": author})

# DELETE the unwanted or anonymous author
@author_routes.route('/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    get_author = Author.query.get_or_404(author_id)
    
    db.session.delete(get_author)
    db.session.commit()

    return response_with(resp.SUCCESS_204)