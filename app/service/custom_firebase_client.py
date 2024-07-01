
from firebase_admin import exceptions
from firebase_admin.messaging import requests, BatchResponse, SendResponse
import concurrent.futures

from firebase_admin import messaging


class CustomFirebaseAdmin(messaging._MessagingService):
    def send_each(self, messages, dry_run=False):
        if not isinstance(messages, list):
            raise ValueError('messages must be a list of messaging.Message instances.')
        if len(messages) > 500:
            raise ValueError('messages must not contain more than 500 elements.')

        def send_data(data):
            try:
                resp = self._client.body(
                    'post',
                    url=self._fcm_url,
                    headers=self._fcm_headers,
                    json=data)
            except requests.exceptions.RequestException as exception:
                return SendResponse(resp=None, exception=self._handle_fcm_error(exception))
            else:
                return SendResponse(resp, exception=None)

        message_data = [self._message_data(message, dry_run) for message in messages]
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                responses = [resp for resp in executor.map(send_data, message_data)]
                return BatchResponse(responses)
        except Exception as error:
            raise exceptions.UnknownError(
                message='Unknown error while making remote service calls: {0}'.format(error),
                cause=error)
