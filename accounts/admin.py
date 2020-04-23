from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label = 'Password',widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Password Confirmation', widget = forms.PasswordInput)
    class meta:
        model = User
        fields = ('name','surname','email','eagle_id')
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('name','password','surname','email', 'eagle_id', 'is_staff','is_active')
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email','name','surname','eagle_id','is_staff',)

    fieldsets = (
        (None, {'fields':('email','surname','name','password')}),
        ('Personal Info',{'fields':('eagle_id',)}),
        ('Permissions',{'fields':('is_staff','is_active','is_superuser',)}),
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','eagle_id','password1','password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User,UserAdmin)
admin.site.unregister(Group)

# Register your models here.
