from celery import shared_task, group
from .services import run_mirror_check_for_alias, iter_health_db_aliases


@shared_task
def task_check_mirror_for_alias(alias: str):
    return run_mirror_check_for_alias(alias)


@shared_task
def task_schedule_all_mirrors():
    aliases = iter_health_db_aliases()
    if not aliases:
        print("[healthcheck] No enabled HealthDatabase entries found.")
        return

    job = group(task_check_mirror_for_alias.s(alias) for alias in aliases)
    job()
