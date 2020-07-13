from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Owner %r>' % self.id


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer(), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    pet_type = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Owner %r>' % self.id


@app.route('/')
def show_owners():
    owners = Owner.query.order_by(Owner.date.desc()).all()
    return render_template('show_owners.html', owners=owners)


@app.route('/owner/<int:id>', methods=['GET', 'POST'])
def owner_page(id):
    owner = Owner.query.get(id)
    pet = Pet.query.filter_by(owner_id=id).all()
    return render_template('owner_page.html', owner=owner, pet=pet)


@app.route('/bonus')
def bonus():
    return render_template('bonus.html')


@app.route('/owner/<int:owner_id>/add_pet', methods=['GET', 'POST'])
def add_pet(owner_id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        pet_type = request.form['pet_type']

        pet = Pet(name=name, age=age, pet_type=pet_type, owner_id=owner_id)

        try:
            db.session.add(pet)
            db.session.commit()
            return redirect('/')
        except Exception as a:
            return str(a)
    else:
        return render_template('add_pet.html')


@app.route('/add_owner', methods=['GET', 'POST'])
def add_owner():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']

        owner = Owner(name=name, age=age, city=city)

        try:
            db.session.add(owner)
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR'
    else:
        return render_template('add_owner.html')


if __name__ == '__main__':
    app.run(debug=True)
