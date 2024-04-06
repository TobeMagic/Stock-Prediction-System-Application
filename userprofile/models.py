from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

GENDER_CHOICE = (
    ('女', '女'),
    ('男', '男'),
)


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name=_('用户'))

    gender = models.CharField(choices=GENDER_CHOICE, max_length=10, verbose_name=_('性别'), blank=True)
    tel = models.CharField(max_length=20, verbose_name=_('电话'), blank=True, db_column='telephone')
    profile_photo = models.ImageField(upload_to='image/', verbose_name=_('头像'), blank=True, null=True)

    class Meta:
        # admin 名称
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = 'userprofile'

    def __str__(self):
        return '{}'.format(self.user.__str__())
