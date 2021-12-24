from flask import (Flask,
                   render_template,
                   redirect,
                   url_for,
                   request,
                   abort,
                   flash)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from sqlalchemy.orm import backref
from werkzeug.datastructures import ContentSecurityPolicy

from forms import SubjectForm, RegisterForm
app = Flask(__name__)

# for web forms to work u need to set a secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/school'
app.config["SECRET_KEY"] = os.urandom(32)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class students(db.Model):
    __tablename__ = 'students'

    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))
    registerations = db.relationship(
        "Register", backref="student_object", lazy=True)

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column('subject_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    registerations = db.relationship(
        "Register", backref="subject_object", lazy=True)

    def __init__(self, name, ):
        self.name = name


class Register(db.Model):
    __tablename__ = "registers"
    id = db.Column('register_id', db.Integer, primary_key=True)
    subject = db.Column(db.Integer, db.ForeignKey(
        'subjects.subject_id'), nullable=False)
    student = db.Column(db.Integer, db.ForeignKey(
        'students.student_id'), nullable=False)

    def __repr__(self) -> str:
        return '<Registeration of stud {} in {}>'.format(self.student, self.subject)
# db.create_all()


@app.route('/')
def show_all():
    return render_template('show_all.html', students=students.query.all())


@app.route('/school', methods=["GET"])
def school():
    sub_form = SubjectForm()
    subjects = Subject.query.all()
    # , register_form=RegisterForm)
    return render_template("school.html", subjects=subjects, subject_form=sub_form)


@app.route('/school', methods=["POST"])
def make_subject():
    flash("created the subject")
    print(request.form.get("name"))
    try:
        sub = Subject(request.form.get('name'))
        db.session.add(sub)
        db.session.commit()

    except:
        db.session.rollback()
        flash("Error occured")

        pass
    return redirect('/school')


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = students(request.form['name'], request.form['city'],
                               request.form['addr'], request.form['pin'])

            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


@app.route('/hello')
def hello_world():
    flash("hello people")
    return render_template("index.html")


@app.route('/redirect')
def go_to_google():
    abort(404)
    return redirect("http://www.google.com")

# dynamic route


@app.route('/user/<name>')
def hellouser(name):
    return "<h1> Hello, {} </h1>".format(name)


@app.errorhandler(404)
def error_404(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
