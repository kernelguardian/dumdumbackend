from os import getenv

from supabase import create_client, Client

from utils.loghelper import MyLogger

logger = MyLogger.__call__().get_logger()


SUPABASE_URL = getenv("SUPABASE_URL")
SUPABASE_KEY = getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def insert_data(table_name="harvest", data={}):
    try:
        data = supabase.table(table_name).insert(data).execute()
    except Exception:
        logger.info("Supabase insertion error | {} | {}".format(data, table_name))
