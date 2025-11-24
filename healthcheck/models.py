from django.db import models


# class HealthDatabase(models.Model):
#     alias = models.CharField(max_length=50, unique=True)
#     type = models.CharField(max_length=20, default="mssql")
#     name = models.CharField(max_length=100)
#     user = models.CharField(max_length=100)
#     password = models.CharField(max_length=200)
#     host = models.CharField(max_length=255)
#     port = models.PositiveIntegerField(default=1433)
#     api_url = models.CharField(max_length=255)
#     api_login = models.CharField(max_length=100)
#     api_pass = models.CharField(max_length=100)
#     is_enabled = models.BooleanField(default=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.alias


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
