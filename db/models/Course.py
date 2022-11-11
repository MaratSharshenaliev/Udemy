import sqlalchemy
from db.base import metadata
Course = sqlalchemy.Table(
    "Course",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("Category", sqlalchemy.String),
    sqlalchemy.Column("SubCategory", sqlalchemy.Integer),
    sqlalchemy.Column("Tittle", sqlalchemy.String(60)),
    sqlalchemy.Column("subTittle", sqlalchemy.String(60)),
    sqlalchemy.Column("Description", sqlalchemy.Text),
    sqlalchemy.Column("language", sqlalchemy.String(5)),
    sqlalchemy.Column("level",  sqlalchemy.String(15)),
    sqlalchemy.Column("currency", sqlalchemy.String(3)),
    sqlalchemy.Column("cost", sqlalchemy.Float),
    sqlalchemy.Column("CourseActivated", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("CourseContentIsNull", sqlalchemy.Boolean, default=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),

    sqlalchemy.Column("image", sqlalchemy.String),
    sqlalchemy.Column("video", sqlalchemy.String),

)

CourseItem = sqlalchemy.Table(
    "CourseItem",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("Tittle", sqlalchemy.String(60)),
    sqlalchemy.Column("Description", sqlalchemy.Text),
    sqlalchemy.Column("CourseId", sqlalchemy.ForeignKey("Course.id"))
)

CourseItemFile = sqlalchemy.Table(
    "CourseItemFile",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("file", sqlalchemy.String, unique=True),
    sqlalchemy.Column("CourseItemId", sqlalchemy.ForeignKey("CourseItem.id")),
    sqlalchemy.Column("CourseId", sqlalchemy.ForeignKey("Course.id"))
)






