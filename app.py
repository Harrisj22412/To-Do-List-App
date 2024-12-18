from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/todo'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/todo'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    done = db.Column(db.Boolean, default=False)

#Creating the database tables
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# Helper functions for serialization
def serialize_todo(todo):
    return {
        'id': todo.id,
        'task': todo.task
    }

#Endpoint to add a new todo
@app.route('/todos', methods=['POST'])
def add_todo():
    task = request.json['task']
    new_todo = Todo(task=task)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(serialize_todo(new_todo)), 201

# Endpoint to get all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([serialize_todo(todo) for todo in todos]), 200

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': f'Todo with id {id} deleted successfully'}), 200