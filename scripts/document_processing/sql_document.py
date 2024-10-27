import sqlite3
import pandas as pd
from scripts.document_processing.base_document import Document

class SQL(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        conn = sqlite3.connect(self.filepath)
        query = "SELECT * FROM your_table"  # Hace falta modificar segun la consulta
        return pd.read_sql_query(query, conn)
