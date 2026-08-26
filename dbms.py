import sqlalchemy as m
from config import USER, PASSWORD, HOST, DATABASE

def mysql_connection():
    engine = m.create_engine(
       f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
    )
    return engine