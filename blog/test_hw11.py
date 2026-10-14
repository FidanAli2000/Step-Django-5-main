from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .forms import CommentForm, ContactForm, PostForm
from .models import Category, ContactMessage, Post


class Homework11Tests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Tarix", slug="tarix")
        self.post = Post.objects.create(
            title="Maraqlı tarix", author="Test", category=self.category, content="Məzmun"
        )

    def test_delete_requires_post(self):
        url = reverse("blog:post_delete", args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())
        response = self.client.post(url)
        self.assertRedirects(response, reverse("blog:post_list"))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
        self.assertEqual(list(get_messages(response.wsgi_request))[0].level_tag, "warning")

    def test_contact_validation_and_storage(self):
        self.assertFalse(ContactForm(data={"name": "Test", "email": "bad", "message": "1234567890"}).is_valid())
        self.assertFalse(ContactForm(data={"name": "Test", "email": "a@b.com", "message": "123"}).is_valid())
        response = self.client.post(reverse("blog:contact"), {
            "name": "Test", "email": "test@example.com", "message": "Salam, necəsiniz?"
        })
        self.assertRedirects(response, reverse("blog:contact"))
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_post_title_validation(self):
        values = {"author": "Test", "content": "Məzmun", "category": self.category.pk}
        for title in ("abc", "SALAM"):
            self.assertFalse(PostForm(data={**values, "title": title}).is_valid())
        self.assertTrue(PostForm(data={**values, "title": "Salam dünya"}).is_valid())

    def test_comment_name_validation(self):
        for name in ("admin", "Admin", "ADMIN", " admin "):
            self.assertFalse(CommentForm(data={"name": name, "text": "Salam"}).is_valid())

    def test_category_create(self):
        response = self.client.post(reverse("blog:category_create"), {
            "name": "Elm", "slug": "elm", "description": "Elm xəbərləri"
        })
        self.assertRedirects(response, reverse("blog:category_list"))
        self.assertTrue(Category.objects.filter(slug="elm").exists())

    def test_message_levels(self):
        values = {"title": "Yeni mövzu", "author": "Test", "content": "Məzmun", "category": self.category.pk}
        response = self.client.post(reverse("blog:post_create"), values)
        self.assertEqual(list(get_messages(response.wsgi_request))[0].level_tag, "success")
        post = Post.objects.get(title="Yeni mövzu")
        response = self.client.post(reverse("blog:post_edit", args=[post.pk]), {**values, "title": "Dəyişmiş mövzu"})
        self.assertEqual(list(get_messages(response.wsgi_request))[0].level_tag, "info")
