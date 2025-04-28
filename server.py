from flask import Flask, request, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy

# Inicijalizacija Flask aplikacije
app = Flask(__name__)

# Konfiguracija putanje do SQLite baze podataka
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

# Inicijalizacija SQLAlchemy objekta
db = SQLAlchemy(app)

# Definicija modela Todo
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Todo %r>' % self.title

# Prikaz početne stranice
@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')

# Dobavljanje svih todos-a
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todos_list = [{'id': todo.id, 'title': todo.title, 'completed': todo.completed} for todo in todos]
    return jsonify({'todos': todos_list})

# Kreiranje novog zadatka
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    if 'title' not in data:
        abort(400, 'Title is required')
    title = data['title']
    todo = Todo(title=title)
    db.session.add(todo)
    db.session.commit()
    return jsonify({'message': 'Todo created successfully'}), 201

# Ažuriranje postojećeg zadatka
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = db.session.get(Todo, todo_id)
    if not todo:
        abort(404, 'Todo not found')
    data = request.json
    if 'title' in data:
        todo.title = data['title']
    if 'completed' in data:
        todo.completed = data['completed']
    db.session.commit()
    return jsonify({'message': 'Todo updated successfully'})

# Brisanje određenog zadatka
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = db.session.get(Todo, todo_id)
    if not todo:
        abort(404, 'Todo not found')
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})

# Pokretanje aplikacije
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
