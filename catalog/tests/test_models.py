from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Topic, Newspaper


class TopicModelTest(TestCase):
    def test_str(self) -> None:
        topic = Topic.objects.create(
            name="Technology"
        )
        self.assertEqual(str(topic), topic.name)


class RedactorModelTest(TestCase):
    def test_str(self) -> None:
        redactor = get_user_model().objects.create_user(
            username="redactor1",
            password="strongpassword123",
            first_name="John",
            last_name="Doe",
            years_of_experience=5
        )
        self.assertEqual(str(redactor), redactor.username)

    def test_get_absolute_url(self) -> None:
        redactor = get_user_model().objects.create_user(
            username="redactor1",
            password="strongpassword123",
            years_of_experience=5
        )
        self.assertEqual(
            redactor.get_absolute_url(),
            reverse("catalog:redactor-detail", args=[str(redactor.id)])
        )


class NewspaperModelTest(TestCase):
    def test_str(self) -> None:
        topic = Topic.objects.create(name="Science")
        newspaper = Newspaper.objects.create(
            title="Science Today",
            content="Interesting content about science",
            topic=topic
        )
        self.assertEqual(str(newspaper), newspaper.title)
