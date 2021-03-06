from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Listing(models.Model):
    alive = models.BooleanField(default=True)
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=1000, blank=True, null=True, default=None)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="all_listing")
    img = models.URLField(max_length=300)
    startingBid = models.FloatField()
    currentBid = models.FloatField(blank=True, null=True)
    bidder = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name="winner")
    watchers = models.ManyToManyField(User, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE, related_name="category", default=None)

    def __str__(self):
        return f"{self.title} by {self.owner}"

    class Meta:
        ordering = ['-post_date']

class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.FloatField()
    bid_date = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    comment = models.TextField(max_length=500, blank=False)
    comment_date = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment} posted {self.comment_date}"

    class Meta:
        ordering = ['-comment_date']

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchlist')

    def __str__(self):
        return f"{self.user} added {self.listing,title}"
