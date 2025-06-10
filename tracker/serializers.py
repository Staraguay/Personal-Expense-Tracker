from rest_framework import serializers
from .models import Transaction, MoneyTransfer

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'description', 'value_cad', 'category', 'date','transaction_type','value_usd','shop','payment_type','isd','tax_ec']

class MoneyTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyTransfer
        fields = ['id', 'platform', 'usd_value', 'commission', 'cad_value', 'date', 'change_rate', 'processing_days', 'isd', 'tax']
