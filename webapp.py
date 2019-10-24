from flask import Flask, render_template, request, redirect, url_for, jsonify, session, json, flash
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, login_required, UserMixin, RoleMixin
from flask_security.utils import hash_password
from werkzeug.security import check_password_hash
import subprocess
from flask_login import login_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECURITY_PASSWORD_SALT'] = 'secretsalt'

db = SQLAlchemy(app)

command = ('lshw -json')

p = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

text = p.stdout.read()
retcode = p.wait()
#print(text)

new_text = json.loads(text)

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role',
            secondary=roles_users,
            backref=db.backref('users', lazy='dynamic')
    )

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))

# conectando os models ao Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar():
    if request.method == 'POST':
        user_datastore.create_user(
            email= request.form.get('email'),
            password = request.form.get('password')#hash_password(request.form.get('password'))
        )
        db.session.commit()

        return redirect(url_for('login_post'))

    return render_template('cadastrar.html')

@app.route('/entrar', methods=['POST', 'GET'])
def login_post():
    if request.method == 'POST':
        email = request.form.get('email') #login
        passw = request.form.get('password')#login

        user = User.query.filter_by(email=email).first()#db
        print(user.password)
        print(email)
        print(passw)
        print(user.email)

        if user.email != email and user.password != passw:
            print("entrou")
            return "<strong>Erro. Tente novamente.</strong>"

        if user.email == email and user.password == passw:
            return  jsonify(new_text), 200
        else:
            return  "<strong>Erro. Tente novamente.</strong>"

    return render_template('perfil.html')


if __name__ == '__main__':
    app.run()