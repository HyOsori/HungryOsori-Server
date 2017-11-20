from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile, UserManager


class UserProfileCreationForm(forms.ModelForm):
    # 사용자 생성 폼
    email = forms.EmailField(
        label=_('이메일'),
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이메일 주소',
                'required': 'True',
            }
        )
    )
    name = forms.CharField(
        label=_('이름'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이름',
                'required': 'True',
            }
        )
    )
    password1 = forms.CharField(
        label=_('비밀번호'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호',
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label=_('비밀번호 확인'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호 확인',
                'required': 'True',
            }
        )
    )

    class Meta:
        model = UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # 두 비밀번호 입력 일치 확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not password1:
            raise forms.ValidationError("비밀번호를 입력해주세요")
        if not password2:
            raise forms.ValidationError("비밀번호를 확인해주세요")
        if password1 != password2:
            raise forms.ValidationError("비밀번호가 같지 않습니다.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserProfileCreationForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserProfileChangeForm(forms.ModelForm):
    # 비밀번호 변경 폼
    password = ReadOnlyPasswordHashField(
        label=_('Password')
    )

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'name', 'is_active',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'password']