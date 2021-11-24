from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path("sign_up", views.sign_up),
    path('magazines', views.magazines),
    path("sign_in", views.sign_in),
    path("magazines/create", views.create_magazine),
    path("magazines/<int:magazine_id>", views.show_mag),
    path("logout", views.logout),
    path("magazines/<int:magazine_id>/delete", views.delete),
    path("magazines/<int:magazine_id>/update", views.update),
    path("favorite/<int:magazine_id>", views.favorite),
    path("unfavorite/<int:magazine_id>", views.unfavorite),
    path("back", views.back)
]
