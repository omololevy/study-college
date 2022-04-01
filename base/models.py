from os import link
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# from pyuploadcare.dj.models import ImageField
from django.dispatch import receiver
from django.db.models.signals import post_save


class Cohort(models.Model):
    name = models.CharField(max_length=50)
    admin = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='hood')
    cohort_logo =  CloudinaryField('profile_photos/', default='profile_photos/user')
    description = models.TextField()
    t_mentor = models.CharField(max_length=60, null=True, blank=True)
    class_rep = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return f'{self.name} cohort'

    def create_cohort(self):
        self.save()

    def delete_cohort(self):
        self.delete()

    @classmethod
    def find_cohort(cls, cohort_id):
        return cls.objects.filter(id=cohort_id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=80, blank=True)
    bio = models.TextField(max_length=254, blank=True)
    profile_picture = CloudinaryField('profile_photos/', default='http://res.cloudinary.com/dim8pysls/image/upload/v1639001486/x3mgnqmbi73lten4ewzv.png')
    location = models.CharField(max_length=50, blank=True, null=True)
    cohort = models.ForeignKey(Cohort, on_delete=models.SET_NULL, null=True, related_name='members', blank=True)

    def __str__(self):
        return f'{self.user.username} profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Module(models.Model):
    name = models.CharField(max_length=120)
    link = models.URLField(max_length=254)
    description = models.TextField(blank=True)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='module')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} Module'

    def create_module(self):
        self.save()

    def delete_module(self):
        self.delete()

    @classmethod
    def search_module(cls, name):
        return cls.objects.filter(name__icontains=name).all()


class Discussion(models.Model):
    title = models.CharField(max_length=120, null=True)
    content= models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='topic_owner')
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='cohort_topic')

