from flask import Flask, render_template, redirect, flash, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_db, Pet
from form import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "petsarecool"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///petadopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)



@app.route('/')
def home_page():

    pet = Pet.query.all()
    return render_template("home_page.html", pet=pet)

@app.route('/newpet', methods=["GET", "POST"])
def add_pet():
    
    form = AddPetForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} added.")
        return redirect(url_for('list_pets'))

    else:
        return render_template("add_pet.html", form=form)


@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('list_pets'))

    else:
        return render_template("edit_pet.html", form=form, pet=pet)


@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):

    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)
