import os
from typing import List
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app: Flask = Flask(__name__)

app.config['SECRET_KEY']                  = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI']     = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db: SQLAlchemy = SQLAlchemy(app)
Migrate(app, db)


class Task(db.Model):
    __tablename__ = 'tasks'

    id:           int  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content:      str  = db.Column(db.String(200), nullable=False)
    is_completed: bool = db.Column(db.Boolean, default=False)

    def __str__(self) -> str:
        return f'Task(id={self.id}, content={self.content}, done={self.is_completed})'


@app.route('/')
def index() -> str:
    uncompleted: List[Task] = Task.query.filter_by(is_completed=False).all()
    completed:   List[Task] = Task.query.filter_by(is_completed=True).all()
    return render_template('index.html', uncompleted_tasks=uncompleted, completed_tasks=completed)


@app.route('/new', methods=['GET', 'POST'])
def new_task() -> str:
    if request.method == 'POST':
        task = Task(content=request.form['content'])
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_task.html')


@app.route('/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id: int) -> str:
    task = Task.query.get(task_id)
    task.is_completed = True
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/tasks/<int:task_id>/uncompleted', methods=['POST'])
def uncompleted_task(task_id: int) -> str:
    task = Task.query.get(task_id)
    task.is_completed = False
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5038)
