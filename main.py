from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:brockman80@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    

    def __init__(self, title, body):
        self.title = title
        self.body = body
        

#class User(db.Model):

    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(120))
    #blogs = db.relationship('Blog', backref='owner')

    #def __init__(self, name):
        #self.name = name


@app.route("/newpost", methods=["POST", "GET"])
def newpost():

    if request.method == "POST":
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        title_error = ""
        body_error = ""

        if '' == blog_title:
            title_error = "Please enter a entry"
            blog_title = ''
        if '' == blog_body:
            body_error = "Please enter a entry"
            blog_body = ''
        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            # get the blog id
            the_blog = new_blog.id
            return redirect ("/blog?id=" + str(the_blog))         
        else:
            return render_template("newpost.html", title="Add a Blog Entry",title_error=title_error,body_error=body_error)

    return render_template("newpost.html", title="Add a Blog Entry")

    
    
         

@app.route("/blog", methods=["POST", "GET"])
def blog():

    blog_id = request.args.get("id")
    if blog_id==None:
        blogs = Blog.query.all()
        return render_template("blog.html", title="Build A Blog", blogs=blogs)
    else:
        blog=Blog.query.get(blog_id)
        return render_template("single-blog.html", blog=blog, title="Build A Blog")

        
# get the blog by the id that you have
        #query result
        
    
    #if request.method == "POST":
        #blog_title = request.form['blog_title']
        #blog_body = request.form['blog_body']
        #new_blog = Blog(blog_title, blog_body)
        #db.session.add(new_blog)
        #db.session.commit()


@app.route("/", methods=["POST", "GET"])
def index():
    
    if request.method == "POST":
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()

    return render_template('add_blog.html', title="Add a Blog Entry", blogs=blogs)

if __name__ == '__main__':
    app.run()

