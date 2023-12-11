from lib.chroma import collection
from lib.schema import Result
import sqlite3, glob, pathlib, pickle
  
conn = sqlite3.connect('database.db')
cur = conn.cursor()

databases = glob.glob('database/*.nafis')
for database in databases:
    hash_ = pathlib.Path(database).as_posix().split('/')[-1].removesuffix('.nafis')
    cur.execute(f"SELECT * FROM imported WHERE hash = '{hash_}'")
    if cur.fetchone():
        continue

    print('Importing', database)
    result: Result = pickle.loads(open(database, 'rb').read())
    for embedding in result.embeddings:
        collection.add(
            ids = [f'{embedding.title}|{embedding.timestamp}'],
            embeddings = [embedding.vector],
        )
    
    cur.execute(f"INSERT INTO imported VALUES('{hash_}')")
    conn.commit()