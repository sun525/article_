from django import forms
from django.core.exceptions import ValidationError

from user.models import UserProfile


class UserForm(forms.ModelForm):
    username = forms.CharField(min_length=8, max_length=20,
                               error_messages={
                                   'required': '用户名不能为空',
                                   'max_length': '用户名超出20个字符',
                                   'min_length': '用户名不能低于8个字符'
                               })
    password2 = forms.CharField(min_length=8, required=True,
                                error_messages={
                                    'required': '密码不能为空',
                                    'min_length': '密码不能低于8个字符'
                                })

    class Meta:
        model = UserProfile
        fields = '__all__'
        error_messages = {
            'password': {
                'required': '密码不能为空'
            },
            'email': {
                'required': '邮箱不能为空'
            }
        }

    # claen_xxx:实现除required,max,min外字符的验证
    def clean_password2(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 is not None and p1 == p2:
            return p1
        # ValidationError可以向errors里增加信息
        raise ValidationError('两次密码不一致')
