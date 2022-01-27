from django.db import models

# Create your models here.
# class Category(models.Model):
#     name = models.CharField(max_length=50)
#     def __str__(self):
#         return self.name

class Product(models.Model):
    name = models.CharField(max_length=150)
    original_price = models.FloatField()
    sale_price = models.FloatField()
    #category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    date_auto = models.DateField(auto_now=True)

    def __str__():
        return self.name