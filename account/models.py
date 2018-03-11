from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File

auth_user = User

class Profile(models.Model):
    SEX_CHOICES = (
        ('m', '男'),
        ('f', '女')
    )
    user = models.OneToOneField(auth_user)
    photo = models.ImageField(upload_to='users', blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='m')
    introduction = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=20, blank=True)
    industry = models.CharField(max_length=20, blank=True)
    education = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return '%s%s' % (settings.MEDIA_URL, 'users/default.png')

    def save(self, *args, **kwargs):
        if not self.photo:
            with open(settings.MEDIA_ROOT + 'users/default.png', 'rb') as f:
                self.photo.save('default.png', File(f), save=False)

        super(Profile, self).save(*args, **kwargs)



class Contact(models.Model):
    user_from = models.ForeignKey(auth_user,
                                  related_name='rel_from_set')
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)

auth_user.add_to_class('following',
                       models.ManyToManyField('self',
                                              through=Contact,
                                              related_name='followers',
                                              symmetrical=False))