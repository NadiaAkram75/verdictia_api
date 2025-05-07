from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Professional
from django.core.mail import send_mail

@receiver(post_save, sender=Professional)
def send_approval_email(sender, instance, **kwargs):
    if instance.status == 'approved':
        user = instance.user
        send_mail(
            subject='Your Account Has Been Approved',
            message=f"Hi {user.full_name},\n\nYour professional account has been approved. You can now log in to the platform.\n\nThank you.",
            from_email='no-reply@yourapp.com',
            recipient_list=[user.email],
        )
