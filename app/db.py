import databases
import sqlalchemy
from sqlalchemy.sql import func

DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)


metadata = sqlalchemy.MetaData()

dblogs = sqlalchemy.Table(
    "log",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("request", sqlalchemy.String),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime(timezone=True), default=func.now()),
    sqlalchemy.Column("response", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
