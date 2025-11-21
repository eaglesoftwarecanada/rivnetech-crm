from django.db import models


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