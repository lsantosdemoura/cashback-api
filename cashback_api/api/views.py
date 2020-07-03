import calendar
from datetime import datetime, timedelta
from decimal import Decimal

import requests
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import CharField, DecimalField, Sum, Value
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PurchaseSerializer, UserSerializer
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
    serializer_class = PurchaseSerializer

    def get_date_range(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end_date = datetime.today()

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start_date = end_date - timedelta(days=30)

        return start_date, end_date

    @staticmethod
    def _get_cashback_percentage(value):
        if value <= 1000:
            return Decimal('0.10')
        elif value <= 1500:
            return Decimal('0.15')
        else:
            return Decimal('0.20')

    @staticmethod
    def absolute_date_range(start_date, end_date):
        first_month_day_date = start_date - timedelta(days=start_date.day)
        last_month_day = calendar.monthrange(start_date.year, start_date.month)[1]
        last_month_day_date = end_date + timedelta(days=last_month_day)
        first_month_day_date = first_month_day_date.strftime('%Y-%m-%d')
        last_month_day_date = last_month_day_date.strftime('%Y-%m-%d')

        return first_month_day_date, last_month_day_date

    def get_cashback(self, purchases_absolute_range, purchases_official_range):
        values_sum_by_month = purchases_absolute_range.values('date__month').annotate(Sum('value'))

        cashback_queryset = []
        for month_and_sum in values_sum_by_month:
            percentage = self._get_cashback_percentage(
                value=month_and_sum['value__sum']
            )
            cashback = month_and_sum['value__sum'] * percentage

            # creates a filter and annotates the `cashback_value` and the
            # `cashback_percentage` to the queryset
            cashback_queryset.append(
                purchases_official_range.filter(date__month=month_and_sum['date__month'])
                .annotate(cashback_value=Value(cashback, output_field=DecimalField()))
                .annotate(
                    cashback_percentage=Value(
                        f'{str(percentage)[2:]}%', output_field=CharField()
                    )
                )
            )

        return [queryset for subqueryset in cashback_queryset for queryset in subqueryset]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """

        start_date, end_date = self.get_date_range()
        first_month_day_date, last_month_day_date = self.absolute_date_range(start_date, end_date)

        end_date = end_date.strftime('%Y-%m-%d')
        start_date = start_date.strftime('%Y-%m-%d')

        purchases_absolute_range = self.request.user.purchase_set.filter(
            date__range=[first_month_day_date, last_month_day_date]
        )
        purchases_official_range = self.request.user.purchase_set.filter(
            date__range=[start_date, end_date]
        )

        cashback_queryset = self.get_cashback(
            purchases_absolute_range, purchases_official_range
        )

        return cashback_queryset


class GatheredCashbackView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    permission_classes = (IsAuthenticated,)

    @method_decorator(cache_page(60*60*2))
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        url = 'https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback'
        params = {'cpf': self.request.user.cpf}
        headers = {'token': settings.CASHBACK_TOKEN}

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        return Response(response.json()['body'])
