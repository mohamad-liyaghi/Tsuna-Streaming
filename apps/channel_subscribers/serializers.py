from rest_framework import serializers


class SubscriberListSerializer(serializers.Serializer):
    """
    Represent a list of subscribers
    """
    user = serializers.CharField()
    date = serializers.DateTimeField()
