from django import forms

from userprofile.models import UserProfile, GENDER_CHOICE


# 用户模型扩展userprofile表单
class UseProfileForm(forms.Form):
    # 从上往下 要先想好，循环渲染时候 是从上往下
    tel = forms.CharField(label='Your telephone', max_length=20, strip=True, required=False)
    gender = forms.ChoiceField(label='Your gender', choices=GENDER_CHOICE, required=False)
    profile_photo = forms.ImageField(label='profile_photo', required=False)


# 自定义表单
class SignupForm(forms.Form):
    # 对某方法进行重写，注意名字
    def signup(self, request, user):
        user_profile = UserProfile()
        user_profile.user = user
        user.save()
        user_profile.save()


# 重写重置密码表单
class ResetPasswordForm(forms.Form):
    """
    重置密码表单，需要手机号验证
    """

    tel = forms.CharField(max_length=20, required=True, label='Telephone')

    # 获取电话号码
    def clean_identity_tel(self):
        tel = self.cleaned_data['tel']
        print(tel)
        """
        由于用get获取对象，如果获取不到会报错，所以这里使用filter
        获取失败返回空对象列表
        在UserProfile中筛选符合条件的用户，返回用户名
        """
        username = UserProfile.objects.filter(tel=tel)
        if not username:
            raise forms.ValidationError("手机号错误!!")

        return self.cleaned_data['tel']

    def save(self, request, **kwargs):
        return self.cleaned_data['tel']
