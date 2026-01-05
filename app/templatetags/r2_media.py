from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def r2_media(path):
    """
    Generate R2 URL for media files.
    Use in templates like: {% r2_media 'videos/my-video.mp4' %}
    """
    if settings.R2_ACCOUNT_ID and settings.R2_ACCESS_KEY_ID:
        # Production - use R2 URL
        return f'https://{settings.R2_BUCKET_NAME}.{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com/{path}'
    else:
        # Development - use local media URL
        return f'{settings.MEDIA_URL}{path}'