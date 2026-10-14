from django.urls import path

from . import views

app_name = "blog"       # ad sahəsi: reverse("blog:post_detail") — başqa app-ın adları ilə qarışmır

urlpatterns = [
    # [DƏRS 7]
    path("", views.post_list, name="post_list"),
    path("post/new/", views.post_create, name="post_create"),  
    path("post/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    path("post/<int:post_id>/delete/", views.post_delete, name="post_delete"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("comment/<int:comment_id>/reply/", views.comment_reply, name="comment_reply"),
    path("about/", views.about, name="about"),

    # [EV 7]
    path("contact/", views.contact, name="contact"),
    path("categories/", views.category_list, name="category_list"),
    path("category/new/", views.category_create, name="category_create"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("author/<str:name>/", views.author_posts, name="author_posts"),
    path("stats/", views.stats, name="stats"),

    # [EV 8]
    path("latest/", views.latest, name="latest"),

    # [PRAKTİKA 10]
    path("tag/<slug:slug>/", views.tag_detail, name="tag_detail"),

    # [EV 10]
    path("tags/", views.tag_list, name="tag_list"),
    path("search/<str:word>/", views.search, name="search"),     # bonus
]
