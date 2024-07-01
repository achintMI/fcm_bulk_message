import os
from flask import jsonify, request
from app.routes import notifications_bp
from app.config import Config
from app.celery.tasks import process_and_send_notifications


@notifications_bp.route('/push-notification', methods=['POST'])
def push_notification():
    try:
        file = request.files.get('file')
        if not file.filename.endswith(".csv"):
            return jsonify({"status": "error", "message": "please provide a valid csv file"}), 401
        file_path = os.path.join(os.getcwd(), Config.TEMP_FILES_DIR, file.filename)
        file.save(file_path)

        process_and_send_notifications.apply_async(args=[file_path], queue='process_and_send_notifications')

        return jsonify({"status": "success", "message": "push notification in progress"}), 202
    except Exception as e:
        return jsonify({"status": "failed", "error": "internal server error"}), 500
