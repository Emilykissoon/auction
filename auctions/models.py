from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.id}: {self.username}"


class Listings(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    title = models.TextField()
    description = models.TextField()
    # bid = models.ForeignKey(Bids, on_delete=models.CASCADE)
    img = models.TextField(null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch", null=True, blank=True)
    open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user_id}\t Listing: {self.title}({self.id})\t{self.description}\t {self.img}"


class Bids(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bid")
    bid = models.FloatField()
    bidder = models.TextField(default='')

    def __str__(self):
        return f"{self.listing.id}: {self.bid}"


class Comments(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing")
    comment = models.TextField()
    commenter = models.TextField()

    def __str__(self):
        return f"{self.commenter}: {self.comment}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="u")
    entry = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}: {self.entry} active: {self.active}"
