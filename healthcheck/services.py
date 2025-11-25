from django.core.exceptions import ObjectDoesNotExist

from app import settings
from healthcheck.healthchecker import HealthCheckerSQLMirrorSync
from django.core.cache import cache
from django.utils import timezone
from healthcheck.models import HealthDatabase

from app.db_config import ensure_db_alias_configured


def cache_key_for_alias(alias: str) -> str:
    return f"healthcheck:{alias}"


def run_mirror_check_for_alias(alias: str) -> dict:
    try:
        cfg = HealthDatabase.objects.get(alias=alias, is_enabled=True)
    except ObjectDoesNotExist:
        result = {
            "alias": alias,
            "ok": False,
            "status": "not_configured",
            "checked_at": timezone.now().isoformat(),
            "message": f"Alias '{alias}' not found or disabled in HealthDatabase",
            "api_timestamp": None,
            "mirror_timestamp": None,
        }
        cache.set(cache_key_for_alias(alias), result, timeout=60 * 60)
        return result

    ensure_db_alias_configured(cfg)

    checker = HealthCheckerSQLMirrorSync(
        db_alias=cfg.alias,
        api_url=cfg.api_url,
        api_login=cfg.api_login,
        api_pass=cfg.api_pass,
        sync_wait_seconds=100,
    )

    result = checker.check_mirror_synced()
    cache.set(cache_key_for_alias(alias), result, timeout=60 * 60)
    return result

def iter_health_db_aliases():
    return list(
        HealthDatabase.objects.filter(is_enabled=True)
        .values_list("alias", flat=True)
    )
