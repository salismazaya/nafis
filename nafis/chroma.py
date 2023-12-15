import chromadb

client = chromadb.PersistentClient(path = '.nafis_data')
collection = client.get_or_create_collection('nafis')