import os

class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'xsslab')
    DB_USER = os.getenv('DB_USER', 'xssuser')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'secret')
    MAX_CONCURRENT_TESTS = int(os.getenv('MAX_CONCURRENT_TESTS', 2))  # Default to 2 concurrent tests

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"

config = Config()
