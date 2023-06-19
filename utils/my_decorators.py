from django.http import HttpRequest, Http404

def permission_checker_decorator_factory(data=None):
    def permission_checker_decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            print(data)
            if request.user.is_authenticated and request.user.is_superuser:
                return func(request, *args, **kwargs)
            else:
                raise Http404

        return wrapper

    return permission_checker_decorator
