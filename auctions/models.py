from django.contrib.auth.models import AbstractUser
from django.db import models

# at least three models in addition to the User model: one for auction listings, one for bids, and one for comments made on auction listings.

class User(AbstractUser):
    pass

# Model for Category. A new Category needs to be created by user to show up on the Category page.
class Category(models.Model):
    name = models.CharField(max_length=100, default="General")

    def __str__(self):
        return self.name


# Model for Auction Listing
class Listing(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    alive = models.BooleanField(default=True)
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=1000, default=None)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="all_listing")
    img = models.URLField(max_length=300, blank=True, null=True, default="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png") #image source from wiki
    currentPrice = models.FloatField()
    bidder = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name="bidder")
    watchers = models.ManyToManyField(User, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.owner}"

    class Meta:
        ordering = ['-post_date']


# Model for Bids
class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.FloatField()
    bid_date = models.DateTimeField(auto_now_add=True)


# Model for Comments
class Comments(models.Model):
    comment = models.TextField(max_length=500, blank=False)
    comment_date = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment} posted {self.comment_date}"

    class Meta:
        ordering = ['-comment_date']


# Model for Watchlist
class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchlist')

    def __str__(self):
        return f"{self.user} added {self.listing.title}"
