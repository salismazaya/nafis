from nafis.chroma import collection
from nafis.schema import Result
from rich.logging import RichHandler
import sqlite3, glob, pathlib, pickle, zlib, logging

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)
logger = logging.getLogger("rich")

logger.info("Connecting to database")
conn = sqlite3.connect('database.db')
cur = conn.cursor()

logger.info("Retrieve all databases")
databases = glob.glob('database/*.nafis')
for database in databases:
    hash_ = pathlib.Path(database).as_posix().split('/')[-1].removesuffix('.nafis')
    cur.execute(f"SELECT * FROM imported WHERE hash = '{hash_}'")
    if cur.fetchone():
        continue

    logger.info(f"Importing database {database}")
    result: Result = pickle.loads(
        zlib.decompress(
            open(database, 'rb').read()
        )
    )
    for embedding in result.embeddings:
        collection.add(
            ids = [f'{embedding.title}|{embedding.timestamp}'],
            embeddings = [embedding.vector],
        )
    
    logger.info("Saving imported database")
    cur.execute(f"INSERT INTO imported VALUES('{hash_}')")
    conn.commit()