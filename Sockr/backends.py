from django.contrib.auth.backends import RemoteUserBackend

class LtuRemoteUserBackend(RemoteUserBackend):
    def configure_user(self, user):
        if "-" not in user.username:
            user.email = "%s@ltu.se" % user.username
            user.is_staff = True
        else:
            user.email = "%s@student.ltu.se" % user.username
        user.save()
        return user