import mailchimp
from django.conf import settings
from main import print_stack_trace, immediate_alert

class Mailchimp():

    def __init__(self):
        self.mchimp = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
        try:
            self.mchimp.helper.ping()
        except:
            print_stack_trace()
            immediate_alert("Keen:Mailchimp is Down!")

    def subscribe(self, list_id, customer):
        try:
            self.mchimp.lists.subscribe(list_id,
                                        email={'email': customer.email},
                                        merge_vars={"FNAME":customer.first_name,
                                                    "LNAME":customer.last_name,
                                                    "FULNAME":customer.full_name,
                                                    "NUMBER":customer.get_phone_number(),
                                                    "SOURCE":customer.source.name},
                                        double_optin=False,
                                        update_existing=True,
                                        send_welcome=True)
        except:
            print_stack_trace()
            try:
                immediate_alert("Keen:Issues with Subscribing Customer(%s) to Mailchimp List (%s)" % (customer.id,list_id))
            except: pass