from django.db import models



class Account(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='user_account')
    currency_code = models.CharField(max_length=3, blank=False, default='USD')
    signup_location = models.CharField(max_length=64, blank=True, null=True)
    signup_ip = models.CharField(max_length=45, blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True)
    exchanges = models.ManyToManyField('crypto.CryptoExchange', blank=True)

    def __str__(self):
        return self.user.username


class Config(models.Model):
    key = models.CharField(max_length=64, unique=True, null=False, blank=False)
    value = models.CharField(max_length=256)



class Log(models.Model):
    table = models.CharField(max_length=32)
    timestamp = models.DateTimeField()




