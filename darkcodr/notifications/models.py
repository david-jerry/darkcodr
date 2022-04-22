from django.conf import settings
from django.db import models
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    FileField,
    ForeignKey,
    GenericIPAddressField,
    ImageField,
    IntegerField,
    ManyToManyField,
    OneToOneField,
    PositiveIntegerField,
    SlugField,
    TextChoices,
    TextField,
    URLField,
    UUIDField,
)
from django.db.models.fields import BigIntegerField
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField

User = settings.AUTH_USER_MODEL

# Create your models here.
class Notification(TimeStampedModel):
    MESSAGE = "message"
    FOLLOWER = "follower"
    LIKE = "like"
    MENTION = "mention"
    CHOICES = (
        (MESSAGE, "Message"),
        (MENTION, "Mention"),
        (FOLLOWER, "Follower"), 
        (LIKE, 'Like')
    )

    reciever = ForeignKey(User, related_name="usernotif", on_delete=CASCADE)
    notification_type = CharField(max_length=20, choices=CHOICES)
    is_read = BooleanField(default=False)
    # notif_info = CharField(max_length=255, blank=True, null=True)
    creator = ForeignKey(User, related_name="notifcreator", on_delete=CASCADE)

    class Meta:
        ordering = ["-created"]
