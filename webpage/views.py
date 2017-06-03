from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView

from .forms import form_user_login


class GenericWebpageView(TemplateView):
    template_name = 'webpage/index.html'

    def get_template_names(self):
        template_name = "webpage/{}.html".format(self.kwargs.get("template", 'index'))
        try:
            loader.select_template([template_name])
            template_name = "webpage/{}.html".format(self.kwargs.get("template", 'index'))
        except:
            template_name = "webpage/index.html"
        return [template_name]


def feedback_view(request):
    context = {}
    return render(request, 'webpage/user-feedback.html', context)


def faq_view(request):
    context = {}
    return render(request, 'webpage/faq.html', context)


def survey_view(request):
    context = {}
    return render(request, 'webpage/survey2017.html', context)


def imprint(request):
    context = {}
    return render(request, 'webpage/imprint.html', context)


def start_view(request):
    context = {}
    return render(request, 'webpage/index.html', context)


def documentation_view(request):
    context = {}
    return render(request, 'webpage/documentation.html', context)


def markdown_view(request):
    context = {}
    return render(request, 'webpage/markdown_test.html', context)


#################################################################
#               views for login/logout                          #
#################################################################

def user_login(request):
    if request.method == 'POST':
        form = form_user_login(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(request.GET.get('next', '/'))
                else:
                    return HttpResponse('not active.')
            else:
                return HttpResponse('user does not exist')
    else:
        form = form_user_login()
        return render(request, 'webpage/user_login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render_to_response('webpage/user_logout.html')
