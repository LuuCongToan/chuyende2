from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from basic_app.models import UserProfileInfo,Post,Group,PostGroup,Page,PostPage

class PageForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        self.user_profile = kwargs.pop('user_profile', None)
        super(PageForm, self).__init__(*args, **kwargs)

    def save(self):
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        created_by = self.user_profile
        follow = [self.user_profile]
        page = Page(name=name, description=description, created_by=created_by)
        page.save()
        page.follow.set(follow)
        return page
class GroupForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        self.user_profile = kwargs.pop('user_profile', None)
        super(GroupForm, self).__init__(*args, **kwargs)

    def save(self):
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        created_by = self.user_profile
        members = [self.user_profile]
        group = Group(name=name, description=description, created_by=created_by)
        group.save()
        group.members.set(members)
        return group
class PostGroupForm(forms.ModelForm):
    class Meta:
        model = PostGroup
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }
class PostPageForm(forms.ModelForm):
    class Meta:
        model = PostPage
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User 
        fields = ('username','email','password')


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo 
        fields = ('portfolio_site','profile_pic')



class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['portfolio_site'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_pic'].widget.attrs.update({'class': 'form-control-file'})
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Current Password'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='New Password'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm New Password'
    )

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
