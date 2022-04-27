"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game_type


class GameTypeView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game_type = Game_type.objects.get(pk=pk)
            serializer = GameTypeSerializer(game_type)
            return Response(serializer.data)
        except Game_type.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        game_types = Game_type.objects.all()
        serializer = GameTypeSerializer(game_types, many=True)
        return Response(serializer.data)
    
class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game_type
        fields = ('id', 'label')    
