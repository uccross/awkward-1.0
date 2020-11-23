# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/master/LICENSE

from __future__ import absolute_import

import sys
import os
import json

import pytest
import numpy

import awkward1

def test_tostring():
    # write a json string from an array built from
    # multiple json fragments from a string
    str = """{"x": 1.1, "y": []}
             {"x": 2.2, "y": [1]}
             {"x": 3.3, "y": [1, 2]}
             {"x": 4.4, "y": [1, 2, 3]}
             {"x": 5.5, "y": [1, 2, 3, 4]}
             {"x": 6.6, "y": [1, 2, 3, 4, 5]}"""

    array = awkward1.from_json(str)
    assert awkward1.to_list(array) == [
        [{'x': 1.1, 'y': []}],
        [{'x': 2.2, 'y': [1]}],
        [{'x': 3.3, 'y': [1, 2]}],
        [{'x': 4.4, 'y': [1, 2, 3]}],
        [{'x': 5.5, 'y': [1, 2, 3, 4]}],
        [{'x': 6.6, 'y': [1, 2, 3, 4, 5]}]]

    assert awkward1.to_json(array) == '[[{"x":1.1,"y":[]}],[{"x":2.2,"y":[1]}],[{"x":3.3,"y":[1,2]}],[{"x":4.4,"y":[1,2,3]}],[{"x":5.5,"y":[1,2,3,4]}],[{"x":6.6,"y":[1,2,3,4,5]}]]'

def test_fromstring():
    # read multiple json fragments from a string
    str = """{"x": 1.1, "y": []}
             {"x": 2.2, "y": [1]}
             {"x": 3.3, "y": [1, 2]}
             {"x": 4.4, "y": [1, 2, 3]}
             {"x": 5.5, "y": [1, 2, 3, 4]}
             {"x": 6.6, "y": [1, 2, 3, 4, 5]}"""

    array = awkward1.from_json(str)
    assert awkward1.to_list(array) == [
        [{'x': 1.1, 'y': []}],
        [{'x': 2.2, 'y': [1]}],
        [{'x': 3.3, 'y': [1, 2]}],
        [{'x': 4.4, 'y': [1, 2, 3]}],
        [{'x': 5.5, 'y': [1, 2, 3, 4]}],
        [{'x': 6.6, 'y': [1, 2, 3, 4, 5]}]]

def test_array_tojson():
    # convert float 'nan' and 'inf' to user-defined strings
    array = awkward1.layout.NumpyArray(numpy.array([
        [float('nan'), float('nan'), 1.1],
        [float('inf'), 3.3, float('-inf')]]))

    assert awkward1.to_json(array, nan_string='NaN', infinity_string='inf',
        minus_infinity_string='-inf') == '[["NaN","NaN",1.1],["inf",3.3,"-inf"]]'

    array2 = awkward1.Array([[0, 2], None, None, None, None, None])
    assert awkward1.to_json(array2, nan_string='NaN') == '[[0,2],"NaN","NaN","NaN","NaN","NaN"]'

def test_fromfile():
    # read multiple json fragments from a json file
    array = awkward1.from_json('tests/samples/test-record-array.json')
    assert awkward1.to_list(array) == [
        [{'x': 1.1, 'y': []}],
        [{'x': 2.2, 'y': [1]}],
        [{'x': 3.3, 'y': [1, 2]}],
        [{'x': 4.4, 'y': [1, 2, 3]}],
        [{'x': 5.5, 'y': [1, 2, 3, 4]}],
        [{'x': 6.6, 'y': [1, 2, 3, 4, 5]}]]

    # read json file containg 'nan' and 'inf' user-defined strings
    # and replace 'nan' and 'inf' strings with floats
    array = awkward1.from_json('tests/samples/test.json', nan_and_inf_as_float=True,
        infinity_string='inf', minus_infinity_string='-inf')

    assert awkward1.to_list(array[0:5]) == [1.1, 2.2, 3.3, float('inf'), float('-inf')]

    # read json file containg 'nan' and 'inf' user-defined strings
    array = awkward1.from_json('tests/samples/test.json')

    assert awkward1.to_list(array) == [1.1, 2.2, 3.3, 'inf', '-inf',
        [4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.1, 11.11],
        [12.12, 13.13, 14.14, 15.15, 16.16, 17.17],
        [[[18.18,   19.19,   20.2,    21.21,   22.22],
          [23.23,   24.24,   25.25,   26.26,   27.27,
           28.28,   29.29,   30.3,    31.31,   32.32,
           33.33,   34.34,   35.35,   36.36,   37.37],
          [38.38],
          [39.39, 40.4, 'NaN', 'NaN', 41.41, 42.42, 43.43]],
         [[44.44,   45.45,   46.46,   47.47,   48.48],
          [49.49,   50.5,    51.51,   52.52,   53.53,
           54.54,   55.55,   56.56,   57.57,   58.58,
           59.59,   60.6,    61.61,   62.62,   63.63],
          [64.64],
          [65.65, 66.66, 'NaN', 'NaN', 67.67, 68.68, 69.69]]]]

    # read json file containg 'nan' and 'inf' user-defined strings
    # and replace 'nan' and 'inf' strings with a predefined 'None' string
    array = awkward1.from_json('tests/samples/test.json',
        infinity_string='inf', minus_infinity_string='-inf', nan_string='NaN')

    assert awkward1.to_list(array) == [1.1, 2.2, 3.3, 'None', 'None',
        [4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.1, 11.11],
        [12.12, 13.13, 14.14, 15.15, 16.16, 17.17],
        [[[18.18,   19.19,   20.2,    21.21,   22.22],
          [23.23,   24.24,   25.25,   26.26,   27.27,
           28.28,   29.29,   30.3,    31.31,   32.32,
           33.33,   34.34,   35.35,   36.36,   37.37],
          [38.38],
          [39.39, 40.4, 'None', 'None', 41.41, 42.42, 43.43]],
         [[44.44,   45.45,   46.46,   47.47,   48.48],
          [49.49,   50.5,    51.51,   52.52,   53.53,
           54.54,   55.55,   56.56,   57.57,   58.58,
           59.59,   60.6,    61.61,   62.62,   63.63],
          [64.64],
          [65.65, 66.66, 'None', 'None', 67.67, 68.68, 69.69]]]]

    # read json file containg multiple definitions of 'nan' and 'inf'
    # user-defined strings
    # replace can only work for one string definition
    array = awkward1.from_json('tests/samples/test-nan-inf.json', nan_and_inf_as_float=True,
        infinity_string='Infinity', nan_string='None')

    assert awkward1.to_list(array) == [1.1, 2.2, 3.3, 'inf', '-inf',
        [4.4, float('inf'), 6.6, 7.7, 8.8, 'NaN', 10.1, 11.11],
        [12.12, 13.13, 14.14, 15.15, 16.16, 17.17],
        [[[18.18,   19.19,   20.2,    21.21,   22.22],
          [23.23,   24.24,   25.25,   26.26,   27.27,
           28.28,   29.29,   30.3,    31.31,   32.32,
           33.33,   34.34,   35.35,   36.36,   37.37],
          [38.38],
          [39.39, 40.4, 'NaN', 'NaN', 41.41, 42.42, 43.43]],
         [[44.44,   45.45,   46.46,   47.47,   48.48],
          [49.49,   50.5,    51.51,   52.52,   53.53,
           54.54,   55.55,   56.56,   57.57,   58.58,
           59.59,   60.6,    61.61,   62.62,   63.63],
          [64.64],
          [65.65, 66.66, 'NaN', 'NaN', 67.67, 68.68, 69.69]]]]
