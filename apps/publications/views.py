from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Publication
from .serializers import PublicationSerializer

class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        instance = serializer.save()
        if user:
            instance.authors.set([user])
