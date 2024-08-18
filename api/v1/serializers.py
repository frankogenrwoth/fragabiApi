from api.models import FragabiUser
from rest_framework import serializers


class FragabiUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FragabiUser
        fields = ['id', 'name', 'user_id', 'grade', 'date_added', 'date_modified']
        read_only_fields = ['date_added', 'date_modified']
