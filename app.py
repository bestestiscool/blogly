from flask import Flask, request, render_template, redirect, flash, session,url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

"""Blogly application."""

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'user123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def index():
    """Show list of users"""
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/users')
def list_users():
    """Show list of users with links to details"""
    users = User.query.all()
    return render_template('list_users.html', users=users)

@app.route('/users/new', methods = ['POST'])
def create_users():
    first_name = request.form['first_name'] 
    last_name = request.form['last_name'] 
    image_url = request.form['image_url'] or None

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    # Redirect to the user detail page for the new user
    return redirect(url_for('show_user', user_id=new_user.id))

    

@app.route('/users/new', methods=['GET'])
def add_user():
    """Show an add form for users"""
    return render_template('add_user.html')

@app.route('/<user_id>')
def show_user(user_id):
    """Show details of a user"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user = user)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        # Assuming you have form fields named 'first_name', 'last_name', and 'image_url'
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']
        db.session.commit()
        return redirect(url_for('show_user', user_id=user.id))
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))
