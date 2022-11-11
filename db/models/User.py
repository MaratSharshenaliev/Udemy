import datetime
import sqlalchemy
from db.base import metadata

users = sqlalchemy.Table(
    "users", 
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("email", sqlalchemy.String, primary_key=True, unique=True),
    sqlalchemy.Column("hashed_password", sqlalchemy.String),

    sqlalchemy.Column("is_superuser", sqlalchemy.Boolean),
    sqlalchemy.Column("is_mentor", sqlalchemy.Boolean),

    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow),
    sqlalchemy.Column("avatar", sqlalchemy.String),
    sqlalchemy.Column("type", sqlalchemy.String(10)),
    sqlalchemy.Column("audience", sqlalchemy.Integer),

    sqlalchemy.Column("firstname", sqlalchemy.String),
    sqlalchemy.Column("lastname", sqlalchemy.String, nullable=True),

)


