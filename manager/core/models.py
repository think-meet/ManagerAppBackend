from django.contrib.auth.models import AbstractUser
from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True,blank=False,null=False)
    password = models.CharField(blank=False, null=False)
    
    def __str__(self):
        return f"User id {self.id}, email {self.email}"
    
    @property
    def is_authenticated(self):
        """Ensures only authenticated users are marked as authenticated"""
        return hasattr(self, "_is_authenticated") and self._is_authenticated
    
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100,blank=False,null=False)
    item_required = models.BooleanField(default=False)
    item_cost = models.IntegerField(blank=False,null=False)
    item_stock = models.IntegerField(blank=False,null=False)
    min_quantity = models.IntegerField(blank=False,null=False)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    
    def __str__(self):
        return f"Item id {self.id}, name {self.item_name}"
    
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100,blank=False,null=False)
    item_cost = models.IntegerField(blank=False,null=False)
    transaction_date_time = models.CharField(max_length=100,blank=False,null=False)
    transaction_type = models.CharField(max_length=10,blank=False,null=False)
    transaction_units = models.IntegerField(blank=False,null=False)
    final_stock = models.IntegerField(blank=False,null=False)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")

    
    def __str__(self):
        return f"Transaction id {self.id}, name {self.item_name}"
    
class Token(models.Model):
    id = models.AutoField(primary_key=True)
    refresh_token = models.TextField(default="",unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens")
    
    def __str__(self):
        return f"Token id {self.id}, user {self.user.email}"
    
class Code(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.TextField(max_length=4)
    creation_epoch = models.IntegerField()
    expiry_epoch = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="codes")
    
    def __str__(self):
        return f"Code id {id}, user {self.user.email}"
    
class Connection(models.Model):
    id = models.AutoField(primary_key=True)
    connection_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="connection_from")
    connection_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="connection_to")
    
    def __str__(self):
        return f"Connection id {self.id}, from {self.connection_from.email} to {self.connection_to.email}"

