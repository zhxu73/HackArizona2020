from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.decorators import action
#from tutorial.quickstart.serializers import UserDataSerializer
from rest_framework.response import Response
from rest_framework import status
import json
from tutorial.quickstart.flight_info import parse_input, error_response, dispatch_intent
import traceback


class GoogleAssistantActionViewSet(viewsets.ViewSet):
    http_method_names = [
        'get', 'post'
    ]

    def create(self, request):
        try:
            json_obj = json.loads(request.body.decode("utf-8"))
        except json.decoder.JSONDecodeError:
            return Response("", status=status.HTTP_400_BAD_REQUEST)
        #print(json.dumps(json_obj, indent=4, sort_keys=True))

        try:
            result = parse_input(json_obj)
            return Response(dispatch_intent(result["intent"], result))

        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response(error_response(), status=status.HTTP_400_BAD_REQUEST)

