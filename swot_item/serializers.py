from rest_framework.response import Response


def serialize(func):
    def serialize_swot_item(swot_item):
        if swot_item is None:
            return {}
        return {
            'swotItemId': swot_item.id,
            'swotId': swot_item.swot_id,
            'creatorId': swot_item.created_by_id,
            'text': swot_item.text,
            'cardType': swot_item.cardType,
            'score': swot_item.score,
        }

    def _serialize(request, *args, **kwargs):
        data, status, errors = func(request, *args, **kwargs)

        if errors:
            return Response({
                'errors': errors,
            }, status=status)

        if type(data) == list:
            return Response({
                'data': [
                    serialize_swot_item(swot_item) for swot_item in data
                ]}, status=status)

        swot_item = data
        return Response({
            'data': serialize_swot_item(swot_item)
        }, status=status)

    return _serialize
