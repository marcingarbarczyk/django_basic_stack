from django.http import HttpRequest


def get_ip(request: HttpRequest) -> str:
    """
    Get client's IP address.

    Args:
      request (HttpRequest): The http request from the client

    Returns:
      str: The IP address of the client.
    """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip
