from rest_framework import serializers
from memberships.models import Membership, Subscription


class MembershipSerializer(serializers.ModelSerializer):
    """
    Serializer for Creating and Listing Memberships.
    """

    class Meta:
        model = Membership
        fields = [
            "title",
            "description",
            "price",
            "active_months",
            "is_available",
            "token",
        ]

        read_only_fields = ["token", "is_available"]
        write_only_fields = ["description"]


class MembershipDetailSerializer(serializers.ModelSerializer):
    lookup_field = "token"

    class Meta:
        model = Membership
        fields = [
            "title",
            "description",
            "price",
            "active_months",
            "is_available",
            "token",
        ]

        read_only_fields = ["token"]


class MembershipSubscribeSerializer(serializers.ModelSerializer):
    membership = serializers.StringRelatedField()

    class Meta:
        model = Subscription
        fields = ["membership", "start_date", "end_date", "token"]

        read_only_fields = fields

    def save(self, **kwargs):
        """
        Override save and add user and membership to the context.
        """
        return Subscription.objects.create(
            user=self.context["user"], membership=self.context["membership"]
        )
