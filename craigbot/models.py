from django.db import models
from django.contrib.auth.models import User


class newBotRequest(models.Model):
    req_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,)
    city = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    search_query = models.CharField(max_length=255)
    price_min = models.IntegerField()
    price_max = models.IntegerField()
    craig_bot = models.ForeignKey('craigBot', on_delete=models.CASCADE, null=True)


class craigBot(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,)
    bot_id = models.AutoField(primary_key=True)
    newBotReq = models.ForeignKey(newBotRequest, on_delete=models.CASCADE)
    item_found = models.BooleanField()
    email_sent = models.BooleanField()
    search_url = models.CharField(max_length=255)  # used for GET request with prices QS
    price_min = models.IntegerField()
    price_max = models.IntegerField()
    search_query = models.CharField(max_length=255)
    # if result found, this hyperlink will be what is sent in email.
    hyperlink_for_result_found = models.CharField(max_length=511)
    date_created = models.DateTimeField(auto_now_add=True)
