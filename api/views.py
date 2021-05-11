from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.db.models import Q, F, Case, Value, When
from .models import Profile, Game, Strategy
# , MeanRev2StDevSerializer
from .serializers import ProfileSerializer, BetSerializer, UserSerializer, GameSerializer, StrategySerializer, TestSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        response = {'message': 'You cannot update the ratings like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cannot create the ratings like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class StrategyViewSet(viewsets.ModelViewSet):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class SupporterViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user = self.request.user
        chosen_team = Profile.objects.filter(user=user)[0].supporting
        return Game.objects.filter(ft1__gt=F('ft2'), team=chosen_team, match_status='ft').annotate(bet_pl=F('home_odds')-1).union(Game.objects.filter(ft1__lt=F('ft2'), team=chosen_team, match_status='ft').annotate(bet_pl=Value(-1))).union(Game.objects.filter(ft1__gt=F('ft2'), opposition=chosen_team, match_status='ft').annotate(bet_pl=Value(-1))).union(Game.objects.filter(ft1__lt=F('ft2'), opposition=chosen_team, match_status='ft').annotate(bet_pl=F('away_odds')-1)).order_by('-match_utc_time')

    serializer_class = BetSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class BlindAwayViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Game.objects.filter(ft1__gt=F('ft2'),  match_status='ft').annotate(bet_pl=Value(-1)).union(Game.objects.filter(ft1__lt=F('ft2'), match_status='ft').annotate(bet_pl=F('away_odds')-1)).order_by('-match_utc_time')

    serializer_class = BetSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
