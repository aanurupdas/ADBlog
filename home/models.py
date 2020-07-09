from django.db import models

# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=122)
    content = models.TextField()
    DateTime = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message From '+ self.name
