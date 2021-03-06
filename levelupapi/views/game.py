"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, Game_type
from django.db.models import Count, Q
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import permissions


class CurrentUserIsCreatorCheck(permissions.BasePermission):
    """Allows owner of an object to edit it. """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif obj.gamer == request.auth.user:
            return True
        elif obj.gamer.id != request.auth.user.id:
            return False
        
        # return obj.gamer.id == request.auth.user.id
    
    
    
class GameView(ViewSet):
    """Level up game view"""
    permission_classes = [ CurrentUserIsCreatorCheck ]
    queryset = Game.objects.none()
    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            gamer = Gamer.objects.get(user=request.auth.user)
            games = Game.objects.annotate(event_count=Count('event'), user_event_count=Count('event',
            filter=Q(event__organizer = gamer)))
            game = games.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        
        gamer = Gamer.objects.get(user=request.auth.user)
        games = Game.objects.annotate(event_count=Count('event'), user_event_count=Count('event',
        filter=Q(event__organizer = gamer)))
        
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
        
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
         Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game_type = Game_type.objects.get(pk=request.data["game_type_id"])

        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            skill_level=request.data["skill_level"],
            number_of_players=request.data['number_of_players'],
            gamer=gamer,
            game_type=game_type
    )
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
        Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)
        self.check_object_permissions(request, game)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]
        game_type = Game_type.objects.get(pk=request.data["game_type"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    
    
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    event_count = serializers.IntegerField(default=None)
    user_event_count = serializers.IntegerField(default=None)
    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'skill_level', 'number_of_players', 'game_type', 'gamer', "game_type", 'event_count', 'user_event_count' )
        depth = 1