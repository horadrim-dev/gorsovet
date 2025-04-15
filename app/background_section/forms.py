from django import forms
from django.core.exceptions import ValidationError
from .models import BackgroundSection

class SectionForm(forms.ModelForm):
    
    class Meta:
        model = BackgroundSection
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("background_image")
        use_parallax = cleaned_data.get("use_parallax")

        if use_parallax and not image:
            msg = "Чтобы использовать эффект параллакса, необходимо задать фоновое изображение"
            self.add_error('background_image', msg)