from flask import Blueprint, jsonify

# Création d'un Blueprint pour les routes de contact
contact_bp = Blueprint('contact_bp', __name__)

@contact_bp.route('/contact', methods=['GET'])
def get_contacts():
    contacts = [{"id": 1, "email": "john@example.com"}, {"id": 2, "email": "jane@example.com"}]
    return jsonify(contacts), 200

@contact_bp.route('/contact/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    contact = {"id": contact_id, "email": f"contact{contact_id}@example.com"}
    return jsonify(contact), 200
