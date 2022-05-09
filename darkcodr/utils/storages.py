import os
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from django.template.defaultfilters import slugify


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"

    def _clean_name(self, name):
        return name

    def _normalize_name(self, name):
        if name.startswith('/static/'):
            name = name.lstrip("/static")

        name = self.location + name
        return name


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    default_acl = "public-read"
    file_overwrite = False

    def _clean_name(self, name):
        return name

    def _normalize_name(self, name):
        if name.startswith('/static/'):
            name = name.lstrip("/static")

        name = self.location + name
        return name


class ProtectedRootS3Boto3Storage(S3Boto3Storage):
    location = "protected"
    default_acl = "private"
    file_overwrite = False
    custom_domain = False

    def _clean_name(self, name):
        return name

    def _normalize_name(self, name):
        if name.startswith('/static/'):
            name = name.lstrip("/static")

        name = self.location + name
        return name


def get_logo_upload_folder(instance, pathname):
    "A standardized pathname for uploaded files and images."
    root, ext = os.path.splitext(pathname)
    return "{0}/logo/{1}/{2}{3}".format(
        "IMG", slugify(instance.name), slugify(root), ext
    )

def get_file_upload_folder(instance, pathname):
    "A standardized pathname for uploaded files and designs."
    root, ext = os.path.splitext(pathname)
    if instance.type == "FILE":
        return f"FILE/{instance.slug}/{slugify(root)}{ext}"
    else:
        return f"DESIGN/{instance.slug}/{slugify(root)}{ext}"

def get_training_video_upload_folder(instance, pathname):
    "A standardized pathname for uploaded training videos."
    root, ext = os.path.splitext(pathname)
    return f"TRAINING/{instance.training.slug}/{instance.id}/{instance.slug}/{slugify(root)}{ext}"
