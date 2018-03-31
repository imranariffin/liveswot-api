import json


def deserialize(func):
    def _deserialize(request, *args, **kwargs):
        if request.method == 'POST':
            request.body = json.loads(request.body)
        return func(request, *args, **kwargs)
    return _deserialize
