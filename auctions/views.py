from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listings, Bids, Comments, Watchlist

from .models import User


def index(request):
    listings = Listings.objects.filter(open=True)
    bids = Bids.objects.all()
    empty = False
    if not listings:
        empty = True
    return render(request, "auctions/index.html", {
        "listings": listings, "bids": bids, "empty": empty
    })


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


@login_required(login_url='login')
def new(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        img = request.POST["img"]
        l = Listings(user_id=request.user, title=title, description=description, img=img)
        l.save()
        b = Bids(listing=l, bid=bid)
        b.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/new.html")


def watchlist(request):
    w = Watchlist.objects.filter(user=request.user, active=True)
    listings = Listings.objects.all()
    bids = Bids.objects.all()
    empty = False
    if not w:
        empty = True
    return render(request, "auctions/watchlist.html", {
        "listings": listings, "watch": w, "bids": bids, "empty": empty
    })


def show(request, entry):
    l = Listings.objects.get(id=entry)
    check = False
    u = False
    comments = Comments.objects.filter(listing=l)
    if request.user.is_authenticated:
        check = True
        if request.user == l.user_id:
            u = True
    b = Bids.objects.get(listing=l)
    w = None
    if check:
        try:
            w = Watchlist.objects.get(user=request.user, entry=entry)
        except Watchlist.DoesNotExist:
            w = None
    e = True
    if not w:
        e = False
    return render(request, "auctions/listing.html", {
        "list": l, "check": check, "u": u,
        "comments": comments, "bid": b, "watch": e, "w": w
    })


@login_required(login_url='login')
def watch(request, entry):
    if request.method == "POST":
        if request.POST.get('add'):
            try:
                w = Watchlist.objects.get(user=request.user, entry=entry)
            except Watchlist.DoesNotExist:
                w = None
            if w is None:
                w = Watchlist(user=request.user, entry=entry)
                w.save()
            else:
                w.active = True
                w.save(update_fields=["active"])
        else:
            w = Watchlist.objects.get(user=request.user, entry=entry)
            w.active = False
            w.save(update_fields=["active"])
        return HttpResponseRedirect(reverse("listing", args=[entry]))


def close(request, entry):
    if request.method == "POST":
        l = Listings.objects.get(id=entry)
        b = Bids.objects.get(listing=l)
        if b.bidder == '':
            u = l.user_id
        else:
            u = User.objects.get(username=b.bidder)
        l.winner = u
        l.open = False
        l.save(update_fields=["winner", "open"])
        return HttpResponseRedirect(reverse("listing", args=[entry]))


@login_required(login_url='login')
def bid(request, entry):
    if request.method == "POST":
        b = request.POST["bid"]
        l = Listings.objects.get(id=entry)
        temp = Bids.objects.get(listing=l)
        temp.bid = b
        temp.bidder = request.user.username
        temp.save(update_fields=["bid", "bidder"])
        return HttpResponseRedirect(reverse("listing", args=[entry]))


@login_required(login_url='login')
def comment(request, entry):
    if request.method == "POST":
        com = request.POST["comment"]
        listing = Listings.objects.get(id=entry)
        c = Comments(listing=listing, comment=com, commenter=str(request.user.username))
        c.save()
        return HttpResponseRedirect(reverse("listing", args=[entry]))
