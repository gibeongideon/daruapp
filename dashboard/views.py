
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template


@login_required(login_url="/user/login")
def index(request):
    print(request.user)
    return render(request, "dashboard/index.html")


@login_required(login_url="user/login")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try: 
        load_template = request.path.split('spinchannel/')[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template('error-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('error-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/user/login")
def icons(request):

    return render(request, "dashboard/ui-icons.html")


@login_required(login_url="/user/login")
def maps(request):
    return render(request, "dashboard/ui-maps.html")


@login_required(login_url="/user/login")
def topo(request):
    return render(request, "dashboard/ui-typography.html")


@login_required(login_url="/user/login")
def support(request):
    return render(request, "dashboard/page-rtl-support.html")
