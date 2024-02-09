from django.db import models
from owner.models import Item
from user.models import CustomUser

class Cart(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_added=models.DateField(auto_now_add=True)

    def subtotal(self):
        return self.quantity*self.item.price


    def __str__(self):
        return self.item.item_name

