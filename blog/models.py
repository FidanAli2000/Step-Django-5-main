from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)                          # URL-də işlənir, təkrarlana bilməz
    description = models.TextField(blank=True)                    # blank=True → formda boş qala bilər

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"                        # admində "Categorys" yazılmasın

    def __str__(self):
        return self.name


# [PRAKTİKA 10] tələbə yazır — Category-nin əkizi
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# [DƏRS 9] müəllim yazıb
class Post(models.Model):
    title = models.CharField(max_length=200)                      # qısa mətn — max_length = maksimum simvol sayı
    author = models.CharField(max_length=50)                      # hələlik ad; Dərs 12-də User olacaq

    # [DƏRS 10] CharField idi → ForeignKey oldu. Post kateqoriyanın ÖZÜNƏ bağlanır, mətnə yox.
    category = models.ForeignKey(
        Category,                                                 # hansı modelə bağlanır
        on_delete=models.PROTECT,                                 # postu olan kateqoriyanı silmək olmaz
        related_name="posts",                                     # tərs əlaqənin adı: category.posts.all()
    )

    content = models.TextField()                                  # uzun mətn — limitsiz
    is_published = models.BooleanField(default=True)              # dərc olunubmu?
    views = models.PositiveIntegerField(default=0)                # baxış sayı, mənfi ola bilməz
    created_at = models.DateTimeField(auto_now_add=True)          # yaranma vaxtı avtomatik yazılır

    # [EV 9] tapşırıq 5
    is_featured = models.BooleanField(default=False)

    # [DƏRS 10] şəkil — fayl media/posts/ qovluğuna düşür, bazada yalnız yolu saxlanır
    image = models.ImageField(upload_to="posts/", blank=True)

    # [PRAKTİKA 10] bir postun çox teqi, bir teqin çox postu ola bilər
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    class Meta:
        ordering = ["-created_at"]                                

    def __str__(self):                                           
        return self.title
    
    def get_absolute_url(self):                                 
        return reverse("blog:post_detail", args=[self.id])


# [DƏRS 10] müəllim yazır — bir postun çox şərhi olur
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.email}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,                                 # post silinsə, şərhləri də silinir
        related_name="comments",                                  # post.comments.all()
    )
    name = models.CharField(max_length=50)                        # şərh yazanın adı
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # [EV 10] tapşırıq 3 — admin şərhi gizlədə bilsin
    is_active = models.BooleanField(default=True)
    
    parent = models.ForeignKey(
        "self",                                                   # özünə bağlanır
        on_delete=models.CASCADE,                                 # valideyn silinsə, uşaqlar da silinir
        related_name="replies",                                   # tərs əlaqə: comment.replies.all()
        null=True,                                                # parent boş qala bilər
        blank=True,                                               # formda parent boş qala bilər
    )

    class Meta:
        ordering = ["-created_at"]                                # [EV 10] tapşırıq 7 — ən yeni şərh birinci

    def __str__(self):
        return f"{self.name}: {self.text[:30]}"
