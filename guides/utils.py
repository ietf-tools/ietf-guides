from django.conf import settings
from hashids import Hashids

def encode_email(email, request_type):
    hasher = Hashids(salt=settings.HASHSALT, min_length=16)
    # Big assumption here about what EmailField will pass as valid (no non-ascii-utf8)
    array = [ord(x) for x in email]
    array.insert(0, 0 if request_type=='guide' else 1)
    return hasher.encode(*array)

def decode_hash(hash):
    hasher = Hashids(salt=settings.HASHSALT)
    decode = hasher.decode(hash)
    if not decode:
        return ()
    request_type = 'participant' if decode[0] else 'guide'
    email = u''.join([chr(x) for x in decode[1:]])
    return request_type, email