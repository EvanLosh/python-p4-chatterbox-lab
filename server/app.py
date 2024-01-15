from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    response = None
    if request.method == 'GET':
        body = [message.to_dict() for message in Message.query.all()]
        response = make_response(jsonify(body),200)
    elif request.method == 'POST':
        body = request.get_json()["body"]
        username = request.get_json()["username"]
        new_message = Message(body = body, username = username)
        db.session.add(new_message)
        db.session.commit()
        response = make_response(new_message.to_dict(), 201)
    
    return response

@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def message_by_id(id):
    response = None
    message = Message.query.filter_by(id=id).first()

    if request.method == 'GET':
        response = make_response(jsonify(message),200)

    elif request.method == 'PATCH':
        setattr(message, "body", request.get_json()["body"])
        db.session.add(message)
        db.session.commit()
        response = make_response(message.to_dict(), 200)

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response = make_response(
            {},
            200
        )
    
    return response

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

if __name__ == '__main__':
    app.run(port=5555)
