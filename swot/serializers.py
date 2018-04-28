from rest_framework.response import Response


def serialize(func):
    def _serialize(request, *args, **kwargs):
        data, status, errors = func(request, *args, **kwargs)

        if type(data) == list:
            return Response({
                'data': [{
                    'swotId': swot.id,
                    'creatorId': swot.created_by_id,
                    'title': swot.title,
                    'description': swot.description,
                } for swot in data]}, status=status)

        swot = data
        return Response({
            'data': {
                'swotId': swot.id,
                'creatorId': swot.created_by_id,
                'title': swot.title,
                'description': swot.description,
            }}, status=status)
    return _serialize
