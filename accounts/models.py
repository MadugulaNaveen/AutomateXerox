from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    order_id = models.CharField(max_length=100,null=True)
    cost = models.FloatField()
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',null=True)    

class Document(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents',null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='Order')
    xerox_type = models.CharField(max_length=100,null=True,default='Single Side')
    copies = models.IntegerField(null=True,default=1)
    def to_dict(self):
        # Convert the model fields to a dictionary
        return {
            'name':self.name,
            'file':self.file.url,
            'user':self.user,
            'order':self.order,
        }

class UserDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,)
