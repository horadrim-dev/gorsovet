from django import forms
from .models import Post, PostCategory
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget


class PostForm(forms.ModelForm):

    tags = TagField(required=False, widget=LabelWidget)

    class Meta:
        model = Post
        # fields = []
        exclude = []

    def clean(self):
        cleaned_data = super().clean()
        slug = cleaned_data.get("alias")

        try:
            post = Post.objects.get(alias=slug)
        except Post.DoesNotExist:
            post = None

        if post:
            msg = "Пост с alias \"{}\" - уже существует".format(slug)
            self.add_error("alias", msg)

class PostCategoryForm(forms.ModelForm):
    class Meta:
        model = PostCategory
        # fields = []
        exclude = []