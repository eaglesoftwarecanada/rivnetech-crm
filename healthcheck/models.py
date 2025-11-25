from django.db import models
from .crypto import encrypt_str, decrypt_str


class HealthDatabase(models.Model):
    alias = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, default="mssql")
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=255)
    port = models.PositiveIntegerField(default=1433)
    db_user = models.CharField(max_length=200)
    api_url = models.CharField(max_length=255)
    api_login = models.CharField(max_length=200)
    _db_password = models.CharField(max_length=500, db_column="db_password")
    _api_pass = models.CharField(max_length=500, db_column="api_pass")
    is_enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Health DB"
        verbose_name_plural = "Health DBs"

    def __str__(self):
        return self.alias

    @property
    def db_password(self) -> str | None:
        return decrypt_str(self._db_password)

    @db_password.setter
    def db_password(self, value: str | None):
        self._db_password = encrypt_str(value)

    @property
    def api_pass(self) -> str | None:
        return decrypt_str(self._api_pass)

    @api_pass.setter
    def api_pass(self, value: str | None):
        self._api_pass = encrypt_str(value)


class Inventry(models.Model):
    recno5 = models.IntegerField(db_column='RECNO5')
    id = models.CharField(db_column='ID', max_length=24)
    tree_id = models.CharField(db_column='TREE_ID', max_length=5)
    descr_1 = models.CharField(db_column='DESCR_1', max_length=80)
    descr_2 = models.CharField(db_column='DESCR_2', max_length=80)
    autoid = models.CharField(db_column='AUTOID', unique=True, primary_key=True, max_length=16)

    class Meta:
        managed = False
        db_table = 'INVENTRY'
