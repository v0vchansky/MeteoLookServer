from django.db import models

class Image(models.Model):
    desc = models.CharField(max_length = 150, db_index = True)
    ident = models.IntegerField(max_length = 255, db_index = True)

    def __str__(self):
        return '{}'.format(self.ident)