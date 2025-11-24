from app import settings
from healthcheck.healthchecker import HealthCheckerSQLMirrorSync
from django.core.cache import cache

# from app.healthcheck.models import HealthDatabase


def cache_key_for_alias(alias: str) -> str:
    return f"healthcheck:{alias}"

# def run_mirror_check_for_alias(alias: str) -> dict:
#     cfg = HealthDatabase.objects.filter(alias=alias).first()
#     if not cfg:
#         return {
#             "alias": alias,
#             "ok": False,
#             "status": "not_configured",
#             "checked_at": None,
#             "message": f"Alias '{alias}' not found in HEALTHCHECK_DBS",
#         }
#
#     checker = HealthCheckerSQLMirrorSync(
#         db_alias=cfg.alias,
#         api_url=cfg.api_url,
#         api_login=cfg.api_login,
#         api_pass=cfg.api_pass,
#         sync_wait_seconds=300,
#     )
#
#     result = checker.check_mirror_synced()
#
#     cache.set(cache_key_for_alias(alias), result, timeout=60 * 60)
#
#     return result

def run_mirror_check_for_alias(alias: str) -> dict:
    cfg = settings.HEALTHCHECK_DBS.get(alias)
    if not cfg:
        return {
            "alias": alias,
            "ok": False,
            "status": "not_configured",
            "checked_at": None,
            "message": f"Alias '{alias}' not found in HEALTHCHECK_DBS",
        }

    checker = HealthCheckerSQLMirrorSync(
        db_alias=cfg["db_alias"],
        api_url=cfg["api_url"],
        api_login=cfg["api_login"],
        api_pass=cfg["api_pass"],
        sync_wait_seconds=300
    )

    result = checker.check_mirror_synced()

    cache.set(cache_key_for_alias(alias), result, timeout=60 * 60)

    return result


def iter_health_db_aliases():
    return list(getattr(settings, "HEALTHCHECK_DBS", {}).keys())