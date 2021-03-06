import logging
from rest_framework import serializers

from core.models import Purchase, User

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'}
    )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['email', 'fullname', 'cpf', 'password']


class PurchaseSerializer(serializers.ModelSerializer):
    cashback_percentage = serializers.CharField(max_length=3, read_only=True)
    cashback_value = serializers.DecimalField(decimal_places=2, max_digits=9, read_only=True)

    def create(self, validated_data):
        request = self.context['request']
        reseller = request.user

        if reseller.cpf == '15350946056':
            validated_data['status'] = 'Aprovado'

        validated_data['reseller'] = reseller
        try:
            purchase = Purchase.objects.create(**validated_data)
        except Exception:
            logger.exception("Error while creating a purchase object.")
        return purchase

    class Meta:
        model = Purchase
        fields = ['code', 'value', 'date', 'reseller', 'status', 'cashback_percentage', 'cashback_value']
        read_only_fields = ['status', 'cashback_percentage', 'cashback_value']
