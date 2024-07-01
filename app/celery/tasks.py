import csv
import firebase_admin
from firebase_admin import credentials, messaging
from app.celery.celery_app import celery_app as app
from app.service.custom_firebase_client import CustomFirebaseAdmin
from app.extensions import db
from app.models.notifications import Notification

cred = credentials.Certificate('serviceAccountKey.json')
firebase_app = firebase_admin.initialize_app(cred)
custom_firebase_app = CustomFirebaseAdmin(firebase_app)
BATCH_SIZE = 500


def create_message(user):
    message_body = user['Message'].replace('{name}', user['Name']).replace('{coupon code}', user['Coupon'])
    return messaging.Message(
        notification=messaging.Notification(
            title=user['Title'],
            body=message_body,
            image=user['Image']
        ),
        token=user['Device_Token'],
        data={
            'username': user['Name'],
            'coupon_code': user['Coupon'],
        }
    )


def read_user_data(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        headers = [header.strip().replace(' ', '_') for header in csv_reader.fieldnames]
        csv_reader.fieldnames = headers
        users = list(csv_reader)
    return users


def notification_to_dict(notification):
    return {
        'customer_id': notification.customer_id,
        'name': notification.name,
        'title': notification.title,
        'message': notification.message,
        'image': notification.image,
        'coupon': notification.coupon,
        'device_token': notification.device_token,
        'status': notification.status,
        'fcm_message_id': notification.fcm_message_id,
    }


@app.task(name='send_batch_notifications')
def send_notifications(users_batch):
    messages = [create_message(user) for user in users_batch]
    response = custom_firebase_app.send_each(messages, dry_run=True)
    notifications = []
    for user, result in zip(users_batch, response.responses):
        notification = Notification(
            customer_id=user.get('Customer_Id'),
            name=user.get('Name'),
            title=user.get('Title'),
            message=user.get('Message').replace('{name}', user['Name']).replace('{coupon code}', user['Coupon']),
            image=user.get('Image'),
            coupon=user.get('Coupon'),
            device_token=user.get('Device_Token'),
            fcm_message_id=result._message_id,
            status='Success' if result.success else 'Failure'

        )
        notifications.append(notification_to_dict(notification))

    store_notifications.apply_async(args=[notifications], queue='store_notifications')
    print(f"Batch sent successfully: {response.success_count} messages sent")
    return response.success_count


@app.task(name="process_and_send_notifications")
def process_and_send_notifications(file_path, batch_size=BATCH_SIZE):
    users = read_user_data(file_path)
    for i in range(0, len(users), batch_size):
        users_batch = users[i:i + batch_size]
        send_notifications.apply_async(args=[users_batch], queue='send_notifications')


@app.task(name='store_notifications')
def store_notifications(notification_dicts):
    notifications = [Notification(**data) for data in notification_dicts]
    db.session.bulk_save_objects(notifications)
    db.session.commit()
    print(f"Stored {len(notifications)} notifications successfully.")
