from rest_framework import serializers
from accounts.models import Plan


class PlanListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = ["title", "description", "price", "active_months", "is_available", "token",]

        extra_kwargs = {
            'description': {'write_only': True},       
            'token': {"read_only" : True}
        }

class PlanDetailSerializer(serializers.ModelSerializer):
    lookup_field = "token"

    class Meta:
        model = Plan
        fields = ["title", "description", "price", "active_months", "is_available", "token",]

        extra_kwargs = {
            'token': {"read_only" : True}
        }

class AvailabilitySerializer(serializers.Serializer):
    pass