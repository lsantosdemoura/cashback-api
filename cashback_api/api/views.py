from datetime import datetime

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import requests

from api.serializers import UserSerializer, PurchaseSerializer
from core.models import Purchase, User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    @staticmethod
    def get_cashback(purchases):
        pass

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        month = self.request.query_params.get('month', datetime.now().month)
        return self.request.user.purchase_set.filter(date__month=month)


class GatheredCashbackView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        url = "https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback"
        params = {'cpf': self.request.user.cpf}
        headers = {'token': settings.CASHBACK_TOKEN}

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        return Response(response.json()["body"])
