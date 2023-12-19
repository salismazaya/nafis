import datetime
from lib.chroma import collection
from lib.schema import Result
from lib.console import Console
import sqlite3, glob, pathlib, pickle, zlib, logging

logger = Console()
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
    with logger.status("Collection add ") as status:
        for index, embedding in enumerate(result.embeddings):
            if (isinstance(embedding.timestamp, datetime.timedelta)):
                timestamp = embedding.timestamp.seconds
            else:
                timestamp = embedding.timestamp
            status.update(f"Collection add {index}/{len(result.embeddings)}")

            collection.add(
                ids = [f'{embedding.title}|{timestamp}'],
                embeddings = [embedding.vector],
            )
    
    logger.info("Saving imported database")
    cur.execute(f"INSERT INTO imported VALUES('{hash_}')")
    conn.commit()