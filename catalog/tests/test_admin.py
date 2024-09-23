from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from catalog.models import Topic, Newspaper


class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testpassword",
        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="redactor1",
            password="redactorpassword",
            first_name="Іван",
            last_name="Петренко",
            years_of_experience=5
        )
        self.topic = Topic.objects.create(name="Science")
        self.newspaper = Newspaper.objects.create(
            title="Science Today",
            content="Interesting science article",
            topic=self.topic
        )
        self.newspaper.publishers.add(self.redactor)

    def test_redactor_years_of_experience_listed(self):
        url = reverse("admin:catalog_redactor_changelist")
        response_test = self.client.get(url)
        self.assertContains(response_test, self.redactor.years_of_experience)

    def test_redactor_detail_years_of_experience_listed(self):
        url = reverse("admin:catalog_redactor_change", args=[self.redactor.pk])
        response_test = self.client.get(url)
        self.assertContains(response_test, self.redactor.years_of_experience)

    def test_redactor_years_of_experience_in_add_form(self):
        url = reverse("admin:catalog_redactor_add")
        response_test = self.client.get(url)
        self.assertContains(response_test, "years_of_experience")

    def test_newspaper_topic_listed(self):
        url = reverse("admin:catalog_newspaper_changelist")
        response_test = self.client.get(url)
        self.assertContains(response_test, self.newspaper.topic.name)

    def test_newspaper_detail_topic_listed(self):
        url = reverse("admin:catalog_newspaper_change", args=[self.newspaper.pk])
        response_test = self.client.get(url)
        self.assertContains(response_test, self.newspaper.topic.name)

    def test_newspaper_topic_in_add_form(self):
        url = reverse("admin:catalog_newspaper_add")
        response_test = self.client.get(url)
        self.assertContains(response_test, "topic")
