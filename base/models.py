from django.db import models
from django.contrib.auth.models import User 
from django.db.models.deletion import CASCADE

# Create your models here.

class DataTransactions(models.Model):
    user = models.CharField(max_length=25, default=None)
    Data_amount = models.IntegerField(default=None)
    TransactionID = models.CharField(max_length=200)
    Credit = models.BooleanField(default=False)
    Timestamp = models.DateTimeField(auto_now_add=True)
    To_wallet = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-Timestamp']
    
    def __str__(self):
        return self.user 
    
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=25, default=None)
    Last_Name = models.CharField(max_length=25, default=None)
    Data_balance = models.IntegerField(null=True, default=0)
    Phone_number = models.CharField(max_length=25, default=None)
    City = models.CharField(max_length=100, default=None)
    Gender = models.CharField(max_length=15, default=None)
    
    def __str__(self):
        return self.user.username


class DataBundle(models.Model):
    Amount = models.IntegerField(default=0)
    Price = models.FloatField(default=0.0)

    