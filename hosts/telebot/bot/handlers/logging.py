import logging
import requests
from bot.config import DB_API_HOST, DB_API_PORT

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def log_command_in_db(name: str, chat_id: int,
                      is_completed: bool, is_cancelled: bool) -> bool:
    url = f'http://{DB_API_HOST}:{DB_API_PORT}/command'
    data = {
        'name': name,
        'chat_id': chat_id,
        'is_completed': is_completed,
        'is_cancelled': is_cancelled,
    }
    res = requests.post(url, json=data)
    return res.ok
