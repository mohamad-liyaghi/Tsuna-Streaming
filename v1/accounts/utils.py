import uuid, random

def token_generator():
    return uuid.uuid4().hex

def user_id_generator():
    return random.randint(0, 999999999999999)