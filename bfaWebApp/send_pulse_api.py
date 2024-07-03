# sendpulse_service.py

from sendpulse import SendpulseApi, Token

class SendPulseService:
    def __init__(self):
        self.api_user_id = 'your_api_id'
        self.api_secret = 'your_api_secret'
        self.token_storage = Token(token_storage='memcached')  # or 'file'
        self.sp_api = SendpulseApi(self.api_user_id, self.api_secret, self.token_storage)

    def create_address_book(self, name):
        return self.sp_api.create_address_book(name)
    
    def add_email_to_book(self, book_id, emails):
        return self.sp_api.add_emails(book_id, emails)
    
    def create_template(self, name, body):
        return self.sp_api.create_template(name, body)
    
    def send_email(self, sender, recipients, subject, body):
        return self.sp_api.smtp_send_mail({
            'html': body,
            'text': body,
            'subject': subject,
            'from': {'name': sender['name'], 'email': sender['email']},
            'to': [{'name': recipient['name'], 'email': recipient['email']} for recipient in recipients]
        })
