from django.contrib.sitemaps import Sitemap

from .models import Company, SecuritiesExchange


class CompanySitemap(Sitemap):
    """Sitemaps for the Company Model"""
    changefreq = "daily"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Company.objects.all()


class SecuritiesExchangeSitemap(Sitemap):
    """Sitemaps for the Securities Exhange Model"""
    changefreq = "daily"
    priority = 0.5
    protocol = "https"

    def items(self):
        return SecuritiesExchange.objects.all()
