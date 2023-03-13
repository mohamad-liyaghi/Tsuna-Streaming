from rest_framework import serializers
from memberships.models import Membership


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ["title", "description", "price", "active_months", "is_available", "token",]

        extra_kwargs = {
            'description': {'write_only': True},       
            'token': {"read_only" : True}
        }