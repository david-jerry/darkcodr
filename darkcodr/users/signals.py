import datetime

from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from django.utils.safestring import mark_safe

from django.dispatch import receiver

from allauth.account.signals import user_signed_up

from darkcodr.utils.logger import LOGGER
from darkcodr.utils.emails import plain_email, support_email, pdf_attachment_email
from darkcodr.utils.unique_generators import unique_id_generator

from .models import Profile, CardDetail

User = get_user_model()


@receiver(pre_save, sender=User)
def generate_unique_id(instance, *args, **kwargs):
    if not instance.unique_id:
        instance.unique_id = unique_id_generator(instance)
        LOGGER.info(f"Created New ID: {instance.unique_id}")

@receiver(post_save, sender=User)
def user_post_save_signal(created, instance, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # CardDetail.objects.create(user=instance)
        body2 = f"""
        Hello {instance.username.title()},
        <br>
        <br>
        Your referral Code is: {instance.unique_id}.
        <br>
        <br>
        <br>
        """

        user_message = get_template('mail/simple_mail.html').render(context={"subject": "REFERRAL ID GENERATED", "body": mark_safe(body2)})
        plain_email(to_email=instance.user.email, subject="Withdrawal Confirmed", body=user_message)
        LOGGER.info("Sent Referral ID to {User}".format(User=instance.username))


@receiver(user_signed_up)
def referral_signals(request, user, **kwargs):
    LOGGER.info("Creating Referral")
    referrer_id = request.session.get("ref_profile")

    admin_body = f"""
    Hello Webmaster,
    <br>
    <br>
    {user.username.title()} Has just successfully signed up.
    <br>
    <br>
    """

    admin_message = get_template('mail/admin_mail.html').render(context={"subject": "New Registration", "body": mark_safe(admin_body)})
    plain_email(to_email="admin@darkcodr.codes", subject="New Registration", body=admin_message)


    if referrer_id is not None:
        recommended_by_user = User.objects.get(id=referrer_id)
        recommender_email = recommended_by_user.email
        new_user = user
        new_user.recommended_by = recommended_by_user
        new_user.save()

        body = f"""
        Hello {recommended_by_user.username.title()},
        <br>
        <br>
        Your referral code: {recommended_by_user.unique_id} was used to refer
        <br>
        <br>
        <strong>NEW USER: {new_user.username.title()}</strong>
        <br>
        <br>
        You earned 3 Darks credits which can be used to purchase items on our platform.
        <br>
        <br>
        """

        body2 = f"""
        Hello {new_user.username.title()},
        <br>
        <br>
        Your have successfully signed up with the referral code: {recommended_by_user.unique_id}
        <br>
        <br>
        We hope you enjoy your experience with us.
        <br>
        <br>
        """

        referrer_message = get_template('mail/simple_mail.html').render(context={"subject": "New Referral", "body": mark_safe(body)})
        user_message = get_template('mail/simple_mail.html').render(context={"subject": "Successful Referrer Registration", "body": mark_safe(body2)})
        plain_email(to_email=user.email, subject="Successful Referrer Registration", body=user_message)
        plain_email(to_email=recommender_email, subject="New Referral Registration", body=referrer_message)
        LOGGER.info(f"Sent new referral registration email to {recommended_by_user.username.title()}")



