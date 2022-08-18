from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewsSitemap(Sitemap):
    "Generate sitemaps for static views."
    changefreq = "annually"
    priority = 0.5
    protocol = "https"
    pages = {
        "home": 0.9,
    }

    def items(self):
        return list(self.pages.keys())

    def location(self, item):
        """Return the location and set the appropriate priority on instance"""
        self.priority = self.pages[item]
        return reverse(item)
