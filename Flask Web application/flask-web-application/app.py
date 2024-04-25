from flask import Flask, render_template, redirect,request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#Configurations
app = Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db = SQLAlchemy(app)

#Create model
class Task(db.Model):
    #Class Variables
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(60), nullable = False)
    completed = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"

@app.route('/', methods=["GET","POST"])
def index():
    #send in to db
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Task(content = task_content)
        try:
        #Create 
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
        
    else:
        tasks = Task.query.order_by(Task.date).all()
        return render_template('index.html',tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id: int):
    task_to_delete = Task.query.get_or_404(id)
    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"

@app.route("/edit/<int:id>", methods=["GET","POST"])
def update(id: int):
    task = Task.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try: 
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template("edit.html",task=task)
    




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)