from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image_file = models.ImageField(upload_to="uploads/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.price} x {self.quantity}"
