# Main settings
MAX_PROJECT_NAME: int = 100
MIN_INVESTED_AMOUNT: int = 1
MIN_PASSWORD_LENGTH: int = 3

# Auth settings
JWT_TOKEN_LIFETIME: int = 3600
JWT_TOKEN_URL: str = 'auth/jwt/login'
JWT_BACKEND_NAME: str = 'jwt'

# Google spreadsheets settings
FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEETS_URL = 'https://docs.google.com/spreadsheets/d/'
