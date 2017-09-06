from django.contrib.auth.backends import RemoteUserBackend

class LtuRemoteUserBackend(RemoteUserBackend):
    def configure_user(self, user):
        user.email = user.username
        user.save()
        return user
