from rest_framework import serializers
from accounts.models import Plan


class PlanListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = ["title", "description",    "price", "token", "active_months", "is_avaiable"]