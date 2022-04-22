from .models import Notification


def create_notification(request, reciever, notification_type):
    notification = Notification.objects.create(reciever=reciever, notification_type=notification_type, creator=request.user)
