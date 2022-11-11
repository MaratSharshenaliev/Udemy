import datetime

import sqlalchemy
from db.base import metadata

Reset_password_cache = sqlalchemy.Table(
    "reset_password_cache",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("email", sqlalchemy.String(100)),
    sqlalchemy.Column("reset_code", sqlalchemy.String(50)),
    sqlalchemy.Column("status", sqlalchemy.String(1)),
    sqlalchemy.Column("reset_code_created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow)
)


