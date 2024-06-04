from urllib.parse import quote_plus

class Config:
    username = 'shipping_user'
    password = quote_plus('@l@niWEB2020!')  # Encode special characters
    host = 'localhost'
    database = 'shipping_calculator'

    SQLALCHEMY_DATABASE_URI = f'mysql+mysqldb://{username}:{password}@{host}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 's3cr3t_k3y_f0r_sh1pp1ng_c4lc'
