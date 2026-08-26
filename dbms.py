import sqlalchemy as m

def mysql_connection():
    engine = m.create_engine(
        "mysql+pymysql://root:admin@localhost/showroom"
    )
    return engine