from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


class HomeView(View):
    template_name = "index/home.html"
    title_tag = "African Stock Markets | Share Prices & Financials"

    def get(self, request):
        return render(request, self.template_name, context=self.get_context())

    def get_context(self, **kwargs):
        ctx = kwargs
        ctx["title_tag"] = self.title_tag
        return ctx


class RobotsView(View):
    """View to render robots.txt file"""
    lines = [
        "User-Agent: *",
        "Allow: /",
        "",
        "User-Agent: *",
        "Disallow: /api/",
        "",
        "Sitemap: https://allafricasecurities.com/sitemap.xml",
    ]

    def get(self, request):
        return HttpResponse("\n".join(self.lines), content_type="text/plain")
