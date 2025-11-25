import pyodbc

from app import settings
from healthcheck.models import HealthDatabase

from django.db import connections

def get_engine_from_type(db_type: str) -> str:
    db_type = (db_type or '').lower()

    if db_type.startswith('postgr'):
        return 'django.db.backends.postgresql'
    if db_type in ('mssql', 'sqlserver'):
        return 'mssql'
    if db_type in ('mysql',):
        return 'django.db.backends.mysql'
    raise ValueError(f"Unknown DB_TYPE: {db_type}")


def build_mssql_options():
    return {
        'unicode_results': True,
        'driver': 'ODBC Driver 17 for SQL Server',
        'setdecoding': [
            {'sqltype': pyodbc.SQL_CHAR, 'encoding': 'utf-8'},
            {'sqltype': pyodbc.SQL_WCHAR, 'encoding': 'utf-8'},
        ],
        'setencoding': [{'encoding': 'utf-8'}],
    }

def ensure_db_alias_configured(cfg: HealthDatabase) -> str:
    alias = cfg.alias

    if alias in connections.databases:
        return alias

    engine = get_engine_from_type(cfg.type)

    db_config = {
        "ENGINE": engine,
        "NAME": cfg.name,
        "USER": cfg.db_user,
        "PASSWORD": cfg.db_password,
        "HOST": cfg.host,
        "PORT": cfg.port,
    }

    if engine == "mssql":
        db_config["OPTIONS"] = build_mssql_options()

    settings.DATABASES[alias] = db_config
    connections.databases[alias] = db_config

    return alias

# def build_databases():
#     databases = {}
#
#     db_type = config("DB_TYPE", default="postgres")
#     engine = get_engine_from_type(db_type)
#
#     default_cfg = {
#         "ENGINE": engine,
#         "NAME": config("DB_NAME"),
#         "USER": config("DB_USER"),
#         "PASSWORD": config("DB_PASS"),
#         "HOST": config("DB_HOST", default="localhost"),
#         "PORT": config("DB_PORT", cast=int, default=5432),
#     }
#
#     if engine == "mssql":
#         default_cfg["OPTIONS"] = build_mssql_options()
#
#     databases["default"] = default_cfg
#
#     health_creds = _load_health_creds()
#
#     for alias, params in health_creds.items():
#         db_engine = get_engine_from_type(params.get("TYPE", "mssql"))
#
#         cfg = {
#             "ENGINE": db_engine,
#             "NAME": params["NAME"],
#             "USER": params["USER"],
#             "PASSWORD": params["PASSWORD"],
#             "HOST": params.get("HOST", "localhost"),
#             "PORT": params.get("PORT", 1433),
#         }
#
#         if db_engine == "mssql":
#             cfg["OPTIONS"] = build_mssql_options()
#
#         databases[alias] = cfg
#
#     return databases

def load_health_dbs():
    for entry in HealthDatabase.objects.filter(is_enabled=True):
        alias = entry.alias

        settings.DATABASES[alias] = {
            "ENGINE": get_engine_from_type(entry.type),
            "NAME": entry.name,
            "USER": entry.user,
            "PASSWORD": entry.password,
            "HOST": entry.host,
            "PORT": entry.port,
            "OPTIONS": build_mssql_options() if entry.TYPE == "mssql" else {},
        }
