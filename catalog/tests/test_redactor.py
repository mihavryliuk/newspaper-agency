from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Redactor, Newspaper

REDACTOR_URL = reverse("catalog:redactor-list")


class PublicRedactorTest(TestCase):
    def test_login_required(self):
        test_response = self.client.get(REDACTOR_URL)
        self.assertNotEqual(test_response.status_code, 200)


class PrivateRedactorTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_redactor",
            password="mypass321",
            years_of_experience=5
        )
        self.client.force_login(self.user)

    def test_retrieve_redactors(self):
        Redactor.objects.create(
            username="redactor1",
            password="pass123",
            years_of_experience=3,
            first_name="John",
            last_name="Doe"
        )
        Redactor.objects.create(
            username="redactor2",
            password="pass456",
            years_of_experience=2,
            first_name="Jane",
            last_name="Doe"
        )
        test_response = self.client.get(REDACTOR_URL)
        self.assertEqual(test_response.status_code, 200)
        redactors = Redactor.objects.all()
        self.assertEqual(
            list(test_response.context["redactor_list"]),
            list(redactors)
        )
        self.assertTemplateUsed(test_response, "catalog/redactor_list.html")

    def test_search_redactor_by_username(self):
        redactor1 = Redactor.objects.create(
            username="redactor1",
            password="pass123",
            years_of_experience=3,
            first_name="John",
            last_name="Doe"
        )

        response = self.client.get(REDACTOR_URL, {"username": "redactor1"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(redactor1, response.context["redactor_list"])

        response = self.client.get(REDACTOR_URL, {"username": "redactor"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(redactor1, response.context["redactor_list"])

        response = self.client.get(REDACTOR_URL, {"username": "notfound"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(redactor1, response.context["redactor_list"])

    def test_create_redactor(self):
        form_data = {
            "username": "new_redactor",
            "password1": "newpass321",
            "password2": "newpass321",
            "years_of_experience": 1,
            "first_name": "Alice",
            "last_name": "Smith"
        }
        response = self.client.post(
            reverse("catalog:redactor-create"),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Redactor.objects.filter(username="new_redactor").exists()
        )

    def test_update_redactor(self):
        redactor = Redactor.objects.create(
            username="redactor_to_update",
            password="updatepass",
            years_of_experience=3,
            first_name="OldName",
            last_name="OldSurname"
        )

        form_data = {
            "years_of_experience": 5
        }
        response = self.client.post(reverse(
            "catalog:redactor-update",
            args=[redactor.id]),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        redactor.refresh_from_db()
        self.assertEqual(redactor.years_of_experience, 5)

    def test_delete_redactor(self):
        redactor = Redactor.objects.create(
            username="redactor_to_delete",
            password="deletepass",
            years_of_experience=2,
            first_name="DeleteMe",
            last_name="LastName"
        )

        response = self.client.post(reverse(
            "catalog:redactor-delete",
            args=[redactor.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Redactor.objects.filter(id=redactor.id).exists())
