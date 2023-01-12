from rest_framework import serializers
from accounts.models import Plan


class PlanListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = ["title", "description", "price", "active_months", "is_avaiable", "token",]

        extra_kwargs = {
            'description': {'write_only': True},       
            'token': {"read_only" : True}
        }