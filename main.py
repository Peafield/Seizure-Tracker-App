from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import NewEntry, LogIn, NewUser
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from functools import wraps
from dash_application import create_dash_application



app = Flask(__name__)
app.config['SECRET_KEY'] = 'P6vRydCGlfbQ`HlegU*En!^CP4UQo'
Bootstrap(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seizure.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Dash App
create_dash_application(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


# Seizure Database Model

class Seizures(db.Model):
    __tablename__ = "Seizures"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(250), nullable=False)
    seizure_type = db.Column(db.String(250), nullable=False)
    note = db.Column(db.String(250), nullable=False)


# db.create_all()

# User Table

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))


# db.create_all()

@app.route('/register', methods=["GET", "POST"])
def register():
    form = NewUser()
    if request.method == "POST":

        if User.query.filter_by(username=request.form.get('username')).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            username=request.form.get('username'),
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("new_entry"))

    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LogIn()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("That username doesn't exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user, remember=True)
            return redirect(url_for('new_entry'))

    return render_template('login.html', form=form, logged_in=current_user.is_authenticated)


@app.route('/calendar', methods=['GET', 'POST'])
def show_calendar():
    events = Seizures.query.all()
    return render_template('calendar.html', events=events)


@app.route('/new-entry', methods=['GET', 'POST'])
def new_entry():
    form = NewEntry()
    if request.method == 'POST':
        new_seizure = Seizures(
            date=request.form.get('date'),
            seizure_type=request.form.get('seizure_type'),
            note=request.form.get('notes'),
        )
        db.session.add(new_seizure)
        db.session.commit()
        return redirect(url_for('show_calendar'))
    return render_template('new-entry.html', form=form)


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    event_id = None
    if request.method == 'POST':
        event_id = request.form['id']
        event_to_delete = Seizures.query.get(event_id)
        db.session.delete(event_to_delete)
        db.session.commit()
        return redirect(url_for('show_calendar'))


# TODO Make reports

@app.route('/dashboard')
def dashboard():
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run()
