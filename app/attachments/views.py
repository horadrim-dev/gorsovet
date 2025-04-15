from django.http import HttpResponse, JsonResponse, Http404, FileResponse
from .models import Attachment
import os

def attachment_download(request, id, *args, **kwargs):
    # media_root = settings.MEDIA_ROOT
    try:
        attachment = Attachment.objects.get(id=id)
    except:
        raise Http404('Файл не найден.')

    if os.path.isfile(attachment._file.path):
        attachment.hits += 1
        attachment.save()
        return FileResponse(
            open(attachment._file.path, 'rb'),
            as_attachment=True,
            filename=attachment.filename
        )
    else:
        raise Http404(
            'Файл "{}" в хранилище не найден.'.format(
                attachment._file.path)
        )