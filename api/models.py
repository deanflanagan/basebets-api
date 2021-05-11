from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Game(models.Model):
    sport = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    league = models.CharField(max_length=30)
    tournament_id = models.IntegerField()
    match_id = models.CharField(max_length=8)
    match_utc_time = models.DateTimeField()
    match_status = models.CharField(max_length=3)
    team = models.CharField(max_length=30)
    opposition = models.CharField(max_length=30)
    ft1 = models.IntegerField(null=True)
    ft2 = models.IntegerField(null=True)
    home_odds = models.DecimalField(max_digits=6, decimal_places=3)
    away_odds = models.DecimalField(max_digits=6, decimal_places=3)
    draw_odds = models.DecimalField(
        max_digits=6, decimal_places=3, blank=True, null=True)
    # bet_pl = models.DecimalField(null=True, decimal_places=3, max_digits=6)

    @property
    def get_team_capres(self):
        if self.ft2:
            return self.ft2 - self.ft1
        return None

    @property
    def get_opposition_capres(self):
        if self.ft1:
            return self.ft1 - self.ft2
        return None

    @property
    def get_team_pl(self):
        if self.ft1:
            return self.home_odds - 1 if self.ft1 > self.ft2 else -1
        return None

    @property
    def get_opposition_pl(self):
        if self.ft1:
            return self.away_odds - 1 if self.ft2 > self.ft1 else -1
        return None

    @property
    def get_perc_team_result(self):
        if self.ft1:
            return - (1/self.away_odds / (1/self.home_odds + 1/self.away_odds)) if self.ft1 < self.ft2 else 1 - (1/self.home_odds / (1/self.home_odds + 1/self.away_odds))
        return None

    @property
    def get_perc_opposition_result(self):
        if self.ft1:
            return -(1/self.home_odds / (1/self.home_odds + 1/self.away_odds)) if self.ft1 > self.ft2 else 1 - (1/self.away_odds / (1/self.home_odds + 1/self.away_odds))

    class Meta:
        ordering = ['match_utc_time']


class Strategy(models.Model):
    title = models.CharField(max_length=32)
    games = models.ManyToManyField(Game, related_name='games', blank=True)
    viewset_url = models.CharField(max_length=32, default='api')

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    strategies = models.ManyToManyField(
        Strategy, related_name='strategies', blank=True)
    supporting = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, blank=True)

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print(instance)
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print(instance)
    instance.profile.save()


# for profile idea: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
# for filter on viewset: https://sunscrapers.com/blog/django-rest-framework-tutorial-part-3-custom-fields/
