from flask import Flask, render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#Initialise Flask application
app = Flask(__name__)

#Configure SQLAlchemy to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialise SQLAlchemy with the Flask application
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

#Define route for homepage
@app.route('/')
def index():
    
    #Query all todo items from the database
    todo_list = Todo.query.all()
    print(todo_list)
    
    #Render the template with the todo list
    return render_template('base.html', todo_list=todo_list)

#Define route for adding a new todo item
@app.route("/add", methods=["POST"])
def add():
    #Get the title of the new todo from the form submitted via POST request
    title = request.form.get("title")
    
    #Create a new Todo object with the received title and set 'complete' to False
    new_todo = Todo(title=title, complete=False)
    
    #Add the new todo object to the database session
    db.session.add(new_todo)
    
    #Commit the changes to the database
    db.session.commit()
    
    #Redirect to the homepage after adding the new todo
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("index"))
    
#Run the Flask application when this script is executed directly
if __name__ == "__main__":
    with app.app_context():
        # Create the database tables
        db.create_all()
    
    
    app.run(debug=True)


    