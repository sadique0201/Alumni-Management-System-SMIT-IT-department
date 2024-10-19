from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/uploads')
app.config["username_post"] = ""

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year_of_passout = db.Column(db.String(4), nullable=False)
    current_designation = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(100), nullable=False)
    photo_filename = db.Column(db.String(100), nullable=True)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        app.logger.info('testing info log')
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # return redirect(url_for('home'), username=user)
            return render_template('index.html', username=user.username)
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        flash('Username already exists')
    return render_template('register.html')


@app.route('/add_alumni', methods=['GET', 'POST'])
def add_alumni():
    alumni_list = Alumni.query.all()  # Fetch all alumni to display
    if request.method == 'POST':
        name = request.form['name']
        year_of_passout = request.form['year_of_passout']
        current_designation = request.form['current_designation']
        organization = request.form['organization']
        photo = request.files['photo']

        if photo:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        new_alumni = Alumni(
            name=name,
            year_of_passout=year_of_passout,
            current_designation=current_designation,
            organization=organization,
            photo_filename=filename
        )

        db.session.add(new_alumni)
        db.session.commit()

        flash('Alumni added successfully!')
        return redirect(url_for('add_alumni'))  # Refresh the page to show the new alumni

    return render_template('add_alumni.html', alumni_list=alumni_list)

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    return render_template("jobs.html")

@app.route('/events')
def events():
    return render_template("events.html")

@app.route('/forum')
def forum():
    return render_template("forum.html")

@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=5001)