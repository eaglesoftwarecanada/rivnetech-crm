from app import settings
from healthcheck.healthchecker import HealthCheckerSQLMirrorSync


def run_mirror_check_for_alias(alias: str):
    cfg = settings.HEALTHCHECK_DBS.get(alias)
    if not cfg:
        print(f"[healthcheck] Alias '{alias}' not found in HEALTHCHECK_DBS")
        return

    checker = HealthCheckerSQLMirrorSync(
        db_alias=cfg["db_alias"],
        api_url=cfg["api_url"],
        api_login=cfg["api_login"],
        api_pass=cfg["api_pass"],
        sync_wait_seconds=300
    )

    checker.check_mirror_synced()


def iter_health_db_aliases():
    return list(getattr(settings, "HEALTHCHECK_DBS", {}).keys())