import unittest
from geocode import geocode, get_geo_objects, get_most_precise


class TestGeocoder(unittest.TestCase):

    def test_most_precise_ensure_locality(self):
        res = get_most_precise(get_geo_objects(
            geocode('Житомир, Киевская, 75', format='json'),
            ensure_locality='Житомир'))
        self.assertEquals(res.get('kind'), 'house')
        self.assertEquals(res.get('precision'), 'exact')
        self.assertEquals(res.get('LocalityName'), 'Житомир')
