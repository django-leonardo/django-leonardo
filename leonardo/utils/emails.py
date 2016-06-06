from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader
from django.utils.html import strip_tags


def send_templated_email(subject, template_name, context,
                         recipients, sender=None, bcc=None,
                         fail_silently=True, files=None):
    """
    send_templated_mail() is a wrapper around Django's e-mail routines that
    allows us to easily send multipart (text/plain & text/html) e-mails using
    templates that are stored in the database. This lets the admin provide
    both a text and a HTML template for each message.

    template_name is the slug of the template to use for this message (see
        models.EmailTemplate)

    context is a dictionary to be used when rendering the template

    recipients can be either a string, eg 'a@b.com', or a list of strings.

    sender should contain a string, eg 'My Site <me@z.com>'. If you leave it
        blank, it'll use settings.DEFAULT_FROM_EMAIL as a fallback.

    bcc is an optional list of addresses that will receive this message as a
        blind carbon copy.

    fail_silently is passed to Django's mail routine. Set to 'True' to ignore
        any errors at send time.

    files can be a list of file paths to be attached, or it can be left blank.
        eg ('/tmp/file1.txt', '/tmp/image.png')

    """

    c = Context(context)
    if not sender:
        sender = settings.DEFAULT_FROM_EMAIL

    template = loader.get_template(template_name)

    text_part = strip_tags(template.render(c))
    html_part = template.render(c)

    if type(recipients) == str:
        if recipients.find(','):
            recipients = recipients.split(',')
    elif type(recipients) != list:
        recipients = [recipients, ]

    msg = EmailMultiAlternatives(subject,
                                 text_part,
                                 sender,
                                 recipients,
                                 bcc=bcc)
    msg.attach_alternative(html_part, "text/html")

    if files:
        if type(files) != list:
            files = [files, ]

        for file in files:
            msg.attach_file(file)

    return msg.send(fail_silently)
