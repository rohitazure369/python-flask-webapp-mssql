# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Define your variables
###############################################
server_url = "rk-vrit-mssql-server.database.windows.net"
db_name = "flask-webapp-db"
username = "sqladmin"
password = "Abcd123456789!"
###############################################

# Construct the SQLALCHEMY_DATABASE_URI using the variables
database_uri = f"mssql+pyodbc://{username}:{password}@{server_url}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"

# Assign the constructed URI to app.config
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
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
