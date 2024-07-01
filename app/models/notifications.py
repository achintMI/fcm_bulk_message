from app.extensions import db
from datetime import datetime


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(50))
    title = db.Column(db.String(100))
    message = db.Column(db.Text)
    image = db.Column(db.String(200))
    coupon = db.Column(db.String(50))
    device_token = db.Column(db.String(200))
    status = db.Column(db.String(20), index=True)
    fcm_message_id = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, index=True)
    updated_at = db.Column(db.TIMESTAMP, nullable=False, index=True)

    def __init__(self, customer_id, name, title, message, image, coupon, device_token, status, fcm_message_id):
        self.customer_id = customer_id
        self.name = name
        self.title = title
        self.message = message
        self.image = image
        self.coupon = coupon
        self.device_token = device_token
        self.status = status
        self.fcm_message_id = fcm_message_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
