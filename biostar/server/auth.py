from biostar.apps.users.models import User

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class AutoSignupAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        # This social login already exists.
        if sociallogin.is_existing:
            return

        # Check if we could/should connect it.
        try:
            email = sociallogin.account.extra_data.get('email')
            #verified = sociallogin.account.extra_data.get('verified_email')
            if email:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass

class ExternalAuth(object):
    '''
    This is an "autentication" that relies on the user being valid.
    We're just following the Django interfaces here.
    '''

    def authenticate(self, email, valid=False):
        # Check the username/password and return a User.
        if valid:
            user = User.objects.get(email=email)
            user.backend = "%s.%s" % (__name__, self.__class__.__name__)
            print user.backend
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
