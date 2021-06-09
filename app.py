from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    sr_No = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False )
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sr_No} - {self.title} "


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    allTodo = ToDo.query.all()
    return render_template('index.html', alltodo=allTodo)

@app.route('/Delete/<int:sr_No>')
def Delete(sr_No):
    todo = ToDo.query.filter_by(sr_No=sr_No).first()
    db.session.delete(todo)
    db.session.commit() 
    return redirect("/")


@app.route('/Update/<int:sr_No>', methods=['GET', 'POST'])
def Update(sr_No):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(sr_No=sr_No).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/") 

    todo = ToDo.query.filter_by(sr_No=sr_No).first()
    return render_template('update.html', todo=todo)      

if __name__ == "__main__":
    app.run(debug=True, port=2607)
    