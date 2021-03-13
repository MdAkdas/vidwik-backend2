import mandrill
from vidwik.global_variable import MANDRILL_API_KEY


def sendMail(template_name, to_email, name,subject, global_merge_vars):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)

        # print(to_email)
        # print(name)

        global_merge_vars = [
            {
                'name': 'UNSUB',
                'content': 'https://videowiki.pt/',
            }

        ]

        message = {
            'from_email': 'puneet@boarded.in',
            'from_name': 'Puneet Gupta',
            'global_merge_vars': global_merge_vars,
            # need reply mail
            'headers': {'Reply-To': 'support@boarded.in'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': subject,
            'tags': ['password-resets'],
            'text': 'Example text content',
            'to': [{'email': to_email,
                    'name': name,
                    'type': 'to'}],
        }

        result = mandrill_client.messages.send_template(
            template_name=template_name, template_content=[], message=message, send_async=False, ip_pool='Main Pool')
        print(result)
        '''
        [{'_id': 'abc123abc123abc123abc123abc123',
        'email': 'recipient.email@example.com',
        'reject_reason': 'hard-bounce',
        'status': 'sent'}]
        '''

    except mandrill.Error as e:
        # Mandrill errors are thrown as exceptions
        # print 'A mandrill error occurred: %s - %s' % (e.__class__, e)

        print('A mandrill error occurred:')
        # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
        raise

#
# signup_template = "getting-started" #signup
# template_name = "videowiki-mail"
# template_name3 = "transaction-successful"
# template_name4 = "getboarded"
# template_name5 = "default"
# template_name6 = "brand-hunt-ambassadors"
# template_name7 = "b00-welcome-dpd-02"
# template_name8 = "a02-user-notification-to-admins-dpd-01-internal"
# template_name9 = "01-alex-dpd-en-introduction"
