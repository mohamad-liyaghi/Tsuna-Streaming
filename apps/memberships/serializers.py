from rest_framework import serializers
from memberships.models import Membership, Subscription


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


class MembershipSubscribeSerializer(serializers.ModelSerializer):

    membership = serializers.StringRelatedField()

    class Meta:
        model = Subscription
        fields = ["membership", "start_date", "end_date", "token"]

        extra_kwargs = {
                'membership': {"read_only" : True}, 
                'start_date': {"read_only" : True}, 
                'end_date': {"read_only" : True}, 
                'token': {"read_only" : True}, 
            }
        

    def save(self, **kwargs):
        # set user and membership plan and then save the Subscription
        kwargs['user'] = self.context['user']
        kwargs['membership'] = self.context['membership']
        return super().save(**kwargs)