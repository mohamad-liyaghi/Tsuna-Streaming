from django.http import HttpResponse


def error_handler_404(request, *args, **kwargs):
    '''Return a message when a page cannot be founded. [404]'''

    return HttpResponse("404 Error. Couldnt find the page with given url.", status=404)


def error_handler_500(request, *args, **kwargs):
    '''Return a message when sth goes wrong with server. [500]'''

    return HttpResponse("500 Server error. Please contact our administration.", status=500)