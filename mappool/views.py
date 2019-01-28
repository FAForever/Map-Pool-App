from .models import Map, djangoPool
from itertools import chain


from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import MapSerializer

maps = Map.objects.all().order_by('name')


class MapViewSet(viewsets.ModelViewSet):
    queryset = maps
    serializer_class = MapSerializer

    def list(self, request, format=None):
        try:
            # Custom order since with normal ordering it displays 5x5 after 10x10 and 20x20
            if request.query_params['ordering'] == 'size':
                self.queryset = chain(Map.objects.getx5(),
                                      Map.objects.getx10(),
                                      Map.objects.getx20(),
                                      Map.objects.getx40())
            else:
                self.queryset = Map.objects.all().order_by(request.query_params['ordering'])
        except KeyError:
            pass
        serializer = MapSerializer(self.queryset, many=True)
        return Response(serializer.data)


class MapPoolViewSet(viewsets.ViewSet):
    def __init__(self, *args, **kwargs):
        # Args passed to pool building, overwritten by query if present
        self.pool_args = {
            'catControl': True,
            'sizeControl': True,
            'poolSize': 30,
            'x5percent': 25,
            'x10percent': 55,
            'x20percent': 20,
            'newPercent': 13,
            'expPercent': 14,
            'comPercent': 33,
            'clsPercent': 40,
            'minRating': 2.0,
            'randomType': 3,
            'spreadType': True,
            'brokenIgnore': True
        }
        # Categorized arguments for easier verification
        self.checkbox_inputs = ['catControl', 'sizeControl', 'spreadType', 'brokenIgnore']
        self.size_percents = ['x5percent', 'x10percent', 'x20percent']
        self.cat_percents = ['newPercent', 'expPercent', 'comPercent', 'clsPercent']

    def verify_query(self, request):
        error_responses = {
            'generic_wrong_query': ('Something is wrong with your settings, '
                                  'change or reset them and try again.'),
            'min_rating': 'Min rating has to be between 0 and 5, change or reset your settings.',
            'pool_size': 'Pool size has to be above zero, change or reset your settings. ',
            'size_percents': 'Size percents don\'t sum up to 100, change or reset your settings.',
            'cat_percents': 'Category percents don\'t sum up to 100, change or reset your settings.'
        }
        # Bool verification
        for checkbox in self.checkbox_inputs:
            try:
                if request.query_params[checkbox] == 'false':
                    self.pool_args[checkbox] = False
                elif request.query_params[checkbox] == 'true':
                    self.pool_args[checkbox] = True
                else:
                    return error_responses['generic_wrong_query']
            except (TypeError, ValueError):
                return error_responses['generic_wrong_query']
            except KeyError:
                pass
            except Exception:
                return 'Something went wrong. <1>'
        # Random type verification
        try:
            self.pool_args['randomType'] = int(request.query_params['randomType'])
            if self.pool_args['randomType'] not in range(0, 7):
                return error_responses['generic_wrong_query']
        except (TypeError, ValueError):
            return error_responses['generic_wrong_query']
        except KeyError:
            pass
        except Exception:
            return 'Something went wrong. <2>'
        # Pool size verification
        try:
            self.pool_args['poolSize'] = int(request.query_params['poolSize'])
            if self.pool_args['poolSize'] < 1:
                return error_responses['pool_size']
        except (TypeError, ValueError):
            return error_responses['pool_size']
        except KeyError:
            pass
        except Exception:
            return 'Something went wrong. <3>'
        # Min rating verification
        try:
            self.pool_args['minRating'] = float(request.query_params['minRating'])
            if self.pool_args['minRating'] <= 0 or self.pool_args['minRating'] > 5:
                return error_responses['min_rating']
        except (TypeError, ValueError):
            return error_responses['generic_wrong_query']
        except KeyError:
            pass
        except Exception:
            return 'Something went wrong. <4>'
        # Size percents verification
        size_percent_sum = 0
        for size_percent in self.size_percents:
            try:
                size_percent_to_int = int(request.query_params[size_percent])
                self.pool_args[size_percent] = size_percent_to_int
                size_percent_sum += size_percent_to_int
            except (TypeError, ValueError):
                return error_responses['generic_wrong_query']
            except KeyError:
                size_percent_sum += self.pool_args[size_percent]
            except Exception:
                return 'Something went wrong. <5>'
        if size_percent_sum != 100:
            return error_responses['size_percents']
        # Category percents verification
        cat_percent_sum = 0
        for cat_percent in self.cat_percents:
            try:
                cat_percent_to_int = int(request.query_params[cat_percent])
                self.pool_args[cat_percent] = cat_percent_to_int
                cat_percent_sum += cat_percent_to_int
            except (TypeError, ValueError):
                return error_responses['generic_wrong_query']
            except KeyError:
                cat_percent_sum += self.pool_args[cat_percent]
            except Exception:
                return 'Something went wrong. <6>'
        if cat_percent_sum != 100:
            return error_responses['cat_percents']
        return None

    def list(self, request, format=None):
        query_verif_result = self.verify_query(request)
        if query_verif_result:
            return Response({'error_response': query_verif_result})

        try:
            pool = djangoPool(**self.pool_args)
        except Exception:
            final_response = {'error_response': 'Something went wrong. <7>'}

        try:
            pool_modified = [{'id': i + 1, **map} for i, map in enumerate(pool['Pool'])]
        except TypeError:
            # If not enough maps or something went wrong `pool` returns an error string
            final_response = {'error_response': pool}
        except Exception as ex:
            final_response = {'error_response': 'Something went wrong. <8>'}
        else:
            final_response = {'extra_info': {'Average rating': pool['Average'],
                                             '5x5 count': pool['x5'],
                                             '10x10 count': pool['x10'],
                                             '20x20 count': pool['x20'],
                                             'New count': pool['new'],
                                             'Exp count': pool['exp'],
                                             'Common count': pool['common'],
                                             'Classic count': pool['classic']},
                              'pool': pool_modified}
        return Response(final_response)
