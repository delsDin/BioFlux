import hashlib
import uuid

SECRET = "MON_SECRET_SUPER_PRIVE"

def get_machine_id():
    return str(uuid.getnode())

def generate_key(machine_id, app_name):
    data = f"{machine_id}-{app_name}-{SECRET}"
    return hashlib.sha256(data.encode()).hexdigest()

def check_license(user_key, app_name):
    machine_id = get_machine_id()
    valid_key = generate_key(machine_id, app_name)
    return user_key == valid_key
