from django.db import models
from .extra_logic import maps
from django.core import serializers


class MapManager(models.Manager):
    def getx5(self):
        return super(MapManager, self).filter(size='5x5')

    def getx10(self):
        return super(MapManager, self).filter(size='10x10')

    def getx20(self):
        return super(MapManager, self).filter(size='20x20')

    def getx40(self):
        return super(MapManager, self).filter(size='40x40')


class Map(models.Model):
    name = models.CharField(max_length=50)
    size = models.CharField(max_length=10)
    category = models.CharField(max_length=20)
    broken = models.BooleanField()
    Tscore = models.FloatField()
    valid = models.BooleanField()
    objects = MapManager()

    def __str__(self):
        return self.name


def djangoPool(catControl,
               sizeControl,
               poolSize,
               x5percent,
               x10percent,
               x20percent,
               newPercent,
               expPercent,
               comPercent,
               clsPercent,
               minRating,
               randomType,
               spreadType,
               brokenIgnore):
    mapQuery = Map.objects.all()
    dump = serializers.serialize("json", mapQuery)
    pool = maps.MapPool(query=dump,
                        poolSizeArg=poolSize,
                        specificCatProportions=catControl,
                        specificSizeProportions=sizeControl,
                        minRating=minRating,
                        randomType=randomType,
                        spread=spreadType,
                        ignoreBroken=brokenIgnore,
                        sizePercentList=[x5percent, x10percent, x20percent],
                        catPercentList=[newPercent, expPercent, comPercent, clsPercent])
    poolResult = pool()
    return poolResult
