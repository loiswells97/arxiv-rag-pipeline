# Connect to the database

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

print(f"Connected to {DB_NAME} on {DB_HOST}:{DB_PORT}")

cursor = conn.cursor()
cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
cursor.execute("CREATE TABLE IF NOT EXISTS documents (id SERIAL PRIMARY KEY, text TEXT, embedding VECTOR(1536), source TEXT, metadata JSONB);")
cursor.execute("CREATE INDEX IF NOT EXISTS documents_embedding_idx ON documents USING hnsw (embedding vector_cosine_ops);")
conn.commit()
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
tables = cursor.fetchall()
for table in tables:
    print(table[0])
cursor.close()
conn.close()

print("Database setup complete")
