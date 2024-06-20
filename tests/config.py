# config.py
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://paci:Gihanga51@localhost/smart_waste_management_test"
    )
    SECRET_KEY = "test_secret_key"
    WTF_CSRF_ENABLED = False
