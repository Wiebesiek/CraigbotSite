from django.urls import path
from . import views
from . import ajax

# Primary website URLS
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('about', views.about, name='about'),
    path('logout', views.logout_view, name='logout'),
    path('createnewbot', views.create_new_bot, name='createnewbot'),
    path('view_bots', views.view_bots, name='view_bots'),
    path('ajax/delete_bot', ajax.delete_bot,),
    path('edit/<int:pk>', views.edit, name='edit'),
]
