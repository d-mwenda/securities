from django.shortcuts import render
from django.views import View


class HomeView(View):
    template_name = "index/home.html"
    title_tag = "African Stock Markets | Share Price & Financials"

    def get(self, request):
        return render(request, self.template_name, context=self.get_context())

    def get_context(self, **kwargs):
        ctx = kwargs
        ctx["title_tag"] = self.title_tag
        return ctx


class RobotsView(View):
    def get(self, request):
        pass
