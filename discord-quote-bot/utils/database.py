from tinydb import TinyDB, Query
from utils import get_config
from tinydb_smartcache import SmartCacheTable


# -----------------------------------------------------


db_name = get_config().get('db_name') or 'database.db'

db = TinyDB(db_name)
db.table_class = SmartCacheTable

guilds_settings =  db.table('guild_setting')
