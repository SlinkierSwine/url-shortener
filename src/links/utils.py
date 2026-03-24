import uuid
from config import settings


def generate_short_id() -> str:
    return uuid.uuid4().hex[:settings.SHORT_ID_LENGTH]

