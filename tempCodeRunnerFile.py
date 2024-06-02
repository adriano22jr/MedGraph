import pandas as pd
from pymongo import MongoClient

def data_cleaning(df):

    df = df.drop(columns=['DOI', 'pages', 'SJR', 'ISSN'], errors='ignore')
    df = df.rename(columns={'PMID': '_id'})
    cols = ['_id'] + [col for col in df.columns if col != '_id']
    df = df[cols]

    return df

def csv_to_mongodb(csv_file, db_name, collection_name, mongodb_uri):
    client = MongoClient(mongodb_uri)
    db = client[db_name]

    if collection_name in db.list_collection_names():
        print(f"La collezione '{collection_name}' esiste già nel database '{db_name}'.")
        return

    df = pd.read_csv(csv_file)
    df = data_cleaning(df)
    data = df.to_dict(orient="records")

    collection = db[collection_name]
    collection.insert_many(data)
    print(f"Dati inseriti con successo nella collezione '{collection_name}' del database '{db_name}'.")

def filter_collection_by_pmid(db_name, collection_name, target_collection_name, pmid_csv_file, mongodb_uri):
    client = MongoClient(mongodb_uri)
    db = client[db_name]

    if target_collection_name in db.list_collection_names():
        print(f"La collezione '{target_collection_name}' esiste già nel database '{db_name}'.")
        return

    pmid_df = pd.read_csv(pmid_csv_file)
    pmid_list = pmid_df["PMID"].tolist()
    source_collection = db[collection_name]
    matching_documents = source_collection.find({"_id": {"$in": pmid_list}})

    target_collection = db[target_collection_name]
    matching_docs_list = list(matching_documents)
    if matching_docs_list:
        target_collection.insert_many(matching_docs_list)
        print(f"Dati inseriti con successo nella collezione '{target_collection_name}' del database '{db_name}'.")
    else:
        print(f"Nessun documento trovato con i PMIDs forniti.")

csv_file = "dataset.csv"
db_name = "MedGraph"
collection_name = "Dataset"
mongodb_uri = "mongodb://localhost:27017/"
csv_to_mongodb(csv_file, db_name, collection_name, mongodb_uri)

new_collection_name = "Dataset2000Entries"
pmid_csv_file = "pmid_samples.csv"
filter_collection_by_pmid(db_name, collection_name, new_collection_name, pmid_csv_file, mongodb_uri)