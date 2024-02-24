from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    TEST: bool
    TELEGRAM_BOT_TOKEN: str
    TIME_PERIOD: int
    API_ID: str
    API_HASH: str

    @property
    def DATABASE_URL_asyncpg(self):
        print(f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        print(f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def TEST_SQLITE_ASYNC(self):
        return 'sqlite+aiosqlite:///database.db'
    
    @property
    def TEST_SQLITE_SYNC(self):
        return 'sqlite:///database.db'
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')
    

settings = Settings()
