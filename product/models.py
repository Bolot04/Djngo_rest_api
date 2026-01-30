from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True,blank=True)
    price = models.IntegerField(default=100)
    category = models.ForeignKey(
        Category,on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        return f"{self.title}"

CHOICES = (
    (i, i) for i in range(1, 6)
)


class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='reviews'
    )
    stars = models.IntegerField(choices=CHOICES, default=0)

    def __str__(self):
        return f"{self.text}"