from rest_framework.response import Response


def serialize(func):

    def serialize_swot(swot):
        if swot is None:
            return {}
        return {
            'createdAt': unicode(swot.created),
            'swotId': swot.id,
            'creatorId': swot.created_by_id,
            'title': swot.title,
            'description': swot.description,
        }

    def _serialize(request, *args, **kwargs):
        data, status, errors = func(request, *args, **kwargs)

        if errors:
            return Response({
                'errors': errors
            }, status=status)

        if type(data) == list:
            return Response({
                'data': [
                    serialize_swot(swot) for swot in data
                ]}, status=status)

        swot = data
        return Response({
            'data': serialize_swot(swot)
        }, status=status)
    return _serialize
