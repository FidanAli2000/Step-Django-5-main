from django import forms

from .models import Comment, Post, Category

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "text"]
        labels = {"name": "Adın", "text": "Rəyin"}
        
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name.strip().lower() == "admin":
            raise forms.ValidationError("admin adı ilə şərh yazmaq olmaz.")
        if len(name.strip()) < 2:
            raise forms.ValidationError("Ad ən azı 2 simvol olmalıdır.")
        return name
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "author", "content", "category", "image", "tags"]
        labels = {
            "title": "Başlıq",
            "author": "Müəllif",
            "content": "Məzmun",
            "category": "Kateqoriya",
            "content": "Məzmun",
            "image": "Şəkil",
            "tags": "Təqlər",
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 5:
            raise forms.ValidationError("Başlıq ən azı 5 simvol olmalıdır.")
        if title.isupper():
            raise forms.ValidationError("Başlığı tam böyük hərflə yazma.")
        return title


class ContactForm(forms.Form):
    name = forms.CharField(label="Ad", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Mesaj", widget=forms.Textarea)

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Mesaj ən azı 10 simvol olmalıdır.")
        return message


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description"]
        labels = {"name": "Ad", "slug": "Slug", "description": "Təsvir"}
