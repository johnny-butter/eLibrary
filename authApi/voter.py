from .models import User


class baseVoter:

    request = None

    def __init__(self, request):
        self.request = request

    def is_logged_in(self):
        if isinstance(self.request.user, User):
            return True

        return False

    def is_superuser(self):
        if self.is_logged_in():
            return self.request.user.is_superuser

        return False


class userVoter(baseVoter):

    def user_can_manage_me(self, userInstance: User):
        if self.is_logged_in():
            if self.is_superuser():
                return True
            if self.request.user == userInstance:
                return True

        return False
