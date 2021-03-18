import datetime
import uuid

# common response
success = {
    'status': 200,
    'code': '200',
    'message': 'OK',
    'data': None,
    'requestId': uuid.uuid4(),
    'requestAt': datetime.datetime.now(),
    'responseAt': datetime.datetime.now()
}

fail = {
    'status': 500,
    'code': '500',
    'message': 'NG',
    'data': None,
    'requestId': uuid.uuid4(),
    'requestAt': datetime.datetime.now(),
    'responseAt': datetime.datetime.now()
}