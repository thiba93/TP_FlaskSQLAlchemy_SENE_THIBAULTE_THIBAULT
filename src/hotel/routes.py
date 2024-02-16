from flask import jsonify, request, Blueprint
from .models import Chambre, Reservation, Client
from datetime import datetime
from .database import db
from sqlalchemy import and_, not_, or_
main = Blueprint('main', __name__)

@main.route('/api/chambres', methods=['POST'])
def ajouter_chambre():
    data = request.get_json()
    numero = data.get('numero')
    type_chambre = data.get('type')
    prix = data.get('prix')

    # Vérifiez si tous les champs nécessaires sont présents
    if not all([numero, type_chambre, prix]):
        return jsonify({"success": False, "message": "Tous les champs sont requis"}), 400

    # Créez une nouvelle instance de Chambre
    nouvelle_chambre = Chambre(numero=numero, type=type_chambre, prix=prix)

    # Ajoutez la nouvelle chambre à la base de données
    db.session.add(nouvelle_chambre)
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Chambre ajoutée avec succès."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Erreur lors de l'ajout de la chambre."}), 500

@main.route('/api/chambres/<int:id>', methods=['DELETE'])
def supprimer_chambre(id):
    chambre = Chambre.query.get(id)
    if chambre is None:
        return jsonify({"success": False, "message": "Chambre non trouvée."}), 404

    db.session.delete(chambre)
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Chambre supprimée avec succès."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Erreur lors de la suppression de la chambre."}), 500

@main.route('/api/chambres/<int:id>', methods=['PUT'])
def modifier_chambre(id):
    chambre = Chambre.query.get(id)
    if chambre is None:
        return jsonify({"success": False, "message": "Chambre non trouvée."}), 404

    data = request.get_json()
    numero = data.get('numero')
    type_chambre = data.get('type')
    prix = data.get('prix')

    # Vérifiez si tous les champs nécessaires sont présents
    if not all([numero, type_chambre, prix]):
        return jsonify({"success": False, "message": "Tous les champs sont requis"}), 400

    # Mise à jour des informations de la chambre
    chambre.numero = numero
    chambre.type = type_chambre
    chambre.prix = prix

    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Chambre mise à jour avec succès."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Erreur lors de la mise à jour de la chambre."}), 500

@main.route('/api/client', methods=['POST'])
def ajouter_client():
    data = request.get_json()
    nom = data.get('nom')
    email = data.get('email')

    # Vérifiez si tous les champs nécessaires sont présents
    if not nom or not email:
        return jsonify({"success": False, "message": "Le nom et l'email sont requis."}), 400

    # Vérifiez si l'email existe déjà
    if Client.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Un client avec cet email existe déjà."}), 400

    # Créez une nouvelle instance de Client
    nouveau_client = Client(nom=nom, email=email)

    # Ajoutez le nouveau client à la base de données
    db.session.add(nouveau_client)
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Client ajouté avec succès."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Erreur lors de l'ajout du client."}), 500

@main.route('/api/reservations', methods=['POST'])
def creer_reservation():
    data = request.get_json()
    id_client = data.get('id_client')
    id_chambre = data.get('id_chambre')
    date_arrivee = data.get('date_arrivee')
    date_depart = data.get('date_depart')
    statut = data.get('statut')

    # Conversion des dates en objets datetime
    try:
        date_arrivee = datetime.strptime(date_arrivee, '%Y-%m-%d')
        date_depart = datetime.strptime(date_depart, '%Y-%m-%d')
    except ValueError:
        return jsonify({"success": False, "message": "Format de date invalide. Utilisez YYYY-MM-DD."}), 400

    # Vérification de la disponibilité de la chambre
    reservations_existantes = Reservation.query.filter(
    Reservation.id_chambre == id_chambre,
    Reservation.date_depart > date_arrivee,
    Reservation.date_arrivee < date_depart
    ).all()

    if reservations_existantes:
        return jsonify({"success": False, "message": "La chambre n'est pas disponible pour les dates sélectionnées."}), 400

    # Création de la nouvelle réservation
    nouvelle_reservation = Reservation(
        id_client=id_client,
        id_chambre=id_chambre,
        date_arrivee=date_arrivee,
        date_depart=date_depart,
        statut=statut
    )

    db.session.add(nouvelle_reservation)
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Réservation créée avec succès."}), 201
    except Exception as e:
        db.session.rollback()
        print(e)  # Ou utilisez votre système de logging préféré
        return jsonify({"success": False, "message": "Erreur lors de la création de la réservation."}), 500

@main.route('/api/reservations/<int:id>', methods=['DELETE'])
def annuler_reservation(id):
    reservation = Reservation.query.get(id)
    if not reservation:
        return jsonify({"success": False, "message": "Réservation non trouvée."}), 404

    db.session.delete(reservation)
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Réservation annulée avec succès."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Erreur lors de l'annulation de la réservation."}), 500

@main.route('/api/chambres/disponibles', methods=['GET'])
def rechercher_chambres_disponibles():
    date_arrivee = request.args.get('date_arrivee')
    date_depart = request.args.get('date_depart')

    try:
        date_arrivee = datetime.strptime(date_arrivee, '%Y-%m-%d')
        date_depart = datetime.strptime(date_depart, '%Y-%m-%d')
    except ValueError:
        return jsonify({"success": False, "message": "Format de date invalide. Utilisez YYYY-MM-DD."}), 400

    if date_arrivee >= date_depart:
        return jsonify({"success": False, "message": "La date d'arrivée doit être antérieure à la date de départ."}), 400

    # Recherche des chambres qui ne sont pas réservées pendant la période donnée
    chambres_disponibles = Chambre.query.outerjoin(Reservation, and_(
        Reservation.id_chambre == Chambre.id,
        not_(and_(Reservation.date_depart <= date_arrivee, Reservation.date_arrivee >= date_depart))
    )).filter(or_(Reservation.id == None, Reservation.date_depart <= date_arrivee, Reservation.date_arrivee >= date_depart)).all()

    resultat = [
        {"id": chambre.id, "numero": chambre.numero, "type": chambre.type, "prix": chambre.prix}
        for chambre in chambres_disponibles
    ]

    return jsonify(resultat), 200



