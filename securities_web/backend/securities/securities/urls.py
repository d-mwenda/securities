"""securities URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

from index.urls import urlpatterns as index_urls
from stock_trading.urls import urlpatterns as stock_trading_urls
from stock_trading.urls import api_urlpatterns as stock_trading_api_urls
from contact.urls import url_patterns as contact_urls
from stock_trading.sitemaps import CompanySitemap, SecuritiesExchangeSitemap
from index.sitemaps import StaticViewsSitemap

sitemaps = {
    "static_views": StaticViewsSitemap,
    "securities_exchanges": SecuritiesExchangeSitemap,
    "company_stock_trading": CompanySitemap,
}

api_urlpatterns = [
    path("stock-trading/", include(stock_trading_api_urls))
]

urlpatterns = [
    path("", include(index_urls)),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap"),
    path("admin/", admin.site.urls),
    path("api/", include(api_urlpatterns)),
    path("stock-trading/", include(stock_trading_urls), name="stock_trading"),
    # path("contact", include(contact_urls), name="contact_urls")
]
