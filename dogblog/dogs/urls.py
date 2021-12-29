# from django.conf.urls import url
from django.urls import path, re_path
from .views import *


urlpatterns = [
    # path('', index, name='home'),
    path('', DogsHome.as_view(), name='home'),
    path('about/', about, name='about'),
    # path('addpage/', addpage, name='add_page'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    # path('post/<slug:post_slug>/', show_post, name='post'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    # path('category/<slug:cat_slug>/', show_category, name='category'),
    path('category/<slug:cat_slug>/', DogsCategory.as_view(), name='category'),
]