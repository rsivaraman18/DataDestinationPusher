from rest_framework import serializers
from .models import Account, Destination


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'account_id', 'account_name', 'app_secret_token', 'website']



class DestinationSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source='account.account_name', read_only=True)  # Include account name
    
    class Meta:
        model = Destination
        fields = '__all__'
        # fields = ['id', 'account', 'url', 'http_method', 'headers']
