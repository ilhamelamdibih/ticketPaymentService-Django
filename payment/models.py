from django.db import models
from users.models import User


class Payment(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    commande_id = models.IntegerField()
    cardNumber = models.IntegerField()
    cvv = models.IntegerField()
    expirationDate = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    transactionDate = models.DateField()
