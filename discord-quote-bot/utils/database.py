from tinydb import TinyDB, Query
from utils import get_config


# -----------------------------------------------------


db_name = get_config().get('db_name') or 'database.db'

database = TinyDB(db_name)
