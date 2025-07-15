
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qalbi.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

@app.route("/admin")
def admin():
    posts = Post.query.all()
    return render_template("admin.html", posts=posts)

@app.route("/admin/init")
def init_db():
    db.create_all()
    return "✅ Database created successfully!"

@app.route("/admin/add", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/")
    return render_template("add_post.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
