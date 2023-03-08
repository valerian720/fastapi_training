
import os
class KeyHolder(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(KeyHolder, cls).__new__(cls)
            with open('key.secret', 'r') as f:
                cls.instance.key = f.read()
        return cls.instance
    
class Settings:
    PROJECT_NAME:str = "Board"
    PROJECT_VERSION: str = "1.0.0"
    
    # ....
    # ....
    # DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    SECRET_KEY :str = KeyHolder().key
    ALGORITHM = "HS256"                         
    ACCESS_TOKEN_EXPIRE_MINUTES = 120  #in mins  


settings = Settings()