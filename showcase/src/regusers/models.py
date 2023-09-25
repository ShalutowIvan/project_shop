from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Float, Boolean, Text, Table, Column


metadata = MetaData()

# user = Table(
#     "user", 
#     metadata,

#     Column("id", Integer, primary_key=True),
    
#     Column("username", String, nullable=False),
#     # Column("is_staff ),
#     Column("is_active", Boolean,  nullable=False),
    
#     Column("password", String, nullable=False),
    
# )




organization = Table(
    "organization",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name_org", String, nullable=False),
    Column("inn", Integer, default=0),
    Column("kpp", Integer, default=0),
    Column("ogrn", Integer, default=0),#пароли нужно хранить в захешированном виде всегда, это для безопасности. Без ключа в захеришрованном виде нельзя его расшифровать
    Column("working_mode", String, default="_"),
    Column("about", Text, default="_"),
    Column("adres", String, default="_"),
    Column("phone", Integer, default=0),#utcnow для разных часовых поясов в случае расположения бд и пользователя в разных часовых поясах, это универсальный часовой пояс. При создании будет автоматом записываться текущее время создания поля. 
    Column("email_name", String, nullable=False),
    Column("telegram", String, default="_"),
    Column("whatsApp", String, default="_"),
)





