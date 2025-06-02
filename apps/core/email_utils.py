"""
Email utility functions for the Pet Adoption Platform
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_adoption_application_notification(application):
    """Send email notification when adoption application is submitted"""
    try:
        # Email to shelter
        shelter_subject = f'New Adoption Application for {application.pet.name}'
        shelter_html_message = render_to_string('emails/new_application_shelter.html', {
            'application': application,
            'pet': application.pet,
            'applicant': application.applicant,
        })
        shelter_plain_message = strip_tags(shelter_html_message)
        
        send_mail(
            shelter_subject,
            shelter_plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [application.pet.shelter.email],
            html_message=shelter_html_message,
            fail_silently=True,
        )
        
        # Email to applicant
        applicant_subject = f'Application Submitted for {application.pet.name}'
        applicant_html_message = render_to_string('emails/application_confirmation.html', {
            'application': application,
            'pet': application.pet,
            'applicant': application.applicant,
        })
        applicant_plain_message = strip_tags(applicant_html_message)
        
        send_mail(
            applicant_subject,
            applicant_plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [application.applicant.email],
            html_message=applicant_html_message,
            fail_silently=True,
        )
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_application_status_update(application):
    """Send email notification when application status changes"""
    try:
        subject = f'Update on Your Application for {application.pet.name}'
        html_message = render_to_string('emails/application_status_update.html', {
            'application': application,
            'pet': application.pet,
            'applicant': application.applicant,
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [application.applicant.email],
            html_message=html_message,
            fail_silently=True,
        )
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_adoption_completion_notification(application):
    """Send email notification when adoption is completed"""
    try:
        # Email to adopter
        adopter_subject = f'Congratulations! {application.pet.name} is Now Yours!'
        adopter_html_message = render_to_string('emails/adoption_completion.html', {
            'application': application,
            'pet': application.pet,
            'adopter': application.applicant,
        })
        adopter_plain_message = strip_tags(adopter_html_message)
        
        send_mail(
            adopter_subject,
            adopter_plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [application.applicant.email],
            html_message=adopter_html_message,
            fail_silently=True,
        )
        
        # Email to shelter
        shelter_subject = f'Adoption Completed: {application.pet.name}'
        shelter_html_message = render_to_string('emails/adoption_completion_shelter.html', {
            'application': application,
            'pet': application.pet,
            'adopter': application.applicant,
        })
        shelter_plain_message = strip_tags(shelter_html_message)
        
        send_mail(
            shelter_subject,
            shelter_plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [application.pet.shelter.email],
            html_message=shelter_html_message,
            fail_silently=True,
        )
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
