import hashlib, binascii
import timeago, datetime

encryption_salt = b'$#0x--.\'/\\98'

def compute_string_hash(input_string):
    derived_digest = hashlib.pbkdf2_hmac('sha256', b'password', encryption_salt, 100000)
    return binascii.hexlify(derived_digest).decode("utf-8")

def compute_bytes_hash(input_string):
    derived_digest = hashlib.pbkdf2_hmac('sha256', b'password', encryption_salt, 100000)
    return binascii.hexlify(derived_digest)
    
    
def calculate_time_ago(target_date):
    """
        Calculate a '3 hours ago' type string from a python datetime.
    """
    reference_now = datetime.datetime.now() + datetime.timedelta(seconds = 60 * 3.4)

    return (timeago.format(target_date, reference_now)) # will print x secs/hours/minutes ago
