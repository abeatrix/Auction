from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import Item_Form, Comment_Form, Bid_Form
from .models import User, Listing, Category, Bids
from django.contrib.auth.decorators import login_required

def index(request):
    context = {"listings": Listing.objects.filter(alive=True)}
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

def listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        listing.alive = False
        listing.save()
        return redirect("/")
    bid_form = Bid_Form()
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        listing = None
    context = {'listing': listing, "form": bid_form}
    return render(request, 'auctions/listing.html', context)

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

def bid(request, listing_id):
    if request.method == "POST":
        form = Bid_Form(request.POST)
        if form.is_valid():
            return redirect("listing", listing_id)

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
