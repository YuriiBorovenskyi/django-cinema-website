from django import forms
from captcha.fields import CaptchaField

from .models import CommentToPerson, CommentToFilm, CommentToNews, \
    CommentToProduct


class UserCommentToPersonForm(forms.ModelForm):
    class Meta:
        model = CommentToPerson
        exclude = ('is_active',)
        widgets = {'cinema_person': forms.HiddenInput}


class GuestCommentToPersonForm(forms.ModelForm):
    captcha = CaptchaField(label='Input text from picture', error_messages={
        'invalid': 'Wrong text'
    })

    class Meta:
        model = CommentToPerson
        exclude = ('is_active',)
        widgets = {'cinema_person': forms.HiddenInput}


class UserCommentToFilmForm(forms.ModelForm):
    class Meta:
        model = CommentToFilm
        exclude = ('is_active',)
        widgets = {'film': forms.HiddenInput}


class GuestCommentToFilmForm(forms.ModelForm):
    captcha = CaptchaField(label='Input text from picture', error_messages={
        'invalid': 'Wrong text'
    })

    class Meta:
        model = CommentToFilm
        exclude = ('is_active',)
        widgets = {'film': forms.HiddenInput}


class UserCommentToNewsForm(forms.ModelForm):
    class Meta:
        model = CommentToNews
        exclude = ('is_active',)
        widgets = {'news': forms.HiddenInput}


class GuestCommentToNewsForm(forms.ModelForm):
    captcha = CaptchaField(label='Input text from picture', error_messages={
        'invalid': 'Wrong text'
    })

    class Meta:
        model = CommentToNews
        exclude = ('is_active',)
        widgets = {'news': forms.HiddenInput}


class UserCommentToProductForm(forms.ModelForm):
    class Meta:
        model = CommentToProduct
        exclude = ('is_active',)
        widgets = {'product': forms.HiddenInput}


class GuestCommentToProductForm(forms.ModelForm):
    captcha = CaptchaField(label='Input text from picture', error_messages={
        'invalid': 'Wrong text'
    })

    class Meta:
        model = CommentToProduct
        exclude = ('is_active',)
        widgets = {'product': forms.HiddenInput}
