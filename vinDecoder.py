#!/usr/local/opt/python/bin/python2.7
"""Decode VINs from the NHTSA API as of 6/16/28."""
import urllib2
import json


class VinDecoder():
    """Super simple module to decode VINs using the NHTSA API."""

    def __init__(self):
        """Initialize the decoder."""
        return None

    def decode(self, vin):
        """Decode the given VIN."""
        url = 'https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/' + vin + '?format=json'
        url = url.strip()
        url = url.replace(" ", "")
        res = urllib2.urlopen(url).read()
        obj = json.loads(res)
        print(json.dumps(obj, indent=4))
        #print obj
        if 'Results' in obj:
            car_json = obj['Results']
            for car_info in car_json:
                if 'Variable' not in car_info:
                    return None
                if car_info['Variable'] == 'Model Year':
                    year = car_info['Value']
                if car_info['Variable'] == 'Make':
                    make = car_info['Value']
                if car_info['Variable'] == 'Trim':
                    trim = car_info['Value']
                if car_info['Variable'] == 'Model':
                    model = car_info['Value']
                if car_info['Variable'] == 'Displacement (L)':
                    disp = car_info['Value']
                if car_info['Variable'] == 'Engine Number of Cylinders':
                    cyl = car_info['Value']
            info = {'vin': vin, 'year': year, 'make': make,
                    'model': model, 'disp': disp, 'cyl': cyl, 'trim': trim}
            return info, vin, year, model, make, cyl, trim


if __name__ == "__main__":
    vd = VinDecoder()
    vin = '1N4AL3AP6FC149535'
    d = vd.decode(vin)
    print d
