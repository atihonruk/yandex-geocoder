# http://api.yandex.com/maps/doc/geocoder/desc/concepts/About.xml

import argparse
import requests
from collections import OrderedDict
from pprint import pprint

YANDEX_GEOCODER_URL = 'http://geocode-maps.yandex.ru/1.x/'

FORMAT_CHOICES = ('json', 'xml')
KIND_CHOICES = ('house', 'street', 'metro', 'district', 'locality')
LANG_CHOICES = ('ru-RU', 'uk-UA', 'be-BY', 'en-US', 'en-BR', 'tr-TR')

PRECISIONS = {k:v for k, v in enumerate(('other', 'street', 'range', 'near','number','exact'))}


def geocode(geocode, kind=None, format=None, ll=None, spn=None,
            rspn=None, results=None, skip=None, lang=None):
    """For detailed description of parameters and its defaults, see
    http://api.yandex.com/maps/doc/geocoder/desc/concepts/input_params.xml
    """

    if kind and kind not in KIND_CHOICES:
        raise ValueError('kind should be one of ' + str(KIND_CHOICES))

    if format and format not in FORMAT_CHOICES:
        raise ValueError('format should be either json or xml')

    if lang and lang not in LANG_CHOICES:
        raise ValueError('lang should be one of ' + str(LANG_CHOICES))

    params = {k: v for k, v in vars().items() if v}
    r = requests.get(YANDEX_GEOCODER_URL, params=params)
    if r.status_code == requests.codes.ok:
        if format == 'json':
            return r.json()
        else:
            return r.text
    else:
        r.raise_for_status()


def _flatten(d):
    for k, v in d.items():
        if isinstance(v, dict):
            yield from _flatten(v)
        else:
            yield (k, v)


def get_geo_objects(result):
    """Converts GeoObjects from geocoder query results
    in json format to flat list of dicts.
    """
    for o in result['response']['GeoObjectCollection']['featureMember']:
        yield OrderedDict(_flatten(o))


def get_most_precise(objs):
    """Returns most precise GeoObject. To determine 'most precise',
    uses scores defined in PRECISIONS dictionary.
    """
    return sorted(objs, key=lambda o: PRECISIONS.get(o['precision'], 0))[-1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('geocode')
    parser.add_argument('--kind', choices=KIND_CHOICES)
    parser.add_argument('--format', choices=FORMAT_CHOICES)
    parser.add_argument('--ll')
    parser.add_argument('--spn')
    parser.add_argument('--rspn')
    parser.add_argument('--results')
    parser.add_argument('--skip')
    parser.add_argument('--lang', choices=LANG_CHOICES)
    parser.add_argument('--flat', action='store_true', default=False,
                        help='flatten results for better readability (only for json format)')

    args = parser.parse_args()
    if args.flat and not args.format:
        args.format = 'json'
    result = geocode(args.geocode, args.kind, args.format,
                     args.ll, args.spn, args.rspn,
                     args.results, args.skip, args.lang)
    if args.flat and args.format == 'json':
        print(pprint(list(get_geo_objects(result))))
    else:
        print(result)
