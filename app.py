# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace 'your_db_name' with your actual database name
# rk-vrit-sql-server.database.windows.net
# rk-vrit-python-web-app-db
# sqladmin
# Abcd123456789!



app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sqladmin:Abcd123456789!@rk-vrit-sql-server.database.windows.net/rk-vrit-python-web-app-db?driver=SQL+Server+Native+Client+11.0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)