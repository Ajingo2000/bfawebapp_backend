from django.shortcuts import render, redirect
from .models import Subscriber, EmailTemplate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q
# Create your views here.

def subscribe_email(request):
    
    sub_email = request.POST['email']
    print(sub_email)
    if request.method == 'POST':
        subscriber = Subscriber(
            email=sub_email
        )

        subscriber.save()

        context = {'email': subscriber.email}
        email_content = render_to_string('newsletter/thanks-for-subscribing.html', context)

        email_subject = 'Thank you for Subscribing'
        recipient_list = [subscriber.email]
        from_email = settings.EMAIL_HOST_USER

        send_mail(
            email_subject,
            '',
            from_email,
            recipient_list,
            html_message=email_content,
            fail_silently=False
        )

        return render(request, 'newsletter/subscribed.html', context)
