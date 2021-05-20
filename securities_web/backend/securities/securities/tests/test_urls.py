from django import test
from django.urls import resolve


class TestURL(test.TestCase):
    def test_root_redirects(self):
        resolved_to = resolve("/")
        self.assertEqual(resolved_to.func.__name__, "RedirectView",
                         "The URL root may not redirect as expected."
                         )
