from django.db import models


class Transaction(models.Model):
    wallet_address = models.CharField(max_length=255)
    tx_hash = models.CharField(max_length=255, unique=True, null=True, blank=True)
    status = models.CharField(max_length=50)  
    timestamp = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.wallet_address} - {self.status} - {self.tx_hash}"
