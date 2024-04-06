# from django.contrib.auth.tokens import default_token_generator
from allauth.account.forms import default_token_generator  # 注意！！ token生成实在allauth里面，不是django自带得token生成器
from allauth.account.utils import user_pk_to_url_str
from allauth.account.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, reverse, redirect, HttpResponseRedirect

from userprofile.forms import UseProfileForm, ResetPasswordForm
from userprofile.models import UserProfile


# Create your views here.

@login_required
def profile(request):
    user = request.user
    # print(request.user)
    return render(request, 'account/profile.html', {'user': user})


@login_required
def profile_update(request):
    """
    集查看和提交于一体，当查看时处理get，点击button提交提交到本页面，处理post请求
    """
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    # print(user, 'ok')
    if request.method == "POST":
        # 得到表单数据
        form = UseProfileForm(request.POST)
        # print(form)
        if form.is_valid():
            user_profile.tel = form.cleaned_data['tel']
            user_profile.gender = form.cleaned_data['gender']
            # 保存对应文件路径
            user_profile.profile_photo = request.FILES.get("profile_photo")
            print(user_profile.profile_photo)
            user_profile.save()

            return HttpResponseRedirect(reverse('userprofile:profile'))

    else:
        default_data = {
            'tel': user_profile.tel, 'gender': user_profile.gender, 'profile_photo': user_profile.profile_photo
        }

        form = UseProfileForm(default_data)
        # print(form, reverse('userprofile:profile'))
    # 如果时get 返回查看
    return render(request, 'account/profile_update.html', {'form': form, 'user': user})


class CustomPasswordResetView(PasswordResetView):

    def post(self, request, *args, **kwargs):
        reset_password_form = ResetPasswordForm(request.POST)
        if reset_password_form.is_valid():

            # 从电话筛选出 用户对象
            tel = reset_password_form.clean_identity_tel()
            # UseProfile 中由于user相同属性的 username
            try:
                username = UserProfile.objects.get(tel=tel)
                user = User.objects.get(username=username)
            except:
                return render(request, 'account/telephone_error.html', {'content': "电话错误(表单格式错误）或和他人一样！"})
            # 查看传参有无 令牌
            token_generator = kwargs.get(
                "token_generator", default_token_generator)
            # 没有生成token
            temp_key = token_generator.make_token(user)
            # 反向解析路径，（并传令牌参数）
            path = reverse(
                "account_reset_password_from_key",
                kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key),
            )  # ^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$ [name='account_reset_password_from_key']
            # 在根目录下建立绝对路径(self = request)
            url = HttpRequest.build_absolute_uri(request, path)
            # 重定向至修改密码链接
            print(request, url, path)
            return redirect(url)

        else:
            return render(request, 'account/telephone_error.html', {'content': "电话错误(表单格式错误）"})


# 注意 这里不能加上 login_required 的限制！ 不然登录页面 忘记密码就会无法登录
password_reset = CustomPasswordResetView.as_view()
