# TP Flask SQLAlchemy - Gestion Hôtel

Ce projet est une application Flask pour la gestion d'un hôtel, permettant de gérer les chambres, les réservations, et les clients.

## Installation

Clonez le dépôt :

git clone https://github.com/thiba93/TP_FlaskSQLAlchemy_SENE_THIBAULTE_THIBAULT.git
cd TP_FlaskSQLAlchemy_SENE_THIBAULTE_THIBAULT


///////////////////////////////
Créations de Chambres
chambre1.json

{
  "numero": "101",
  "type": "simple",
  "prix": 75.00
}
chambre2.json

{
  "numero": "102",
  "type": "double",
  "prix": 90.00
}
chambre3.json

{
  "numero": "103",
  "type": "suite",
  "prix": 150.00
}

///////////////////////////////////////
Créations de Clients
client1.json

{
  "nom": "Alice Dupont",
  "email": "alice.dupont@example.com"
}
client2.json

{
  "nom": "Bob Martin",
  "email": "bob.martin@example.com"
}
client3.json

{
  "nom": "Charlie Nom",
  "email": "charlie.nom@example.com"
}

///////////////////////////////////////
Créations de Réservations
reservation1.json

{
  "id_client": 1,
  "id_chambre": 1,
  "date_arrivee": "2024-03-01",
  "date_depart": "2024-03-05",
  "statut": "confirmée"
}
reservation2.json

{
  "id_client": 2,
  "id_chambre": 2,
  "date_arrivee": "2024-04-10",
  "date_depart": "2024-04-15",
  "statut": "confirmée"
}
reservation3.json

{
  "id_client": 3,
  "id_chambre": 3,
  "date_arrivee": "2024-05-20",
  "date_depart": "2024-05-25",
  "statut": "confirmée"
}
