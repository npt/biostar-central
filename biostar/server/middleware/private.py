from django.conf import settings
from django.contrib.auth.views import redirect_to_login

class MakePrivate(object):
    """
    Requires authentication for everything.
    """

    def process_request(self, request):
        if settings.PRIVATE_SITE and not request.user.is_authenticated():
            if not request.path.startswith('/accounts/'):
                return redirect_to_login(request.get_full_path())
