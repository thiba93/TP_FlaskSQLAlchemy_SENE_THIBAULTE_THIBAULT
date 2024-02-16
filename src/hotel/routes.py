from flask import jsonify, request, Blueprint
from .models import Chambre, Reservation, Client
from datetime import datetime
from .database import db
main = Blueprint('main', __name__)