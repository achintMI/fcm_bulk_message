# push notification through fcm


## Requirements

- Python 3.11
- Redis (for Celery message brokering)


## Setup

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd flask_project
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Create a `.env` file in the project root and add fill .env.example values:
    ```plaintext
    FLASK_CONFIG=development
   CELERY_BROKER_URL=
   CELERY_BACKEND_URL=
   OPENAI_API_KEY=
    ```
5. Create a `serviceAccountKey.json` file in the project root, it should have firebase admin login details
6. Database Migrations:
   ```sh
   flask db upgrade
   ```
7. Run the application:
    ```sh
    export FLASK_CONFIG=development  # Change to testing or production as needed
    python run.py
    ```
8. Run the celery app:
   ```sh
   celery -A  app.celery_worker.celery worker  -Q store_notifications,process_and_send_notifications,send_notifications --loglevel=info```
   ```
   
9. Access the healthcheck endpoint:
    ```sh
    curl http://127.0.0.1:8000/healthcheck
    ```

### Process a CSV file, to send push notifications
```bash
curl --location 'http://192.168.31.227:8000/push-notification' \
--form 'file=@"/Users/achintmistry/Desktop/To delte/Upwork Demo File - Sheet1.csv"'
```

response: 
```bash
{
    "message": "push notification in progress",
    "status": "success"
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
