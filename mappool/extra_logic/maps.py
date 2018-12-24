"""
8 5x5 maps, 16 10x10 maps, 6 20x20 maps;  ~25%/50%/20% spread
10 classic, 12 common, 4 exp, 4 new
New maps are 13% of the pool, Exp maps are 14%, Common are 33% and Classic are 40%
"""

import os
import json
import math
from colorama import init, Fore
import logging

logger = logging.getLogger(__name__)

# This file works both as part of the app and standalone as long as there is a json file to get maps from
if __name__ == '__main__':
    init(convert=True)
    logging.basicConfig(level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)  # stdout logs, DEBUG for dev-debugging
else:
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)  # INFO for papertrail on production

curFolder = os.path.dirname(__file__)
fixturePath = os.path.join(curFolder, '../fixtures/')
detailLevel = 1  # 0 - 2, for debugging

logColors = {
    'success1': Fore.GREEN,
    'success2': Fore.CYAN,
    'warning1': Fore.RED,
    'warning2': Fore.YELLOW
}


class TryPickAgain(Exception):
    """Raise to go and pick a different map during pool building"""
    pass


class Map:
    def __init__(self, name, size, category, broken, Tscore, valid):
        self.name = name
        self.size = size
        self.category = category
        self.broken = broken
        self.Tscore = Tscore
        self.valid = valid

    def __str__(self, detailLevel):
        return ('Name - {0:<30} Size - {1:<10} Category - {2:<15} Broken - {3:<10} Total score - {4:<10} Valid - {5:<10} '
                .format(self.name, self.size, self.category, self.broken, self.Tscore, self.valid))


class MapPool:
    def __init__(self,
                query=None,
                poolSizeArg=None,
                specificCatProportions=None,
                specificSizeProportions=None,
                minRating=None,
                randomType=None,
                spread=None,
                ignoreBroken=None,
                sizePercentList=None,
                catPercentList=None):

        self.query = query
        self.poolSize = poolSizeArg or 30
        self.UseSpecifiedCategoryProportions = specificCatProportions if specificCatProportions is not None else True
        self.UseSpecifiedSizeProportions = specificSizeProportions if specificSizeProportions is not None else True
        self.minRatingThreshold = minRating if minRating is not None else 2.0  # 0 - 5
        self.typeOfRandom = randomType if randomType is not None else 3  # One of the randomTypes keys
        self.EvenlySpreadCategoriesOverSizes = spread if spread is not None else True
        self.ignoreBrokenMaps = ignoreBroken if ignoreBroken is not None else True
        # Assigned later
        self.catDict = None
        self.sizeDict = None
        self.UseCatDict = None
        self.UseSizeDict = None
        self.maps = None
        self.pool = None

        # Order has to align, values have to be same as in the sheet, keys are used for logs
        self.categories = {
            'new': 'new',
            'experimental': 'experimental',
            'common': 'common',
            'classic': 'classic',
        }

        self.sizes = {
            '5x5': ['5x5'],
            '10x10': ['10x10'],
            '20x20': ['20x20', '40x40'],
        }
        # defaults
        self.catPercents = {
            'newPercent': 14,
            'expPercent': 13,
            'comPercent': 33,
            'clPercent': 40,
        }
        # defaults
        self.sizePercents = {
            'x5Percent': 25,
            'x10Percent': 55,
            'x20Percent': 20,
        }

        self.randomTypes = {
            0: None,
            1: False,
            2: 1.5,
            3: 2,
            4: 2.5,
            5: 4,
            6: 20,
        }

        self.sizePercentList = sizePercentList or list(self.sizePercents.values())
        self.catPercentList = catPercentList or list(self.catPercents.values())
        self.__createListsAndDicts()

        """
        So to clear stuff up, when not using specific(Cat/Size)Proportions maps are
        pulled from one global list so the weight stays true and no pseudo-random is in place,
        but when specific(Cat/Size)Proportions is True I split maps into dicts
        by whats biggest (amount of sizes or cats) for more efficient and fast picking. This is nice
        for if you e.g. add a small edge-case cat with only a few maps, or wanna
        split 20x20 and 40x40 into different sizes. And weight "truth" is irrelevant
        here since maps would end up limited by category or size one way or another.
        This is likely overcomplicated but thats how I wrote it initially and too lazy to rewrite.
        """

    def __createListsAndDicts(self):
        def __buildCatDict():
            self.UseCatDict = True
            self.catDict = {category: [] for category in self.categories.values()}

        def __buildSizeDict():
            self.UseSizeDict = True
            self.sizeDict = {size: [] for size in self.sizes}
            # Sizes are a bit different to categories due to encapsulation into a list so that 20x20 and 40x40 are counted as the same size

        self.UseCatDict = False
        self.UseSizeDict = False
        if self.UseSpecifiedSizeProportions and self.UseSpecifiedCategoryProportions:
            if len(self.categories) >= len(self.sizes):
                __buildCatDict()
            elif len(self.sizes) > len(self.categories):
                __buildSizeDict()
        elif self.UseSpecifiedCategoryProportions:
            __buildCatDict()
        elif self.UseSpecifiedSizeProportions:
            __buildSizeDict()

        self.catCount = [int(math.floor(self.percIntoNum(category, self.poolSize))) for category in self.catPercentList]
        self.sizeCount = [int(math.floor(self.percIntoNum(size, self.poolSize))) for size in self.sizePercentList]

    @staticmethod
    def percIntoNum(percent, whole):
        return (percent * whole) / 100.0

    @staticmethod
    def fetchMapsIntoJson():  # 'python manage.py loaddata djangoDump.json' after this to load json into an actual DB
        def __convertToPythonBool():
            nonlocal broken
            nonlocal valid
            if broken == 'FALSE':
                broken = False
            else:
                broken = True
            if valid == 'TRUE':
                valid = True
            else:
                valid = False

        def __writeToJson(Maplist):
            with open(f'{fixturePath}/maps.json', 'w') as mdb:
                json.dump({'Maps': [eachmap.__dict__ for eachmap in Maplist]}, mdb, indent=2)
            with open(f'{fixturePath}/djangoDump.json', 'w') as mdb:
                json.dump([{'pk': i + 1, 'model': 'mappool.Map', 'fields': eachmap.__dict__} for i, eachmap in enumerate(Maplist)], mdb, indent=2)

        if __name__ == '__main__':
            import gspread_fetch
        else:
            from . import gspread_fetch
        fetchedMaps = gspread_fetch.fetch()
        Maplist = []
        for name, size, category, broken, Tscore, valid in zip(fetchedMaps[0], fetchedMaps[1], fetchedMaps[2], fetchedMaps[3], fetchedMaps[4], fetchedMaps[5]):
            __convertToPythonBool()
            Maplist.append(Map(name, size, category, broken, Tscore, valid))
        try:
            __writeToJson(Maplist)
        except FileNotFoundError:
            os.mkdir(fixturePath)
            __writeToJson(Maplist)
        except Exception:
            print('Error while trying to fetch/write data from the spreadsheet.')
            exit()

    def __call__(self):
        self.checkProportions()
        self.adjustSizes(cats=False)
        self.adjustSizes(cats=True)
        self.fetchMapsFromJsonOrQuery()
        self.pool = self.buildPool()
        try:
            avg = round(self._averagePoolRating(self.pool), 2)
            return {
                'Pool': self.pool[0],
                'Average': avg,
                'x5': self.pool[1],
                'x10': self.pool[2],
                'x20': self.pool[3],
                'new': sum(self.pool[4]),
                'exp': sum(self.pool[5]),
                'common': sum(self.pool[6]),
                'classic': sum(self.pool[7])
            }
        except TypeError:
            return self.pool
        except Exception as ex:
            return ex

    # Just an internal check, app uses api queries for configuring the pool settings, it's checks are in mappool/views.py
    def checkProportions(self):
        if self.UseSpecifiedSizeProportions is True and sum(self.sizePercentList) != 100:
            print('Sum of size percentages is not equal to 100!')
            exit()
        if self.UseSpecifiedCategoryProportions is True and sum(self.catPercentList) != 100:
            print('Sum of category percentages is not equal to 100!')
            exit()

    # Since proportions are passed as % we go and adjust counts so that catCount and sizeCount == poolSize
    def adjustSizes(self, cats=True):
        decimals = []
        if cats is True:
            percentList = self.catPercentList
            mapCount = self.catCount
        else:
            percentList = self.sizePercentList
            mapCount = self.sizeCount

        for percentage in percentList:
            roundedDown = math.floor(self.percIntoNum(percentage, self.poolSize))
            decimals.append(self.percIntoNum(percentage, self.poolSize) - roundedDown)
        while sum(mapCount) != self.poolSize:
            if sum(mapCount) < self.poolSize:
                i = decimals.index(max(decimals))
                mapCount[i] += 1
            elif sum(mapCount) > self.poolSize:
                i = decimals.index(min(decimals))
                mapCount[i] -= 1
            decimals[i] = 0

    def fetchMapsFromJsonOrQuery(self):
        if self.query is None:
            with open(f'{fixturePath}/maps.json', 'r') as mdb:
                self.maps = json.load(mdb)
            if not self.UseCatDict and not self.UseSizeDict:
                pass
            elif self.UseCatDict:
                self.catDict = {category: [amap for amap in self.maps['Maps']
                if amap['category'] == category]for category in self.categories.values()}
            elif self.UseSizeDict:
                self.sizeDict = {size: [amap for amap in self.maps['Maps'] if amap['size'] == size] for size in self.sizes}
        else:
            self.maps = json.loads(self.query)
            addKey = {'Maps': self.maps}
            dumpKey = json.dumps(addKey)
            self.maps = json.loads(dumpKey)
            if not self.UseCatDict and not self.UseSizeDict:
                self.maps = {'Maps': [amap['fields'] for amap in self.maps['Maps']]}
            elif self.UseCatDict:
                self.catDict = {category: [amap['fields'] for amap in self.maps['Maps']
                if amap['fields']['category'] == category] for category in self.categories.values()}
            elif self.UseSizeDict:
                self.sizeDict = {size: [amap['fields'] for amap in self.maps['Maps'] if amap['fields']['size'] == size] for size in self.sizes}

    # Here is an exercise on logic Kappa
    def buildPool(self):
        from numpy.random import choice
        from random import randint
        iterCount = 0
        iterCountLimit = 3000
        pool = []
        forcePick = False
        otherSizeIsFull = False
        minCatInSize = 0
        mapCounter = 0
        weights = self.__weighTheMaps()
        dynSizeCounter, antiRepeat, sizeCounter, catCounter, mapsForPool = self.__buildPoolBuildData()
        minCatInSize = 1
        # Complex over complicated the Zen dictates, but the man didn't listen
        while (mapCounter < self.poolSize) and (iterCount < iterCountLimit):
            for i, nested in enumerate(mapsForPool):
                if ((self.UseCatDict and sum(catCounter[i]) < self.catCount[i])
                or (self.UseSizeDict and sum(sizeCounter[i]) < self.sizeCount[i])
                or (not self.UseCatDict and not self.UseSizeDict)):
                    iterCount += 1
                    if weights is None:
                        pick = randint(0, len(nested) - 1)
                    else:
                        pick = int(choice(range(len(nested)), 1, p=weights[i]))
                    try:
                        # We iterate over size or cat dict so it's easy to count one of those, but not both
                        # If we need to limit the other one too we calculate how much maps there is in cats/sizes and compare vs the limit
                        if self.UseSizeDict and self.UseSpecifiedCategoryProportions:
                            catCounterSum = 0
                            index = None
                            for j, cat in enumerate(list(self.categories.values())):
                                if nested[pick]['category'] == cat:
                                    index = j
                            catCounterSum = sum(catCounter[index])
                            if catCounterSum >= self.catCount[index]:
                                raise TryPickAgain
                        elif self.UseCatDict and self.UseSpecifiedSizeProportions:
                            sizeCounterSum = 0
                            index = None
                            for j, size in enumerate(list(self.sizes.values())):
                                for size_ in size:
                                    if nested[pick]['size'] == size_:
                                        index = j
                            sizeCounterSum = sum(sizeCounter[index])
                            if sizeCounterSum >= self.sizeCount[index]:
                                raise TryPickAgain
                        for j in antiRepeat[i]:
                            if pick == j:
                                raise TryPickAgain
                    except TryPickAgain:
                        continue
                    else:
                        # Used for even spread of cats over sizes, note that it can stil be uneven in the end cause some cats/sizes fill earlier than others
                        if self.UseCatDict:
                            minCatInSize = min([size[i] for size in sizeCounter])
                            dynSizeCounter = [size[i] for size in sizeCounter]
                        elif self.UseSizeDict or not (self.UseSizeDict or self.UseCatDict):
                            index = None
                            for j, cat in enumerate(list(self.categories.values())):
                                if nested[pick]['category'] == cat:
                                    index = j
                            minCatInSize = min([size[index] for size in sizeCounter])
                            dynSizeCounter = [size[index] for size in sizeCounter]
                        # If a cat has same amount of maps in each size it tries to force pick
                        for j, size in enumerate(sizeCounter[1:]):
                            if self.UseCatDict and sizeCounter[0][i] != size[i]:
                                break
                            elif self.UseSizeDict or not (self.UseSizeDict or self.UseCatDict) and sizeCounter[0][index] != size[index]:
                                # index may not be initiated yet?
                                break
                        else:
                            forcePick = True
                        # Main logic check
                        if (nested[pick]['valid'] is False
                        or (self.ignoreBrokenMaps is True and nested[pick]['broken'] is True)
                        or float(nested[pick]['Tscore']) < self.minRatingThreshold):
                            self.__buildPoolLog(sizeCounter, catCounter, i, pick, forcePick, iterCount, nested, pool, status='skipped')
                            continue
                        try:
                            for j, sizeList in enumerate(list(self.sizes.values())):
                                for size in sizeList:
                                    # Check if some other size is full
                                    for k in range(len(self.sizes)):
                                        if self.UseSpecifiedSizeProportions and k != j and sum(sizeCounter[k]) >= self.sizeCount[k]:
                                            otherSizeIsFull = True
                                    if (nested[pick]['size'] == size and (sum(sizeCounter[j]) >= self.sizeCount[j] and self.UseSpecifiedSizeProportions is True
                                    or (not forcePick and (self.EvenlySpreadCategoriesOverSizes is True and dynSizeCounter[j] > minCatInSize and not otherSizeIsFull)))):
                                        self.__buildPoolLog(sizeCounter, catCounter, i, pick, forcePick, iterCount, nested, pool, status='skipped')
                                        raise TryPickAgain
                        except TryPickAgain:
                            continue
                        else:
                            mapCounter, sizeCounter, catCounter = self.__buildPoolUpdateCounters(pick, nested, sizeCounter, catCounter, mapCounter)
                            pool.append(nested[pick])
                            antiRepeat[i].append(pick)
                            self.__buildPoolLog(sizeCounter, catCounter, i, pick, forcePick, iterCount, nested, pool, status='appended')
                            forcePick = False
        if iterCount >= iterCountLimit:
            pool = 'Not enough maps to process the request, change or reset your settings.'
        self.__buildPoolLog(sizeCounter, catCounter, i, pick, forcePick, iterCount, nested, pool, status='finished')
        if isinstance(pool, str):
            return pool
        return [pool, sum(sizeCounter[0]), sum(sizeCounter[1]), sum(sizeCounter[2]), catCounter[0], catCounter[1], catCounter[2], catCounter[3]]

    def __weighTheMaps(self):
        def __weightTheMapsBuildData():
            if self.UseCatDict:
                mapsToWeigh = self.catDict.values()
                weightList = [[] for category in self.categories]
                scoreSum = [0.0 for category in self.categories]
            elif self.UseSizeDict:
                mapsToWeigh = self.sizeDict.values()
                weightList = [[] for size in self.sizes]
                scoreSum = [0.0 for size in self.sizes]
            elif self.UseCatDict is False:
                mapsToWeigh = [self.maps['Maps']]
                weightList = [[]]
                scoreSum = [0.0]
            else:
                print('Invalid category control value.')
                exit()
            return mapsToWeigh, weightList, scoreSum

        if self.randomTypes.get(self.typeOfRandom) is None:
            return None
        elif self.randomTypes.get(self.typeOfRandom) is False:
            curved = False
        else:
            curved = True
            curveStrength = self.randomTypes.get(self.typeOfRandom)
        mapsToWeigh, weightList, scoreSum = __weightTheMapsBuildData()
        if curved is True:
            def floatScore(score):
                return curveStrength**float(score) - 1
        elif curved is False:
            floatScore = float
        for i, nested in enumerate(mapsToWeigh):
            for j, eachmap in enumerate(nested):
                weightList[i].append(floatScore(eachmap['Tscore']))
                scoreSum[i] += weightList[i][j]
            for j, eachmap in enumerate(weightList[i]):
                try:
                    weightList[i][j] = 1.0 / (scoreSum[i] / eachmap)
                except ZeroDivisionError:
                    weightList[i][j] = 0.0
                    continue
        return weightList

    # Depending on if it's UseCatDict or UseSizeDict we will have an easy way to count sizes or cats, but not the other
    def __buildPoolBuildData(self):
        if self.UseCatDict:
            dynSizeCounter = None
            antiRepeat = [[] for category in self.categories]
            sizeCounter = [[0 for category in self.categories] for size in self.sizes]
            catCounter = [[0 for size in self.sizes] for category in self.categories]
            mapsForPool = [category for category in self.catDict.values()]
        elif self.UseSizeDict:
            dynSizeCounter = None
            antiRepeat = [[] for size in self.sizes]
            sizeCounter = [[0 for category in self.categories] for size in self.sizes]
            catCounter = [[0 for size in self.sizes] for category in self.categories]
            mapsForPool = [size for size in self.sizeDict.values()]
        else:
            if len(self.categories) > len(self.sizes):
                dynSizeCounter = [0 for cat in self.categories]
            else:
                dynSizeCounter = [0 for size in self.sizes]
            antiRepeat = [[]]
            sizeCounter = [[0 for category in self.categories] for size in self.sizes]
            catCounter = [[0 for size in self.sizes] for category in self.categories]
            mapsForPool = [allMaps for allMaps in [self.maps['Maps']]]

        return dynSizeCounter, antiRepeat, sizeCounter, catCounter, mapsForPool

    def __buildPoolUpdateCounters(self, pick, nested, sizeCounter, catCounter, mapCounter):
        for i, sizeList in enumerate(self.sizes.values()):
            for size in sizeList:
                for j, category in enumerate(self.categories.values()):
                    if nested[pick]['size'] == size and nested[pick]['category'] == category:
                        sizeCounter[i][j] += 1
                        catCounter[j][i] += 1
        mapCounter += 1
        return mapCounter, sizeCounter, catCounter

    def __buildPoolLog(self, sizeCounter, catCounter, i, pick, forcePick, iterCount, nested, pool, status='skipped'):
        if status == 'skipped':
            logger.debug(
                '{0} {1} {2} skipped,  pick is {3[size]:<7} poolsize is {4:<3} current catsize is {5:<3} '
                'category is {3[category]:<15} map is {3[name]:<25} forcePick is {6:<3} iter is {7}'
                .format(sizeCounter[0], sizeCounter[1], sizeCounter[2], nested[pick], sum(sizeCounter[0]) + sum(sizeCounter[1])
                        + sum(sizeCounter[2]), sizeCounter[0][i] + sizeCounter[1][i] + sizeCounter[2][i], forcePick, iterCount))
        elif status == 'appended':
            logger.debug(
                '{0} {1} {2} appended, pick is {3[size]:<7} poolsize is {4:<3} current catsize is {5:<3} '
                'category is {3[category]:<15} map is {3[name]:<25} forcePick is {6:<3} iter is {7}'
                .format(sizeCounter[0], sizeCounter[1], sizeCounter[2], nested[pick], sum(sizeCounter[0]) + sum(sizeCounter[1])
                        + sum(sizeCounter[2]), sizeCounter[0][i] + sizeCounter[1][i] + sizeCounter[2][i], forcePick, iterCount))
        elif status == 'finished':
            if isinstance(pool, str):
                logger.info(f'{logColors["warning1"]} Pool got stuck with these settings: '
                    f'{logColors["warning2"]}Pool size - {self.poolSize:<4};{logColors["warning1"]} '
                    f'Category control is {self.UseSpecifiedCategoryProportions:<2};{logColors["warning2"]} '
                    f'Size control is {self.UseSpecifiedSizeProportions:<2};{logColors["warning1"]} 5x5 is {sum(sizeCounter[0]):<3}; '
                     f'{logColors["warning2"]}10x10 is {sum(sizeCounter[1]):<3}; {logColors["warning1"]}20x20 is {sum(sizeCounter[2]):<3};'
                     f'{logColors["warning2"]} new is {sum(catCounter[0]):<3};{logColors["warning1"]} exp is {sum(catCounter[1]):<3}; '
                      f'{logColors["warning2"]}common is {sum(catCounter[2]):<3};{logColors["warning1"]} classic is {sum(catCounter[3]):<3};'
                      f'{logColors["warning2"]} min rating is {self.minRatingThreshold:<2} ; '
                      f'{logColors["warning1"]}type of random is {self.typeOfRandom:<1};{logColors["warning2"]} even spread is '
                      f'{self.EvenlySpreadCategoriesOverSizes:<1}')
            else:
                logger.info(f'{logColors["success1"]}Pool was built with these settings: '
                    f'{logColors["success2"]}Pool size - {self.poolSize:<4};{logColors["success1"]} '
                    f'Category control is {self.UseSpecifiedCategoryProportions:<2};{logColors["success2"]} '
                    f'Size control is {self.UseSpecifiedSizeProportions:<2};{logColors["success1"]} 5x5 is {sum(sizeCounter[0]):<3}; '
                     f'{logColors["success2"]}10x10 is {sum(sizeCounter[1]):<3}; {logColors["success1"]}20x20 is {sum(sizeCounter[2]):<3}; '
                     f'{logColors["success2"]} new is {sum(catCounter[0]):<3};{logColors["success1"]} exp is {sum(catCounter[1]):<3}; '
                      f'{logColors["success2"]}common is {sum(catCounter[2]):<3};{logColors["success1"]} classic is {sum(catCounter[3]):<3}; '
                      f'{logColors["success2"]} min rating is {self.minRatingThreshold:<2} ; '
                      f'{logColors["success1"]}type of random is {self.typeOfRandom:<1};{logColors["success2"]} even spread is '
                      f'{self.EvenlySpreadCategoriesOverSizes:<1}')

    def _averagePoolRating(self, pool):
        sumOfRating = 0
        for eachmap in pool[0]:
            sumOfRating += float(eachmap['Tscore'])
        avgRating = sumOfRating / self.poolSize
        return avgRating

    def printPool(self):  # Just for running as __main__
        if isinstance(self.pool, str):
            print(self.pool)
        else:
            print('5x5')
            for eachmap in self.pool[0]:
                if eachmap['size'] == '5x5':
                    print(self.output(eachmap, detailLevel=detailLevel))
            print('10x10')
            for eachmap in self.pool[0]:
                if eachmap['size'] == '10x10':
                    print(self.output(eachmap, detailLevel=detailLevel))
            print('20x20')
            for eachmap in self.pool[0]:
                if eachmap['size'] == '20x20' or eachmap['size'] == '40x40':
                    print(self.output(eachmap, detailLevel=detailLevel))
            print('\nAverage rating of this pool is: {}\n'.format(round(self._averagePoolRating(self.pool), 2)))

    def printAllMaps(self):
        with open(f'{fixturePath}/maps.json', 'r') as mdb:
            maps = json.load(mdb)
            for eachmap in maps['Maps']:
                print(self.output(eachmap))

    @staticmethod
    def output(aMap, detailLevel=1):
        if detailLevel is 2:
            return ('Name - {0:<30} Size - {1:<10} Category - {2:<15} Broken - {3:<10} Total score - {4:<10} Valid - {5:<6} '
                    .format(aMap['name'], aMap['size'], aMap['category'], aMap['broken'], aMap['Tscore'], aMap['valid']))
        elif detailLevel is 1:
            return ('Name - {0:<30} Size - {1:<10} Category - {2:<15} Total score - {3:<5} '
                    .format(aMap['name'], aMap['size'], aMap['category'], aMap['Tscore']))
        else:
            return ('Name - {0:<30}'.format(aMap['name']))


if __name__ == '__main__':
    some_pool = MapPool(query=None,
                poolSizeArg=30,
                specificCatProportions=True,
                specificSizeProportions=True,
                minRating=2,
                randomType=3,
                spread=True,
                ignoreBroken=True,
                sizePercentList=None,
                catPercentList=None)
    # some_pool.fetchMapsIntoJson()
    some_pool()
    some_pool.printPool()
    # some_pool.printAllMaps()
