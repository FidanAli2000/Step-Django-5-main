from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import CommentForm, PostForm, ContactForm, CategoryForm
from .models import Post, Category, Tag, Comment, ContactMessage

# ─────────────────────────── postlar ───────────────────────────

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post uğurla yaradıldı.")
            return redirect(post)
    else:
        form = PostForm()
    
    return render(request, "blog/post_form.html", {"form": form, "page_title": "Yeni post"})


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.info(request, "Post uğurla yeniləndi.")
            return redirect(post)
    else:
        form = PostForm(instance=post)
    
    return render(request, "blog/post_form.html", {"form": form, "post": post, "page_title": "Postu redaktə et"})


def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        messages.warning(request, "Post silindi.")
        return redirect("blog:post_list")
    return render(request, "blog/post_confirm_delete.html", {"post": post})


def post_list(request):                                           
    posts = Post.objects.filter(is_published=True)
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, post_id):                                
    post = get_object_or_404(Post, id=post_id, is_published=True)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Şərhiniz uğurla göndərildi.")
            return redirect(post)
    else:
        form = CommentForm()
    
    post.views += 1
    post.save()

    # comments = post.comments.filter(is_active=True)
    comments = post.comments.filter(is_active=True, parent=None) 

    similar = Post.objects.filter(category=post.category, is_published=True)
    similar = similar.exclude(id=post.id)[:3]

    context = {
        "post": post, 
        "comments": comments, 
        "similar": similar, 
        "form": form
    }
    return render(request, "blog/post_detail.html", context)


def about(request):
    return render(request, "blog/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(**form.cleaned_data)
            messages.success(request, "Mesajınız uğurla göndərildi.")
            return redirect("blog:contact")
    else:
        form = ContactForm()
    return render(request, "blog/contact.html", {"form": form})



def comment_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id, is_active=True)
    post = parent_comment.post

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.parent = parent_comment
            reply.save()
            messages.success(request, "Cavabınız uğurla göndərildi.")
            return redirect(post)
    else:
        form = CommentForm()

    context = {
        "form": form,
        "parent_comment": parent_comment,
        "post": post,
    }
    return render(request, "blog/comment_reply.html", context)
# ───────────────────────── kateqoriyalar ─────────────────────────

def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kateqoriya yaradıldı.")
            return redirect("blog:category_list")
    else:
        form = CategoryForm()
    return render(request, "blog/category_form.html", {"form": form})


def category_list(request):
    categories = Category.objects.annotate(post_count=Count("posts"))
    return render(request, "blog/category_list.html", {"categories": categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(is_published=True)
    context = {"category": category, "posts": posts}
    return render(request, "blog/category_detail.html", context)


# ─────────────────────────── teqlər ───────────────────────────

def tag_detail(request, slug):                                    
    tag = get_object_or_404(Tag, slug=slug)
    posts = tag.posts.filter(is_published=True)
    context = {"tag": tag, "posts": posts}
    return render(request, "blog/tag_detail.html", context)


def tag_list(request):                                            
    tags = Tag.objects.annotate(post_count=Count("posts"))
    return render(request, "blog/tag_list.html", {"tags": tags})


# ─────────────────────── digər səhifələr ───────────────────────

def author_posts(request, name):                                 
    posts = Post.objects.filter(author=name, is_published=True)
    context = {"name": name, "posts": posts}
    return render(request, "blog/author_posts.html", context)


def latest(request):                                             
    posts = Post.objects.filter(is_published=True).order_by("-created_at")[:3]
    return render(request, "blog/latest.html", {"posts": posts})


def stats(request):                                              
    published = Post.objects.filter(is_published=True)

    most_commented = published.annotate(comment_count=Count("comments"))
    most_commented = most_commented.order_by("-comment_count").first()

    context = {
        "post_count": published.count(),
        "category_count": Category.objects.count(),
        "top_post": published.order_by("-views").first(),
        "comment_count": Comment.objects.count(),                 
        "tag_count": Tag.objects.count(),                         
        "most_commented": most_commented,                         
    }
    return render(request, "blog/stats.html", context)


def search(request, word):                                        
    posts = Post.objects.filter(title__icontains=word, is_published=True)
    context = {"word": word, "posts": posts}
    return render(request, "blog/search.html", context)
