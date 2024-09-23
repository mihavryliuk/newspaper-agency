from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Topic

TOPIC_LIST_URL = reverse("catalog:topic-list")


class PublicTopicTest(TestCase):
    def test_login_required(self):
        test_response = self.client.get(TOPIC_LIST_URL)
        self.assertNotEqual(test_response.status_code, 200)


class PrivateTopicTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        self.client.force_login(self.user)

    def test_retrieve_topics(self):
        Topic.objects.create(name="Django")
        Topic.objects.create(name="Python")

        test_response = self.client.get(TOPIC_LIST_URL)
        self.assertEqual(test_response.status_code, 200)
        topics = Topic.objects.all()
        self.assertEqual(list(test_response.context["topic_list"]), list(topics))
        self.assertTemplateUsed(test_response, "catalog/topic_list.html")

    def test_search_topic_by_name(self):
        topic1 = Topic.objects.create(name="Django")
        topic2 = Topic.objects.create(name="Python")

        response = self.client.get(TOPIC_LIST_URL, {"name": "Django"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(topic1, response.context["topic_list"])
        self.assertNotIn(topic2, response.context["topic_list"])

        response = self.client.get(TOPIC_LIST_URL, {"name": "Pyt"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(topic2, response.context["topic_list"])
        self.assertNotIn(topic1, response.context["topic_list"])

    def test_create_topic(self):
        create_url = reverse("catalog:topic-create")
        form_data = {"name": "New Topic"}
        response = self.client.post(create_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Topic.objects.filter(name="New Topic").exists())

    def test_update_topic(self):
        topic = Topic.objects.create(name="Old Topic")
        update_url = reverse("catalog:topic-update", args=[topic.pk])
        form_data = {"name": "Updated Topic"}
        response = self.client.post(update_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        topic.refresh_from_db()
        self.assertEqual(topic.name, "Updated Topic")

    def test_delete_topic(self):
        topic = Topic.objects.create(name="To be deleted")
        delete_url = reverse("catalog:topic-delete", args=[topic.pk])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Topic.objects.filter(name="To be deleted").exists())
