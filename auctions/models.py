from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORY_CHOICES = [
        ("Fashion", "Fashion"),
        ("Toys", "Toys"),
        ("Electronics", "Electronics"),
        ("Home", "Home"),
        ("Technology", "Technology"),
        ("Art/Culture", "Art/Culture"),
    ]

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=240)
    start_bid = models.IntegerField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="listings"
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="won_auctions",
    )

    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("removed", "Removed"), ("won", "Won")],
        default="active",
    )

    def current_price(self):
        """Return the highest bid, or the starting bid if none exist."""
        highest_bid = self.bids.order_by("-amount").first()
        return highest_bid.amount if highest_bid else self.start_bid

    def remove(self):
        """Force remove listing regardless of bids"""
        self.status = "removed"
        self.winner = None
        self.closed_at = timezone.now()
        self.save()

    def close(self):
        """
        Close auction:
        - If bids exist → mark as 'won' and assign winner
        - If no bids → mark as 'removed'
        """
        highest_bid = self.bids.order_by("-amount").first()
        if highest_bid:
            self.status = "won"
            self.winner = highest_bid.bidder
        else:
            self.status = "removed"
            self.winner = None
        self.closed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.title} ({self.category})"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} bid {self.amount} on {self.listing.title}"


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"
