"""XMas_happiness_engine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from . import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

urlpatterns = [
    url(regex=r'^login/$', view=login, kwargs={'template_name': 'login.html'}, name='login'),
    url(regex=r'^logout/$', view=logout, kwargs={'next_page': '/'}, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'ttm/(?P<thought>[\w\-]+)$',views.thought_to_memory)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)