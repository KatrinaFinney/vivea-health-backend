# vivea_health/routes.py
from flask import Blueprint, jsonify
from .jwt_helpers import verify_token

# Use a blueprint for organization (optional, but recommended for larger projects)
api = Blueprint('api', __name__)

@api.route('/api/health', methods=['GET'])
def health():
    user = verify_token()
    if not user:
        return jsonify({'message': 'Unauthorized'}), 401
    return jsonify({"status": "healthy"})
