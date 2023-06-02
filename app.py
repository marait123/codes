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

from forms import SubjectForm, RegisterForm
app = Flask(__name__)

# for web forms to work u need to set a secret_key
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/school'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://mohammed:123456@localhost:5432/school'

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
    image = db.Column(db.String(100))

    def __init__(self, name, city, addr, pin, image):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin
        self.image = image

    def __str__(self):
        return f"student {self.name} from {self.city} with id {self.id} with image {self.image}"

    def __repr__(self):
        return f"student {self.name} from {self.city} with id {self.id} with image {self.image}"


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column('subject_id', db.Integer, primary_key=True)
    # TODO: define a name property on with max_length = 100
    name = db.Column(db.String(100))
    registerations = db.relationship(
        "Register", backref="subject_object", lazy=True)

    def __init__(self, name, ):
        self.name = name


class Register(db.Model):
    __tablename__ = "registers"
    id = db.Column('register_id', db.Integer, primary_key=True)

    student = db.Column(db.Integer, db.ForeignKey(
        'students.student_id'), nullable=False)
    # TODO link this property to the subject table

    # TODO; link this property to the student table

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
    return render_template("school.html", subjects=subjects, subject_form=sub_form)


@app.route('/school', methods=["POST"])
def make_subject():
    flash("created the subject")
    print(request.form.get("name"))
    try:
        # TODO: create a new subject and add it to the database

    except:
        # TODO:  rollback in case of any error

        # TODO: check the school.html for flashed messages (no implementation needed)
        flash("Error occured")

    # TOOD: redirect to the school endpoint
    return redirect('/school')


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or \
                not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            # read image, and save locally
            image = request.files['image']
            image.save(os.path.join("static", "upload", image.filename))
            # TODO: create user and add it to the database

            flash('Record was successfully added')
            return redirect(url_for('student_info', student_id=student.id))
    return render_template('new_student.html')

# update student info


@app.route('/update', methods=['GET', 'POST'])
def update_student():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or \
                not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = students(request.form['name'], request.form['city'],
                               request.form['addr'], request.form['pin'])

            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))


@app.route("/student_info/<int:student_id>")
def student_info(student_id):
    # TODO: get student with that student_id

    return render_template("student_info.html", student=student)


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
    app.run(debug=True, port=5022, host='0.0.0.0')
