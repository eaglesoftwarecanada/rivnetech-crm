import requests

import time
from datetime import datetime

import humanize
from app import settings
from healthcheck.models import Inventry
from utils.ebms_requests import BasicAUTHRequest


class HealthCheckerSQLMirrorSync(BasicAUTHRequest):
    descr_1 = "Record for health check SQL mirror sync! Do not delete!"
    tree_id = "1"

    def __init__(
        self,
        db_alias,
        api_url,
        api_login,
        api_pass,
        sync_wait_seconds = 300,
    ):
        super().__init__(
            login=api_login,
            password=api_pass
        )

        self.db_alias = db_alias
        self.url = f"{api_url.rstrip('/')}/Odata/INVENTRY"
        self.sync_wait_seconds = sync_wait_seconds

    def send_message_to_discord_webhook(self, message):
        print(f"[{self.db_alias}] {message}")
        webhook_url = getattr(settings, "SERVER_HEALTH_DISCORD_WEBHOOK_URL", None)

        if not webhook_url:
            print("Discord webhook is not configured")
            return

        response = requests.post(webhook_url, json={"content": f'{self.db_alias} / {message}'})
        if response.status_code not in (200, 204):
            print(f"{response.status_code} / {response.text}")

    def send_notification_api_down(self, status_code):
        estimate_down_time = self.estimate_down_time()
        message = f"EBMS API failed with status code: {status_code} for approximately {estimate_down_time}"
        self.send_message_to_discord_webhook(message)

    def send_notification_sync_down(self):
        estimate_down_time = self.estimate_down_time()
        message = f"SQL Mirror Sync has been down for approximately {estimate_down_time}"
        self.send_message_to_discord_webhook(message)

    def get_test_record(self, descr_1):
        search_url = f"{self.url}?$filter=DESCR_1 eq '{descr_1}'"
        return self.get(search_url)

    def create_test_record(self, descr_1, descr_2):
        data = {
            "TREE_ID": self.tree_id,
            "DESCR_1": descr_1,
            "DESCR_2": descr_2
        }
        return self.post(self.url, data)

    def patch_inventry(self, autoid, descr_2):
        data = {"DESCR_2": descr_2}
        return self.patch(f"{self.url}('{autoid}')", data)

    def delete_test_record(self, autoid):
        return self.delete(f"{self.url}('{autoid}')")

    def update_or_create_test_record(self, descr_1):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")

        get_response = self.get_test_record(descr_1)

        if get_response.status_code != 200:
            self.send_notification_api_down(get_response.status_code)
            return None, None

        test_records = get_response.json().get('value', [])
        autoid_w_timestamp = None

        if not test_records:
            create_response = self.create_test_record(descr_1, timestamp)
            if create_response.status_code != 200:
                self.send_notification_api_down(create_response.status_code)
                return None, None
            autoid_w_timestamp = create_response.json().get('AUTOID')
        else:
            for idx, test_record in enumerate(test_records):
                autoid = test_record.get('AUTOID')
                if idx == 0:
                    patch_response = self.patch_inventry(autoid, timestamp)
                    if patch_response.status_code != 200:
                        self.send_notification_api_down(patch_response.status_code)
                        return None, None
                    autoid_w_timestamp = autoid
                else:
                    delete_response = self.delete_test_record(autoid)
                    if delete_response.status_code != 204:
                        self.send_notification_api_down(delete_response.status_code)
                        return None, None

        return autoid_w_timestamp, timestamp

    def get_timestamp_test_record_from_mirror(self, autoid=None):
        qs = Inventry.objects.using(self.db_alias)
        if autoid:
            inventry = qs.filter(autoid=autoid).first()
        else:
            inventry = qs.filter(descr_1=self.descr_1).first()
        return inventry.descr_2 if inventry else None

    def estimate_down_time(self):
        mirror_timestamp = self.get_timestamp_test_record_from_mirror()
        if not mirror_timestamp:
            return "unknown time (no test record)"

        mirror_time = datetime.strptime(mirror_timestamp, "%Y-%m-%d %H:%M:%S:%f")
        now = datetime.now()
        delta = now - mirror_time
        return humanize.precisedelta(delta, minimum_unit="minutes", format="%0.0f")

    def check_mirror_synced(self):
        autoid_w_timestamp, timestamp = self.update_or_create_test_record(self.descr_1)
        if not autoid_w_timestamp:
            return

        time.sleep(self.sync_wait_seconds)

        mirror_timestamp = self.get_timestamp_test_record_from_mirror(autoid_w_timestamp)
        if mirror_timestamp != timestamp:
            self.send_notification_sync_down()
        else:
            print(f"{self.db_alias} | SQL Mirror Sync is OK")

    def is_mirror_synced_last_35_minutes(self) -> bool:
        mirror_timestamp = self.get_timestamp_test_record_from_mirror()
        if not mirror_timestamp:
            return False

        now = datetime.now()
        mirror_time = datetime.strptime(mirror_timestamp, "%Y-%m-%d %H:%M:%S:%f")
        delta = now - mirror_time
        return delta.total_seconds() < 2100
