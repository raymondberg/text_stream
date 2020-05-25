from functools import wraps

from flask import abort
from twilio.twiml.messaging_response import MessagingResponse


class TwilioService:
    @classmethod
    def is_too_long(_, message):
        return len(message) > 160

    @classmethod
    def is_valid_request(_, f):
        """Validates that incoming requests genuinely originated from Twilio"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Create an instance of the RequestValidator class
            validator = RequestValidator(os.environ.get('TWILIO_AUTH_TOKEN'))

            # Validate the request using its URL, POST data,
            # and X-TWILIO-SIGNATURE header
            request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

            # Continue processing the request if it's valid, return a 403 error if
            # it's not
            if request_valid:
                return f(*args, **kwargs)
            else:
                return abort(403)
        return decorated_function

    class Responses:
        @classmethod
        def respond(_, message):
            resp = MessagingResponse()
            resp.message(message)
            return str(resp)

        @classmethod
        def success(cls):
            return cls.respond("Thanks for your message! We'll add it to the stream.")

        @classmethod
        def too_long(cls):
            return cls.respond("Oops! We can only accept 160 characters. Can you try something shorter?")

        @classmethod
        def unknown(cls):
            return cls.respond("Something went wrong. Please try again.")
