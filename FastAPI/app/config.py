from pydantic_settings import BaseSettings
'''We use BaseSettings to set the environment variables for the database, secret key, and other settings.'''
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    expiration_time: int
    class Config:
        env_file = ".env"
        '''Esto importa el archivo que creamos donde tenemos los valores de las variables de entorno.'''
        
settings = Settings()

