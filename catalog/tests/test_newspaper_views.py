from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Newspaper, Topic

NEWSPAPER_LIST_URL = reverse("catalog:newspaper-list")


class PublicNewspaperTest(TestCase):
    def test_login_required(self):
        test_response = self.client.get(NEWSPAPER_LIST_URL)
        self.assertNotEqual(test_response.status_code, 200)


class PrivateNewspaperTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="Politics")
        self.newspaper = Newspaper.objects.create(
            title="The Daily News",
            content="Today's top story...",
            topic=self.topic,
        )

    def test_retrieve_newspapers(self):
        Newspaper.objects.create(title="News 1", content="Content 1", topic=self.topic)
        Newspaper.objects.create(title="News 2", content="Content 2", topic=self.topic)

        test_response = self.client.get(NEWSPAPER_LIST_URL)
        self.assertEqual(test_response.status_code, 200)
        newspapers = Newspaper.objects.all()
        self.assertEqual(list(test_response.context["newspaper_list"]), list(newspapers))
        self.assertTemplateUsed(test_response, "catalog/newspaper_list.html")

    def test_search_newspaper_by_title(self):
        newspaper1 = Newspaper.objects.create(title="Breaking News", content="Content", topic=self.topic)
        newspaper2 = Newspaper.objects.create(title="Tech News", content="Latest tech...", topic=self.topic)

        response = self.client.get(NEWSPAPER_LIST_URL, {"title": "Breaking"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(newspaper1, response.context["newspaper_list"])
        self.assertNotIn(newspaper2, response.context["newspaper_list"])

        response = self.client.get(NEWSPAPER_LIST_URL, {"title": "Tech"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(newspaper2, response.context["newspaper_list"])

    def test_create_newspaper(self):
        redactor = get_user_model().objects.create_user(
            username="test_redactor",
            password="password123"
        )
        topic = Topic.objects.create(name="Science")
        form_data = {
            "title": "Newspaper Title",
            "content": "Some interesting content",
            "topic": topic.id,
            "publishers": [redactor.id]
        }

        response = self.client.post(reverse("catalog:newspaper-create"), data=form_data)

        if response.status_code == 200 and "form" in response.context:
            if not response.context["form"].is_valid():
                print(response.context["form"].errors)

        self.assertEqual(response.status_code, 302)

    def test_update_newspaper(self):
        redactor = get_user_model().objects.create_user(
            username="test_redactor",
            password="password123"
        )
        topic = Topic.objects.create(name="Science")
        newspaper = Newspaper.objects.create(
            title="Old Title",
            content="Some interesting content",
            topic=topic
        )

        form_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "topic": topic.id,
            "publishers": [redactor.id]
        }

        response = self.client.post(reverse("catalog:newspaper-update", args=[newspaper.id]), data=form_data)

        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")

        if response.status_code == 200 and "form" in response.context:
            if not response.context["form"].is_valid():
                print(response.context["form"].errors)

        self.assertEqual(response.status_code, 302)

    def test_delete_newspaper(self):
        delete_url = reverse("catalog:newspaper-delete", args=[self.newspaper.pk])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Newspaper.objects.filter(title=self.newspaper.title).exists())
