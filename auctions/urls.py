from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist/<int:id>", views.watchlist, name="watchlist"),
    path("history/", views.history, name="history"),
    path(
        "toggle_watchlist/<int:id>/", views.toggle_watchlist, name="toggle_watchlist"
    ),  # 👈 new
    path("my_watchlist/", views.my_watchlist, name="my_watchlist"),  # 👈 new
]
