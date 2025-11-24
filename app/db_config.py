import ast

import pyodbc
from decouple import config

from app import settings
# from healthch
# eck.models import HealthDatabase


class DBConfigError(Exception):
    pass

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

def _load_health_creds():
    raw_health = config("DB_CREDS_HEALTH", default="{}")
    try:
        creds = ast.literal_eval(raw_health)
        if not isinstance(creds, dict):
            raise ValueError("DB_CREDS_HEALTH must be a dict-like structure")
        return creds
    except Exception as exc:
        raise DBConfigError(f"Failed to parse DB_CREDS_HEALTH: {exc}") from exc

def build_databases():
    databases = {}

    db_type = config("DB_TYPE", default="postgres")
    engine = get_engine_from_type(db_type)

    default_cfg = {
        "ENGINE": engine,
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASS"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", cast=int, default=5432),
    }

    if engine == "mssql":
        default_cfg["OPTIONS"] = build_mssql_options()

    databases["default"] = default_cfg

    health_creds = _load_health_creds()

    for alias, params in health_creds.items():
        db_engine = get_engine_from_type(params.get("TYPE", "mssql"))

        cfg = {
            "ENGINE": db_engine,
            "NAME": params["NAME"],
            "USER": params["USER"],
            "PASSWORD": params["PASSWORD"],
            "HOST": params.get("HOST", "localhost"),
            "PORT": params.get("PORT", 1433),
        }

        if db_engine == "mssql":
            cfg["OPTIONS"] = build_mssql_options()

        databases[alias] = cfg

    return databases


def build_healthcheck_dbs():
    health_creds = _load_health_creds()
    result = {}

    for alias, params in health_creds.items():
        try:
            result[alias] = {
                "db_alias": alias,
                "api_url": params["API_URL"],
                "api_login": params["API_LOGIN"],
                "api_pass": params["API_PASS"],
            }
        except KeyError as exc:
            raise DBConfigError(
                f"Missing API_* key in DB_CREDS_HEALTH for alias '{alias}': {exc}"
            ) from exc

    return result

# def load_health_dbs():
#     for entry in HealthDatabase.objects.filter(is_enabled=True):
#         alias = entry.alias
#
#         settings.DATABASES[alias] = {
#             "ENGINE": get_engine_from_type(entry.type),
#             "NAME": entry.name,
#             "USER": entry.user,
#             "PASSWORD": entry.password,
#             "HOST": entry.host,
#             "PORT": entry.port,
#             "OPTIONS": build_mssql_options() if entry.TYPE == "mssql" else {},
#         }
