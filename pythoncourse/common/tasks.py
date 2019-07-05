"""Asynchronous tasks of the common for all apps are defined here."""

from django.core.mail import send_mail
from django.conf import settings


def send_mail_data(mail_dict):
    """
    Function to send emails.

    Input Params:
        mail_dict(dict): collection dictionary with following details,
            to(list): list of to email ids.
            subject(str): email subject.
            text(str): text content
            html(str): html file
            from: from address
    Return:
        success response
    """
    # try:
    print 'sending email to ', mail_dict['to_emails']
    # send_mail(
    #     mail_dict['subject'],
    #     mail_dict['text'],
    #     settings.EMAIL_HOST_USER,
    #     mail_dict['to_emails'],
    #     fail_silently=False,
    #     html_message=mail_dict['html']
    # )

    print 'email send'
    # except:
    #     print 'Email failed.'
    #     pass
    # return 1
