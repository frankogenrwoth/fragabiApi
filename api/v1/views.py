from rest_framework import viewsets
from api.models import FragabiUser
from api.v1.serializers import FragabiUserSerializer


class FragabiUserViewSet(viewsets.ModelViewSet):
    queryset = FragabiUser.objects.all()
    serializer_class = FragabiUserSerializer