import uuid

def get_hwid():
    hwid = uuid.getnode()
    return str(hwid)

def check_hwid(allowed_hwid):
    current_hwid = get_hwid()
    if current_hwid != allowed_hwid:
        return False
    return True