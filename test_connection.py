import sqlalchemy

engine = sqlalchemy.create_engine(
    "mysql+mysqlconnector://user_dteng:cirilgroupt@127.0.0.1:3306/db_dteng"
)

with engine.connect() as connection:
    result = connection.execute(sqlalchemy.text("SELECT 1"))
    print(result.scalar())