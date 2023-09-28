from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Float, Boolean, Text, Table, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import sqlalchemy


metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(40), unique=True, index=True),
    Column("name", String(100)),
    Column("password", String()),
    Column("is_active", Boolean(), default=True),
    Column("time_create_user", TIMESTAMP, default=datetime.utcnow),
)


# tokens = Table(
#     "tokens",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column(
#         "token",
#         UUID(as_uuid=False),
#         server_default=sqlalchemy.text("uuid_generate_v4()"),
#         unique=True,
#         nullable=False,
#         index=True,
#     ),
#     Column("expires", DateTime()),
#     Column("user_id", ForeignKey("users.id")),
# )




# https://habr.com/ru/articles/513328/
#это ссылка с инфой по фаст апи по реге