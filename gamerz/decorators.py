from django.http import HttpResponseForbidden

def membership_required(tier):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.membership.tier != tier:
                return HttpResponseForbidden("You don't have access to this feature.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
