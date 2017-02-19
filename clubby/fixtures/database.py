from django.conf import settings

from oauth2_provider.models import Application

from profiles.models import User


import time


user = User.objects.create_superuser(email='jineshpaul89@gmail.com', password='admin@123')
time.sleep(1)

application = Application(client_id=settings.CLIENT_ID, user=user, client_type='confidential',
                          authorization_grant_type='password', client_secret=settings.CLIENT_SECRET, name='clubby')
application.save()
time.sleep(1)

