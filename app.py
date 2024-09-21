from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/todo'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80),unique=True, nullable=False)

#Creating the database tables
with app.app.context():
    db.create_all()

# Helper functions for serialization
def serialize_todo(todo):
    return {
        'id': todo.id,
        'task': todo.task
    }

@app.route('/todos', methods=['POST'])
def add_todo():
    task = request.json['task']
    new_todo = Todo(task=task)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(serialize_todo(new_todo)), 201

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([serialize_todo(todo) for todo in todos]), 200