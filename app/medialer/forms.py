from django import forms

from . import models


class AlbumForm(forms.ModelForm):

    class Meta:
        model = models.Album
        fields = '__all__'

class AlbumPictureForm(forms.ModelForm):

    class Meta:
        model = models.AlbumPicture
        fields = '__all__'
        widgets = {
            'caption_text': forms.Textarea(attrs={'rows': 2}),
        }


class PluginPictureForm(forms.ModelForm):

    class Meta:
        model = models.PluginPicture
        fields = '__all__'
        # exclude = ['caption_text']
        widgets = {
            'caption_text': forms.Textarea(attrs={'rows': 2}),
        }


# =========================== VIDEO ====================================#

import re

from django import forms
from django.conf import settings



YOUTUBE_URL_RE = re.compile(r'(?:(?:http://|https://|//)?(?:www\.)?youtu\.?be.*).*')
# https://stackoverflow.com/a/9102270
YOUTUBE_VIDEO_ID_RE = re.compile(r'(?:[?&]v=|/embed/|/1/|/v/|https?://(?:www\.)?youtu\.be/)([^&\n?#]+)')
DEFAULT_YOUTUBE_EMBED_URL = '//www.youtube.com/embed/{}'


class VideoPlayerPluginForm(forms.ModelForm):
    class Meta:
        model = models.VideoPlayer
        exclude = []

    def clean_embed_link(self):
        link = self.cleaned_data['embed_link']
        # let's check if it's a youtube url
        # (the low cost version)
        if YOUTUBE_URL_RE.match(link):
            # try to get the video id
            results = YOUTUBE_VIDEO_ID_RE.findall(link)
            if results:
                embed_url = getattr(settings, "DJANGOCMS_VIDEO_YOUTUBE_EMBED_URL", DEFAULT_YOUTUBE_EMBED_URL)
                link = embed_url.format(results[0])
        return link
