from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import Item_Form, Comment_Form, Bid_Form, Cat_Form
from .models import User, Listing, Category, Bids, WatchList, Comments
from django.contrib.auth.decorators import login_required

# Index Page that display a list of Listings
def index(request):
    listings = Listing.objects.filter(alive=True)
    context = {"listings": listings}
    return render(request, "auctions/index.html", context)


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Listing Page
def listing(request, listing_id):
    watchlist = WatchList.objects.filter(listing=listing_id).exists()
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        listing.alive = False
        listing.save()
        return redirect("/")
    try:
        listing = Listing.objects.get(id=listing_id)
        price = listing.currentPrice+0.1
        comments = Comments.objects.filter(listing_id=listing_id)
    except Listing.DoesNotExist:
        listing = None
    context = {'listing': listing, "comments": comments, "watchlist": watchlist, "price": price}
    return render(request, 'auctions/listing.html', context)


# Categories Index Page
def categories(request):
    cats = Category.objects.all()
    form = Cat_Form()
    if request.method == "POST":
        form = Cat_Form(request.POST)
        if form.is_valid():
            new_cat = form.save(commit=False)
            form.save()
            context = {"form": Item_Form()}
            return render(request, 'auctions/create.html', context)
    context = {"cats": cats, "form": form}
    return render(request, "auctions/categories.html", context)


# Category Index Page
def category(request, cat_id):
    cat = Category.objects.get(id=cat_id)
    listings = Listing.objects.filter(category=cat_id, alive=True)
    if request.method == "POST":
        listings = Listing.objects.filter(category=cat_id)
    context = {"cat": cat, "listings": listings}
    return render(request, "auctions/category.html", context)


# Create Listing
@login_required
def create(request):
    form = Item_Form()
    category = Category.objects.all()
    if request.method == "POST":
        form = Item_Form(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.owner = request.user
            new_item.save()
            return redirect("listing", listing_id=new_item.id)
        else:
            context = {"form": form, "category": category, "listings": listing, 'errors': form.errors}
            return render(request, 'auctions/create.html', context)
    listings = Listing.objects.filter(owner=request.user)
    context = {"form": form, "category": category, "listings": listing}
    return render(request, 'auctions/create.html', context)


# Place Bid on Listing
@login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        form = Bid_Form(request.POST)
        if form.is_valid():
            price = float(request.POST['bid'])
            current_price = listing.currentPrice
            if price > current_price:
                highest_bid = form.save(commit=False)
                highest_bid.bidder = request.user
                highest_bid.listing = listing
                highest_bid.save()
                listing.currentPrice = price
                listing.bidder = request.user
                listing.save()
            return redirect("listing", listing_id)

# Add Comment to Listing Page
@login_required
def comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        form = Comment_Form(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.listing = listing
            new_comment.save()
            return redirect("listing", listing_id=listing_id)
        else:
            context = {'listing': listing, "errors": form.errors}
            return render(request, 'auctions/listing.html', context)

# Add Listing to Watchlist
@login_required
def add(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        listing = WatchList(user=request.user, listing=item)
        listing.save()
        return redirect("listing", listing_id=listing_id)

# Remove Listing from Watchlist
@login_required
def remove(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        listing = request.user.watchlist.get(listing=item)
        listing.delete()
        return redirect("listing", listing_id=listing_id)

# Current User's Watchlist
@login_required
def watchlist(request):
    listings = request.user.watchlist.all()

    context = {"listings": listings}
    return render(request, "auctions/watchlist.html", context)
