from django.contrib.auth.hashers import make_password
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=20,
                                unique=True,
                                verbose_name='用户名')
    password = models.CharField(max_length=100,
                                verbose_name='密码')
    email = models.CharField(max_length=50,
                             unique=True,
                             verbose_name='邮箱')
    photo = models.CharField(max_length=100,
                             verbose_name='头像',
                             blank=True,
                             null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 修改用户邮箱时,密码没有改变的情况下,需避免重复加密
        if not self.password.startswith('pbkdf2_sha256') and len(self.password) <= 70:
            self.password = make_password(self.password)  # 加密
        super().save()

    class Meta:
        db_table = 't_user'
        verbose_name = '客户'
        verbose_name_plural = verbose_name

