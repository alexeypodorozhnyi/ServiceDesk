from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
import datetime
from django.contrib.auth import logout

class CheckUserLogin(MiddlewareMixin):

    def process_request(self, request):
        if not request.user.is_authenticated and request.path == '/':
            return HttpResponseRedirect('authorisation/login/')


class CheckUserSession(MiddlewareMixin):

    def process_request(self, request):
        if not request.user.is_authenticated:
            return
        if 'last_action' not in request.session.keys():
            request.session['last_action'] = datetime.datetime.now().isoformat()
        timediff = datetime.datetime.now() - datetime.datetime.fromisoformat(request.session.get('last_action'))
        if timediff.total_seconds() > 300 and not request.user.is_staff:
            logout(request)
            HttpResponseRedirect('authorisation/login/')
        request.session['last_action'] = datetime.datetime.now().isoformat()