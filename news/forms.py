from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Article, Newsletter, Publisher, User


class RegistrationForm(UserCreationForm):    

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "role",
            "password1",
            "password2",
        )


class ArticleForm(forms.ModelForm):    

    class Meta:
        model = Article
        fields = (
            "title",
            "content",
            "publisher",
        )

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter article title",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Write your article here...",
                }
            ),
            "publisher": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if self.user and self.user.role == User.Role.JOURNALIST:
            self.fields["publisher"].queryset = (
                Publisher.objects.filter(
                    journalists=self.user
                )
            )


class NewsletterForm(forms.ModelForm):    

    class Meta:
        model = Newsletter
        fields = (
            "title",
            "description",
            "articles",
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["articles"].queryset = Article.objects.filter(
            approved=True
        )


class PublisherForm(forms.ModelForm):    

    class Meta:
        model = Publisher
        fields = (
            "name",
            "description",
            "website",
            "editors",
            "journalists",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["editors"].queryset = User.objects.filter(
            role=User.Role.EDITOR
        )

        self.fields["journalists"].queryset = User.objects.filter(
            role=User.Role.JOURNALIST
        )