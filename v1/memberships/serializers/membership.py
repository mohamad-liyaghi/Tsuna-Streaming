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


class MembershipDetailSerializer(serializers.ModelSerializer):
    lookup_field = "token"

    class Meta:
        model = Membership
        fields = ["title", "description", "price", "active_months", "is_available", "token",]

        extra_kwargs = {
            'token': {"read_only" : True}
        }
