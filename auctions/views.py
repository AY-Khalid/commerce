from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .forms import ListingForm

from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.filter(status="active")
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user  # 👈 auto detect user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()

    return render(request, "auctions/create_listing.html", {"form": form})


# @login_required
# def watchlist(request, id):
#     listing = Listing.objects.get(pk=id)
#     bidder = {listing.start_bid:listing.owner}
#     if request.method == 'POST':
#         current_bid = request.form.get["bid_amount"]:
#         bidder.add(current_bid)
#     return render(request, "auctions/watchlist.html", {
#         "listings": listing
#     })


@login_required
def watchlist(request, id):
    listing = get_object_or_404(Listing, pk=id)

    if request.method == "POST":
        if "bid_amount" in request.POST:  # Place a bid
            bid_amount = request.POST.get("bid_amount")
            try:
                bid_amount = float(bid_amount)
            except ValueError:
                messages.error(request, "Invalid bid amount.")
                return redirect("watchlist", id=id)

            current_price = listing.current_price()
            highest_bid = listing.bids.order_by("-amount").first()

            if highest_bid and highest_bid.bidder == request.user:
                messages.error(request, "You are already the highest bidder.")
                return redirect("watchlist", id=id)

            if bid_amount > current_price:
                Bid.objects.create(
                    listing=listing, bidder=request.user, amount=bid_amount
                )
                messages.success(request, f"You placed a bid of ${bid_amount}!")
            else:
                messages.error(
                    request, f"Your bid must be higher than ${current_price}."
                )
            return redirect("watchlist", id=id)

        elif "remove_listing" in request.POST:  # Owner removes auction
            if request.user == listing.owner:
                listing.close()
                messages.success(request, f"The listing '{listing.title}' was closed.")
                return redirect("history")
            else:
                messages.error(request, "Only the owner can remove this listing.")
                return redirect("watchlist", id=id)
        elif "comment" in request.POST:
            content = request.POST.get("comment")
            if content.strip():
                Comment.objects.create(
                    listing=listing,
                    user=request.user,
                    content=content
                )
                messages.success(request, "Your comment was added!")
            else:
                messages.error(request, "Comment cannot be empty.")
            return redirect("watchlist", id=id)

    # Context
    highest_bid = listing.bids.order_by("-amount").first()
    user_bids = listing.bids.filter(bidder=request.user)
    user_is_highest = highest_bid and highest_bid.bidder == request.user

    if user_is_highest:
        bid_status = "Your bid is the current bid"
    elif user_bids.exists():
        bid_status = "You are not currently the highest bidder"
    else:
        bid_status = "You have not bid yet"

    return render(
        request,
        "auctions/watchlist.html",
        {
            "listing": listing,
            "count_current_bid": listing.bids.count(),
            "current_price": listing.current_price(),
            "bid_status": bid_status,
            "comments": listing.comments.order_by("-created_at"),
        },
    )


@login_required
def history(request):
    listings = Listing.objects.all().order_by("-created_at")
    return render(request, "auctions/history.html", {"listings": listings})


@login_required
def toggle_watchlist(request, id):
    listing = get_object_or_404(Listing, pk=id)

    if request.user in listing.watchers.all():
        listing.watchers.remove(request.user)
        messages.info(request, f"Removed '{listing.title}' from your watchlist.")
    else:
        listing.watchers.add(request.user)
        messages.success(request, f"Added '{listing.title}' to your watchlist.")

    return redirect("watchlist", id=id)


@login_required
def my_watchlist(request):
    listings = request.user.watchlist.all()  # all items the user is watching
    return render(request, "auctions/my_watchlist.html", {"listings": listings})
