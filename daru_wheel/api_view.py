from rest_framework import viewsets
from rest_framework import permissions

# from rest_framework import generics #, permissions, viewsets, serializers,filters, status
from .models import Stake
from .serializers import StakeSerializer


class StakeViewSet(viewsets.ModelViewSet):
    """ViewSet for the Stake class"""

    permission_classes = (permissions.IsAuthenticated,)

    queryset = Stake.objects.all()

    # def get_queryset(self):
    #     queryset = Stake.objects.all()#filter(user_id=self.kwargs["user"])
    #     return queryset

    serializer_class = StakeSerializer

    # search_fields = ('target_currency', )
    # ordering_fields = ('created_at', )
