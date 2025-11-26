import copy

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

    try:
        base = copy.deepcopy(connections.databases["default"])
    except KeyError:
        base = {}

    base.update(
        {
            "ENGINE": engine,
            "NAME": cfg.name,
            "USER": cfg.db_user,
            "PASSWORD": cfg.db_password,
            "HOST": cfg.host,
            "PORT": cfg.port,
        }
    )

    if engine == "mssql":
        options = base.get("OPTIONS", {})
        options.update(build_mssql_options())
        base["OPTIONS"] = options

    settings.DATABASES[alias] = base
    connections.databases[alias] = base

    return alias

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
