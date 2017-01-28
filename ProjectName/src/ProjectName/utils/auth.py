from django.core.urlresolvers import reverse


def get_login_url():
    return reverse('account_login')
