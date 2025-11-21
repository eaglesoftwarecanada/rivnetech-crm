import json
import pyodbc
from decouple import config

DB_CREDS = json.loads(config('DB_CREDS').replace("'", '"'))

def build_db_config(info):
    return {
        'ENGINE': 'mssql',
        'NAME': info['NAME'],
        'USER': info['USER'],
        'PASSWORD': info['PASSWORD'],
        'HOST': info.get('HOST', 'localhost'),
        'PORT': info.get('PORT', 1433),
        'OPTIONS': {
            'unicode_results': True,
            'driver': 'ODBC Driver 17 for SQL Server',
            'setdecoding': [
                {'sqltype': pyodbc.SQL_CHAR, 'encoding': 'utf-8'},
                {'sqltype': pyodbc.SQL_WCHAR, 'encoding': 'utf-8'},
            ],
            'setencoding': [{'encoding': 'utf-8'}],
        },
    }

DATABASES = {alias: build_db_config(cfg) for alias, cfg in DB_CREDS.items()}