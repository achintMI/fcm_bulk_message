from flask import jsonify
from app.routes import healthcheck_bp


@healthcheck_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'healthy'}), 200
