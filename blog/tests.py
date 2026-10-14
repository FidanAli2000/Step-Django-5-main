# Yalnız müəllim üçün — dərsdə YAZILMIR, tələbəyə göstərilmir.
# Layihənin hər URL-ni yoxlayır:  python manage.py test
from django.test import TestCase
from django.urls import reverse

from .models import Post, Category, Tag, Comment


class Lesson10Tests(TestCase):
    fixtures = ["demo_full"]

    def test_all_pages_open(self):
        urls = ["/", "/post/1/", "/about/", "/contact/", "/categories/", "/category/oyunlar/",
                "/author/nigar/", "/stats/", "/latest/", "/tag/python/", "/tags/", "/search/git/"]
        for url in urls:
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_404(self):
        for url in ["/post/99/", "/category/futbol/", "/tag/yoxdur/"]:
            self.assertEqual(self.client.get(url).status_code, 404, url)

    def test_fk_and_reverse_relation(self):
        oyunlar = Category.objects.get(slug="oyunlar")
        self.assertEqual(oyunlar.posts.count(), 2)
        self.assertContains(self.client.get("/category/oyunlar/"), "FIFA")
        self.assertContains(self.client.get("/"), "/category/oyunlar/")

    def test_protect(self):
        from django.db.models import ProtectedError
        with self.assertRaises(ProtectedError):
            Category.objects.get(slug="oyunlar").delete()

    def test_comments_only_active(self):
        r = self.client.get("/post/2/")
        self.assertContains(r, "Redstone-u indi başa düşdüm")
        self.assertNotContains(r, "Ucuz telefonlar")
        Post.objects.get(id=2).delete()                       # CASCADE
        self.assertEqual(Comment.objects.filter(post_id=2).count(), 0)

    def test_tags(self):
        r = self.client.get("/tag/python/")
        self.assertContains(r, "Python-da ilk addım")
        self.assertContains(r, "Git nədir")
        self.assertNotContains(r, "FIFA")
        self.assertContains(self.client.get("/tags/"), "(2)")

    def test_counts_similar_stats(self):
        self.assertContains(self.client.get("/categories/"), "(2)")
        self.assertContains(self.client.get("/post/2/"), "FIFA")          # oxşar post
        r = self.client.get("/stats/")
        self.assertContains(r, "Minecraft")                               # ən çox şərh
        self.assertContains(r, "3 şərh")

    def test_admin(self):
        from django.contrib.auth.models import User
        User.objects.create_superuser("admin", "a@a.az", "step12345")
        self.client.login(username="admin", password="step12345")
        for url in ["/admin/blog/post/", "/admin/blog/post/1/change/", "/admin/blog/comment/",
                    "/admin/blog/tag/add/", "/admin/blog/category/"]:
            self.assertEqual(self.client.get(url).status_code, 200, url)
