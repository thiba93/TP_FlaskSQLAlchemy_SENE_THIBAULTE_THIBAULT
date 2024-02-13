from flask import Blueprint, render_template
from .forms import InscriptionForm, AjoutFilmForm
from .models import Utilisateur, Film
from .database import db
from werkzeug.security import generate_password_hash
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/inscription', methods=['GET', 'POST'])
def inscription():
    # Définir les actions pour inscrire un utilisateur
    form = InscriptionForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.mot_de_passe.data)

        # logique pour entrer l'utilisateur dans la BDD
        new_user = Utilisateur(
            nom=form.nom.data,
            email=form.email.data,
            mot_de_passe_hash = hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return render_template('index.html')
    return render_template('inscription.html', form=form)

@main.route('/ajouter-film', methods=['GET', 'POST'])
def ajouter_film():
    form = AjoutFilmForm()
    if form.validate_on_submit():
        new_film = Film(
            titre = form.titre.data,
            realisateur = form.realisateur.data,
            annee_sortie = form.annee_sortie.data,
            genre = form.genre.data
        )
        db.session.add(new_film)
        db.session.commit()
        return render_template('index.html')
    return render_template('ajouter-film.html', form=form)

@main.route('/film/<int:id>')
def display(id):
    film = Film.query.get_or_404(id)
    return render_template('afficher-film.html', film=film)

