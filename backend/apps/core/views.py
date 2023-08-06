from django.http import JsonResponse


def error_handler_404(request, *args, **kwargs):
    """
    Return a message with status of 404 when page not found.
    """

    return JsonResponse(
        {
            'message': 'Page not found.'
        }, status=404
    )


def error_handler_500(request, *args, **kwargs):
    """
    Return a message with status of 500 when an internal server error occurred.
    """

    return JsonResponse(
        {
            'message': 'An internal server error occurred.'
        }, status=500
    )
