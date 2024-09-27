from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.forms import (
    NewspaperForm,
    RedactorCreationForm,
    RedactorUpdateForm,
    TopicSearchForm,
    NewspaperSearchForm,
    RedactorSearchForm
)
from catalog.models import Newspaper, Topic


class FormsTestCase(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.redactor = get_user_model().objects.create_user(
            username="testredactor",
            password="testpassword",
            years_of_experience=5
        )
        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            content="Test content",
            topic=self.topic
        )
        self.newspaper.publishers.add(self.redactor)

    def test_newspaper_form_valid(self):
        form_data = {
            "title": self.newspaper.title,
            "content": self.newspaper.content,
            "topic": self.topic.pk,
            "publishers": [self.redactor.pk],
        }
        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_redactor_creation_form_valid(self):
        form_data = {
            "username": "newredactor",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "John",
            "last_name": "Doe",
            "years_of_experience": 3
        }
        form = RedactorCreationForm(data=form_data)

        if not form.is_valid():
            print(form.errors)

        self.assertTrue(form.is_valid())

    def test_redactor_update_form_valid(self):
        form_data = {
            "years_of_experience": 10
        }
        form = RedactorUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_topic_search_form(self):
        form = TopicSearchForm(data={"name": "Test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test")

    def test_newspaper_search_form(self):
        form = NewspaperSearchForm(data={"title": "Test Newspaper"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Test Newspaper")

    def test_redactor_search_form(self):
        form = RedactorSearchForm(data={"username": "testredactor"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testredactor")
