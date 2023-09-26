from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Float, Boolean, Text, Table, Column
from sqlalchemy.dialects.postgresql import UUID


metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(40), unique=True, index=True),
    Column("name", String(100)),
    Column("hashed_password", String()),
    Column(
        "is_active",
        sqlalchemy.Boolean(),
        server_default=sqlalchemy.sql.expression.true(),
        nullable=False,
    ),
)


tokens_table = Table(
    "tokens",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "token",
        UUID(as_uuid=False),
        server_default=sqlalchemy.text("uuid_generate_v4()"),
        unique=True,
        nullable=False,
        index=True,
    ),
    Column("expires", DateTime()),
    Column("user_id", ForeignKey("users.id")),
)

# https://habr.com/ru/articles/513328/
#это ссылка с инфой по фаст апи по реге