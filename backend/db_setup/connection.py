import config
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

pool = ConnectionPool(
    conninfo=config.db_url,
    max_size=10,
    kwargs={"autocommit": True}
)

checkpointer = PostgresSaver(pool)

checkpointer.setup()