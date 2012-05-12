django-events
=============

Django app for managing public and private events.

Its features include:
- Ability to define multiple events
- Ability for multiple ticket types with different prices per event (e.g. "Regular" / "Student")
- Payment integration with Stripe (https://stripe.com/)
- List public events on the homepage
- Have a secret link for private events
- Email to acknowledge purchase + reminder email when your event is coming up

Requirements
---------------

- Django framework (ver. 1.3.1+, available at https://www.djangoproject.com/download/)
- Stripe library for online payments (ver. 1.5+, available at https://stripe.com/docs/libraries).

Stripe settings
---------------

In order to handle online payments, you need the Stripe account. After successful
registration at https://stripe.com/, you will be given a set of test and production keys.
Use them in the settings STRIPE_PUBLIC_KEY & STRIPE_PRIVATE_KEY. Make sure to
use the test keys first to check if everything is working well.

E-mail settings
---------------

If you want the app to send e-mails to users to acknowledge the purchase or
to remind them of an upcoming event, configure the e-mail settings in the
settings.py file (otherwise, comment out the e-mail-related lines)

If everything is configured properly, a message will be sent each time a
purchase is accepted.

You can send the reminder e-mails by typing:

./manage.py send_reminders

This will identify all the events that happen within REMINDER_DAYS (7 by default)
days and will notify all the users that bought the tickets for those events.