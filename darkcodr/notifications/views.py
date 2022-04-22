from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from darkcodr.notifications.models import Notification


# Create your views here.
@login_required
def notification_list(request):
    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)

    if goto != '':
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True
        notification.save()

        if notification.notification_type == Notification.MESSAGE:
            return redirect('dm:message', user_id=notification.creator.id)
        elif notification.notification_type == Notification.FOLLOWER:
            return redirect('users:detail', username=notification.creator.username)
        elif notification.notification_type == Notification.LIKE:
            return redirect('users:detail', username=notification.reciever.username)
        elif notification.notification_type == Notification.MENTION:
            return redirect('users:detail', username=notification.creator.username)

    return render(request, 'notifications/list.html')
