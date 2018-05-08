from flask import jsonify

class ExceptionHandler(Exception):
    '''
        Called by app.py when an error occurs. Accepts a message which it 
        turns into proper error response
    '''
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        msg = dict(self.payload or ())
        msg['Error'] = self.message
        return msg
