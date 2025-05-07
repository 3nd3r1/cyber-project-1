from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from arenabuilds.models import Augment, Build, BuildAugment, BuildItem, Champion, Item


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label="Username", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Password is required")

        try:
            # Vuln 5: A07:2021: Authentication Failures: No password validation
            pass
            # Fix 5: validate the password
            # validate_password(password)
        except ValidationError as e:
            self.add_error("password", e)

        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CreateBuildForm(forms.ModelForm):
    title = forms.CharField(
        label="Build Title", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    champion = forms.ModelChoiceField(
        label="Champion",
        queryset=Champion.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
    )

    item_1 = forms.ModelChoiceField(queryset=Item.objects.all(), required=False)
    item_2 = forms.ModelChoiceField(queryset=Item.objects.all(), required=False)
    item_3 = forms.ModelChoiceField(queryset=Item.objects.all(), required=False)
    item_4 = forms.ModelChoiceField(queryset=Item.objects.all(), required=False)
    item_5 = forms.ModelChoiceField(queryset=Item.objects.all(), required=False)

    augment_0 = forms.ModelChoiceField(queryset=Augment.objects.all(), required=False)
    augment_1 = forms.ModelChoiceField(queryset=Augment.objects.all(), required=False)
    augment_2 = forms.ModelChoiceField(queryset=Augment.objects.all(), required=False)
    augment_3 = forms.ModelChoiceField(queryset=Augment.objects.all(), required=False)
    augment_4 = forms.ModelChoiceField(queryset=Augment.objects.all(), required=False)
    augment_5 = forms.ModelChoiceField(queryset=Augment.objects.all(), required=False)

    class Meta:
        model = Build
        fields = ["title", "champion", "description"]

    def save(self, commit=True, user=None):
        build = super().save(commit=False)

        if user:
            build.author = user

        if commit:
            build.save()

            for i in range(6):
                item = self.cleaned_data.get(f"item_{i}")
                if item:
                    BuildItem.objects.create(build=build, item=item)

            for i in range(6):
                augment = self.cleaned_data.get(f"augment_{i}")
                if augment:
                    BuildAugment.objects.create(build=build, augment=augment)

        return build


class SearchForm(forms.Form):
    query = forms.CharField(
        label="Search",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search builds"}
        ),
    )
