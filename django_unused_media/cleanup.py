# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

import os


def _get_file_fields():
    """
        Get all fields which are inherited from FileField
    """

    fields = []

    for m in models.get_models():
        for f in m._meta.get_fields():
            if isinstance(f, models.FileField):
                fields.append(f)

    return fields


def get_used_media():
    """
        Get media which are still used in models
    """

    media = []

    for f in _get_file_fields():
        is_null = {
            '%s__isnull' % f.name: True,
        }
        is_empty = {
            '%s' % f.name: '',
        }

        for t in f.model.objects.values(f.name).exclude(**is_empty).exclude(**is_null):
            media.append(t.get(f.name))

    return media


def _get_all_media():
    """
        Get all media from MEDIA_ROOT
    """

    media = []

    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for name in files:
            media.append(os.path.relpath(os.path.join(root, name), settings.MEDIA_ROOT))

    return media


def get_unused_media():
    """
        Get media which are not used in models
    """

    all_media = _get_all_media()
    used_media = get_used_media()

    return [t for t in all_media if t not in used_media]


def _remove_media(files):
    """
        Delete file from media dir
    """
    for f in files:
        os.remove(os.path.join(settings.MEDIA_ROOT, f))


def remove_unused_media():
    """
        Remove unused media
    """
    _remove_media(get_unused_media())


def remove_empty_dirs(path=settings.MEDIA_ROOT):
    """
        Recursively delete empty directories; return True if everything was deleted.
    """

    if not os.path.isdir(path):
        return False

    if all([remove_empty_dirs(os.path.join(path, filename)) for filename in os.listdir(path)]):
        os.rmdir(path)
        return True
    else:
        return False