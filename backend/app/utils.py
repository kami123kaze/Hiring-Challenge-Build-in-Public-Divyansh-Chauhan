import datetime

def get_current_timestamp():
    return datetime.datetime.now(datetime.UTC).strftime("%d%m%Y")

def validate_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def generate_session_id(user_id: str) -> str:
    return f"{user_id}_{int(datetime.datetime.now(datetime.UTC).timestamp())}"