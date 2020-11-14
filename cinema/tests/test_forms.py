from django.forms import HiddenInput

from cinema.forms import (
    GuestCommentToFilmForm,
    GuestCommentToNewsForm,
    GuestCommentToPersonForm,
    GuestCommentToProductForm,
    UserCommentToFilmForm,
    UserCommentToNewsForm,
    UserCommentToPersonForm,
    UserCommentToProductForm,
)
from cinema.models import (
    CommentToFilm,
    CommentToNews,
    CommentToPerson,
    CommentToProduct,
)


class TestUserCommentToPersonForm:
    def test_form_is_created_from_model(self):
        form = UserCommentToPersonForm()
        assert form.Meta.model is CommentToPerson

    def test_is_active_field_is_excluded_from_form(self):
        form = UserCommentToPersonForm()
        assert "is_active" in form.Meta.exclude

    def test_widget_of_captcha_field_of_form(self):
        form = UserCommentToPersonForm()
        assert form.Meta.widgets["cinema_person"] is HiddenInput


class TestUserCommentToFilmForm:
    def test_form_is_created_from_model(self):
        form = UserCommentToFilmForm()
        assert form.Meta.model is CommentToFilm

    def test_is_active_field_is_excluded_from_form(self):
        form = UserCommentToFilmForm()
        assert "is_active" in form.Meta.exclude

    def test_widget_of_captcha_field_of_form(self):
        form = UserCommentToFilmForm()
        assert form.Meta.widgets["film"] is HiddenInput


class TestUserCommentToNewsForm:
    def test_form_is_created_from_model(self):
        form = UserCommentToNewsForm()
        assert form.Meta.model is CommentToNews

    def test_is_active_field_is_excluded_from_form(self):
        form = UserCommentToNewsForm()
        assert "is_active" in form.Meta.exclude

    def test_widget_of_captcha_field_of_form(self):
        form = UserCommentToNewsForm()
        assert form.Meta.widgets["news"] is HiddenInput


class TestUserCommentToProductForm:
    def test_form_is_created_from_model(self):
        form = UserCommentToProductForm()
        assert form.Meta.model is CommentToProduct

    def test_is_active_field_is_excluded_from_form(self):
        form = UserCommentToProductForm()
        assert "is_active" in form.Meta.exclude

    def test_widget_of_captcha_field_of_form(self):
        form = UserCommentToProductForm()
        assert form.Meta.widgets["product"] is HiddenInput


class TestGuestCommentToPersonForm:
    def test_form_is_created_from_model(self):
        form = GuestCommentToPersonForm()
        assert form.Meta.model is CommentToPerson

    def test_is_active_field_is_excluded_from_form(self):
        form = GuestCommentToPersonForm()
        assert "is_active" in form.Meta.exclude

    def test_widget_of_captcha_field_of_form(self):
        form = GuestCommentToPersonForm()
        assert form.Meta.widgets["cinema_person"] is HiddenInput

    def test_captcha_field_label_of_form(self):
        form = GuestCommentToPersonForm()
        assert (
            form.fields["captcha"].label is None
            or form.fields["captcha"].label == "Input text from picture"
        )

    def test_captcha_field_options_of_form(self):
        form = GuestCommentToPersonForm()
        assert form.fields["captcha"].error_messages["invalid"] == "Wrong text"


class TestGuestCommentToFilmForm:
    def test_form_is_created_from_model(self):
        form = GuestCommentToFilmForm()
        assert form.Meta.model is CommentToFilm

    def test_is_active_field_is_excluded_from_form(self):
        form = GuestCommentToFilmForm()
        assert "is_active" in form.Meta.exclude

    def test_widget_of_captcha_field_of_form(self):
        form = GuestCommentToFilmForm()
        assert form.Meta.widgets["film"] is HiddenInput

    def test_captcha_field_label_of_form(self):
        form = GuestCommentToFilmForm()
        assert (
            form.fields["captcha"].label is None
            or form.fields["captcha"].label == "Input text from picture"
        )

    def test_captcha_field_options_of_form(self):
        form = GuestCommentToFilmForm()
        assert form.fields["captcha"].error_messages["invalid"] == "Wrong text"


class TestGuestCommentToNewsForm:
    def test_form_is_created_from_model(self):
        form = GuestCommentToNewsForm()
        assert form.Meta.model is CommentToNews

    def test_is_active_field_is_excluded_from_form(self):
        form = GuestCommentToNewsForm()
        assert "is_active" in form.Meta.exclude

    def test_widget_of_captcha_field_of_form(self):
        form = GuestCommentToNewsForm()
        assert form.Meta.widgets["news"] is HiddenInput

    def test_captcha_field_label_of_form(self):
        form = GuestCommentToNewsForm()
        assert (
            form.fields["captcha"].label is None
            or form.fields["captcha"].label == "Input text from picture"
        )

    def test_captcha_field_options_of_form(self):
        form = GuestCommentToNewsForm()
        assert form.fields["captcha"].error_messages["invalid"] == "Wrong text"


class TestGuestCommentToProductForm:
    def test_form_is_created_from_model(self):
        form = GuestCommentToProductForm()
        assert form.Meta.model is CommentToProduct

    def test_is_active_field_is_excluded_from_form(self):
        form = GuestCommentToProductForm()
        assert "is_active" in form.Meta.exclude

    def test_widget_of_captcha_field_of_form(self):
        form = GuestCommentToProductForm()
        assert form.Meta.widgets["product"] is HiddenInput

    def test_captcha_field_label_of_form(self):
        form = GuestCommentToProductForm()
        assert (
            form.fields["captcha"].label is None
            or form.fields["captcha"].label == "Input text from picture"
        )

    def test_captcha_field_options_of_form(self):
        form = GuestCommentToProductForm()
        assert form.fields["captcha"].error_messages["invalid"] == "Wrong text"
