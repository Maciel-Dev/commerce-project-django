from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing
from .models import Category


def index(request):
    return render(request, "auctions/index.html")


def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create.html",
                      {
                          'category_list': Category.objects.all()
                      })

    elif request.method == "POST":
        title = request.POST["title"]
        description = request.POST["desc"]
        imageURL = request.POST["imageTxt"]
        price = request.POST["price"]
        category = request.POST["category"]
        user = request.user

        categoryObj = Category.objects.get(name=category)

        newListing = Listing(
            title=title,
            description=description,
            imageURL=imageURL,
            price=price,
            active=True,
            owner=user,
            category=categoryObj
        )

        newListing.save()
        return HttpResponseRedirect(reverse(index))


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