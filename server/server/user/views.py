from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class FirstTestViews(APIView):
    """
    """

    @classmethod
    def get(cls, request):
        """
        """
        data = {'mesassge': 'Hello welcome to rest api'}
        return Response(data, status=status.HTTP_200_OK)
