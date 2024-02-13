from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/<int:id>')
def display(id):
    return render_template('display.html', id=id)

