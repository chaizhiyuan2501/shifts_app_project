import uuid

def unique_code(prefix="code"):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"

def unique_name(prefix="user"):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"