from django import forms
from . import models

#class CommentArticle(forms.ModelForm):
	#class Meta:
		#model = models.Article
		#fields = ['title', 'body', 'slug', 'thumb']
from .models import Article, Comment
from django.contrib.auth.models import User

class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = (
            'category',
            'title',
            'description',
            'duration',
            'amount',
            'image',
            'image2',
            'image3',
            'status',
        )

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            'title',
            'body',
            'status',
            'restrict_comment',
        )


class UserLoginForm(forms.Form):
    username = forms.CharField(label="", widget= forms.TextInput(attrs = {'placeholder':'Username'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs = {'placeholder':'Password'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="", widget = forms.PasswordInput(attrs = {'id': 'pass1','class': 'input100', 'placeholder':'Enter Password Here...'}))
    confirm_password = forms.CharField(label="",  widget = forms.PasswordInput(attrs = {'id': 'pass2', 'class': 'input100'}))
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            )
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password Mismatch")
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Password Mismatch")
        return email


class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

#class ProfileEditForm(forms.ModelForm):
#    class Meta:
#        model = Profile
#        exclude = ('user',)



class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment here!!!', 'rows':'4', 'cols':'50'}))
    class Meta:
        model = Comment
        fields = ('content',)
