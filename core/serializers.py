import json


def deserialize(func):
    def _deserialize(request, *args, **kwargs):
        if request.method in ('POST', 'PUT',):
            request.body = json.loads(request.body)
        return func(request, *args, **kwargs)
    return _deserialize
