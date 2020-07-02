from rest_framework import serializers

from core.models import Purchase, User


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
    def create(self, validated_data):
        request = self.context['request']
        reseller = request.user

        if reseller.cpf == '15350946056':
            validated_data['status'] = 'Aprovado'

        validated_data['reseller'] = reseller
        purchase = Purchase.objects.create(**validated_data)
        return purchase

    class Meta:
        model = Purchase
        fields = ['code', 'value', 'date', 'reseller', 'status']
        read_only_fields = ['status']
