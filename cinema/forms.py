from captcha.fields import CaptchaField
from django import forms

from .models import (
    CommentToFilm,
    CommentToNews,
    CommentToPerson,
    CommentToProduct,
)


class UserCommentToPersonForm(forms.ModelForm):
    """Form for adding comments to cinema person.

    It is created from 'CommentToPerson' model.

    This form will be filled in by registered, signed-in users.
    """

    class Meta:
        model = CommentToPerson
        exclude = ("is_active",)
        widgets = {"cinema_person": forms.HiddenInput}


class GuestCommentToPersonForm(forms.ModelForm):
    """Form for adding comments to cinema person.

    It is created from 'CommentToPerson' model.

    This form will be filled in by website guests.
    Form additionally contains "CAPTCHA" field, which allows you to protect
    website from bots.
    """

    captcha = CaptchaField(
        label="Input text from picture",
        error_messages={"invalid": "Wrong text"},
    )

    class Meta:
        model = CommentToPerson
        exclude = ("is_active",)
        widgets = {"cinema_person": forms.HiddenInput}


class UserCommentToFilmForm(forms.ModelForm):
    """Form for adding comments to movie.

    It is created from 'CommentToFilm' model.

    This form will be filled in by registered, signed-in users.
    """

    class Meta:
        model = CommentToFilm
        exclude = ("is_active",)
        widgets = {"film": forms.HiddenInput}


class GuestCommentToFilmForm(forms.ModelForm):
    """Form for adding comments to movie.

    It is created from 'CommentToFilm' model.

    This form will be filled in by website guests.
    Form additionally contains "CAPTCHA" field, which allows you to protect
    website from bots.
    """

    captcha = CaptchaField(
        label="Input text from picture",
        error_messages={"invalid": "Wrong text"},
    )

    class Meta:
        model = CommentToFilm
        exclude = ("is_active",)
        widgets = {"film": forms.HiddenInput}


class UserCommentToNewsForm(forms.ModelForm):
    """Form for adding comments to news.

    It is created from 'CommentToNews' model.

    This form will be filled in by registered, signed-in users.
    """

    class Meta:
        model = CommentToNews
        exclude = ("is_active",)
        widgets = {"news": forms.HiddenInput}


class GuestCommentToNewsForm(forms.ModelForm):
    """Form for adding comments to news.

    It is created from 'CommentToNews' model.

    This form will be filled in by website guests.
    Form additionally contains "CAPTCHA" field, which allows you to protect
    website from bots.
    """

    captcha = CaptchaField(
        label="Input text from picture",
        error_messages={"invalid": "Wrong text"},
    )

    class Meta:
        model = CommentToNews
        exclude = ("is_active",)
        widgets = {"news": forms.HiddenInput}


class UserCommentToProductForm(forms.ModelForm):
    """Form for adding comments to movie on blu-ray.

    It is created from 'CommentToProduct' model.

    This form will be filled in by registered, signed-in users.
    """

    class Meta:
        model = CommentToProduct
        exclude = ("is_active",)
        widgets = {"product": forms.HiddenInput}


class GuestCommentToProductForm(forms.ModelForm):
    """Form for adding comments to movie on blu-ray.

    It is created from 'CommentToProduct' model.

    This form will be filled in by website guests.
    Form additionally contains "CAPTCHA" field, which allows you to protect
    website from bots.
    """

    captcha = CaptchaField(
        label="Input text from picture",
        error_messages={"invalid": "Wrong text"},
    )

    class Meta:
        model = CommentToProduct
        exclude = ("is_active",)
        widgets = {"product": forms.HiddenInput}
