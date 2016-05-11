from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy

from .forms import form_user_login


def start_view(request):
	context = RequestContext(request)
	return render(request, 'webpage/index.html', context)


#################################################################
#				views for login/logout							#
#################################################################

def user_login(request):
	errors=[]
	if request.method == 'POST':
		form = form_user_login(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(username=cd['username'],password=cd['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(request.GET.get('next','/'))
				else:
					return HttpResponse('not active.')
			else:
				return HttpResponse('user does not exist')
	else:
		form = form_user_login()
		return render(request, 'webpage/user_login.html', {'form':form})


def user_logout(request):
	logout(request)
	return render_to_response('webpage/user_logout.html')
