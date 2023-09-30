from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    imageURL = models.CharField(max_length=500)
    price = models.FloatField()
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")

    def __str__(self):
        return self.title


class Bid(models.Model):
    auctioneer = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True, null=False, related_name="auctioneer")
    product = models.ForeignKey(Listing, on_delete=models.RESTRICT, blank=True, null=False, related_name="product")
    bid_price = models.FloatField()


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True, null=False, related_name="user_id")
    listing_id = models.ForeignKey(Listing, on_delete=models.RESTRICT, blank=True, null=False, related_name="listing_id")
    commentary = models.CharField(max_length=255)

