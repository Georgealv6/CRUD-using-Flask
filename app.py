from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Mytask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f"Task {self.id}"

with app.app_context():
        db.create_all()


@app.route("/", methods=["POST","GET"])
def index():
    #add a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = Mytask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
      #see all task
    else:
        tasks = Mytask.query.all()
        print(tasks)
        return render_template("index.html", tasks=tasks)



#Delete an item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = Mytask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"    

# Edit an item

@app.route("/update/<int:id>", methods=["POST","GET"])
def update(id:int):
    task = Mytask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"    
    else:
        return render_template('update.html', task=task)
    

if __name__ == "__main__":
    app.run(debug=True) 