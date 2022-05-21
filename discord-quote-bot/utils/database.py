import pickledb
from utils import get_config


# -----------------------------------------------------


db_name = get_config().get('db_name') or 'database.db'

database = pickledb.load(db_name, True)
