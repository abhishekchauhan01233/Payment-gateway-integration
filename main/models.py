from django.db import models

# Create your models here.
class donate_model(models.Model):
    name = models.CharField(max_length=200, blank=False)
    phone = models.BigIntegerField()
    email = models.EmailField(max_length=320, blank=False)
    amount = models.BigIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'DONATIONS'

class transaction_model(models.Model):
    made_by = models.CharField(max_length=200, blank=False)
    made_on = models.DateField(max_length=50)
    amount = models.BigIntegerField()
    order_id = models.CharField(unique=True, max_length=1000, null=True, blank=True)
    checksum = models.CharField(max_length=1000, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%doDR') + str(self.id)
        return super().save(*args, **kwargs)