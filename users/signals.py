from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender= Profile)
def profileUpdated(sender, instance, created, **kwwargs):
    print('Profile Saved')
    print('Instance:', instance)
    print('Created:', created)

@receiver(post_delete, sender= Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

    
@receiver(post_save, sender= User)
def createProfile(sender, instance, created, **kwargs):
    print('Profile signal triggered')
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )

        subject = 'Welcome to DevSearch'
        message = 'We are glad you are here!'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )

@receiver(post_save, sender= Profile)
def userUpdate(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

# post_save.connect(profileUpdated, sender= Profile)
# post_delete.connect(deleteUser, sender= Profile)
# post_save.connect(createProfile, sender= User)
# post_delete.connect(deleteUser, sender= Profile)