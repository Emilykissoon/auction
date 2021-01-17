from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<str:entry>", views.show, name="listing"),
    path("<str:entry>/watch", views.watch, name="watch"),
    path("<str:entry>/close", views.close, name="close"),
    path("<str:entry>/bid", views.bid, name="bid"),
    path("<str:entry>/comment", views.comment, name="comment")
]
