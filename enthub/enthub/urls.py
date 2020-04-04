"""enthub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from ent import views as yct_views
from contact import views as contact_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('ent.urls', namespace="ent")),
    #path('', include('users.urls', namespace="users")),
    path('contact/', contact_views.contact_page, name="contact_page"),
    path('about/', yct_views.about, name="about"),
    
    path('login/', yct_views.user_login, name="user_login"),
    path('post_create/', yct_views.post_create, name="post_create"),
    path('activate/<uidb64>/<token>', yct_views.ActivateAccountView.as_view(), name="activate"),
    path('logout/', yct_views.user_logout, name="user_logout"),
    path('signup/', yct_views.signup_view, name="signup_view"),
    
    path('like/', yct_views.like_post, name="like_post"),
]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
