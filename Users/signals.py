from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings

def createProfile(sender,instance,created,**kwargs):
    userobj=instance
    if created:
        profile=Profile.objects.create(
            user=userobj,
            name=userobj.username,
            username=userobj.username,
            email=userobj.email
        )
        print("profile also created for this user")
        
        subject="Welcome to Developers Web Application"
        message="We are glad you are here"
        
        send_mail(subject,
                  message,
                  settings.EMAIL_HOST_USER,
                  [profile.email],
                  fail_silently=False,
                  )
        print('Mail successfully sent to new registered user')
        
def deleteUser(sender,instance,**kwargs):
    profile=instance
    userobj=profile.user
    userobj.delete()
    print('User is also deleted')

def updateUser(sender,instance,created,**kwargs):
    if created==False:
        profile=instance
        user=profile.user
        user.first_name=profile.name
        user.email=profile.email
        user.username=profile.username
        user.save()
        print('user updated sucessfully')
        
        
post_save.connect(updateUser,sender=Profile)
post_save.connect(createProfile,sender=User)
#post_delete.connect(deleteUser,sender=Profile)