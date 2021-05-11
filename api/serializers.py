from rest_framework import serializers
from .models import Profile, Game, Strategy
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class GameSerializer(serializers.ModelSerializer):
    team_capres = serializers.ReadOnlyField(source='get_team_capres')
    opposition_capres = serializers.ReadOnlyField(
        source='get_opposition_capres')
    team_pl = serializers.ReadOnlyField(source='get_team_pl')
    opposition_pl = serializers.ReadOnlyField(source='get_opposition_pl')

    team_perc_result = serializers.ReadOnlyField(source='get_perc_team_result')
    opposition_perc_result = serializers.ReadOnlyField(
        source='get_perc_opposition_result')

    class Meta:
        model = Game
        fields = '__all__'


class BetSerializer(serializers.ModelSerializer):

    bet_pl = serializers.SerializerMethodField()
    strat_num = serializers.SerializerMethodField()

    def get_bet_pl(self, obj):
        try:
            return obj.bet_pl
        except:
            return None

    def get_strat_num(self, obj):
        try:
            return obj.strat_num
        except:
            return None

    class Meta:
        model = Game
        fields = '__all__'


class StrategySerializer(serializers.ModelSerializer):
    games = GameSerializer(many=True)

    class Meta:
        model = Strategy
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    lookup_field = 'username'
    strategies = StrategySerializer(many=True)
    # update4 here https://django.cowhite.com/blog/create-and-update-django-rest-framework-nested-serializers/

    class Meta:
        model = Profile
        fields = ['username', 'id', 'strategies', 'supporting', 'email']

    def update(self, instance, validated_data):

        strategies_data = validated_data.pop('strategies')
        instance.email = validated_data.get('email', instance.email)
        instance.supporting = validated_data.get(
            'supporting', instance.supporting)
        instance.strategies.clear()

        for strategy in strategies_data:
            strategy, created = Strategy.objects.get_or_create(
                title=strategy['title'])

            instance.strategies.add(strategy)
        instance.save()
        return instance


class TestSerializer(serializers.ModelSerializer):
    handicap = serializers.IntegerField()
    team_perc_result = serializers.ReadOnlyField(source='get_perc_team_result')

    class Meta:
        model = Game
        fields = ('team_perc_result', 'handicap')
