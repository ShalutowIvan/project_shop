class Paginator:
    def __init__(self, limit: int = 10, skip: int = 0):
        self.limit = limit
        self.skip = skip

a = Paginator()

print(a.__dict__)

alembic.ini
sqlalchemy.url = postgresql+asyncpg://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s?async_fallback=True




config = context.config

config.set_main_option("sqlalchemy.url", str(DATABASE_URL))



# section = config.config_ini_section#это для передачи в файл alembic.ini данных о пользователе БД
# config.set_section_option(section, "DB_HOST", DB_HOST)
# config.set_section_option(section, "DB_PORT", DB_PORT)
# config.set_section_option(section, "DB_PASS", DB_PASS)
# config.set_section_option(section, "DB_USER", DB_USER)
# config.set_section_option(section, "DB_NAME", DB_NAME)



target_metadata = Base.metadata


sys.path.append(os.path.join(sys.path[0], 'src'))#это нужно для миграций, потому что файл env.py не видит папку src