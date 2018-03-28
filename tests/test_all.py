#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fnmatch
import json
import pytest
import os


def pytest_generate_tests(metafunc):
    """ Parametrizes all test cases in each json in this file directory
    (e.g, tests/**/*.json). Each test case name will be composed by the
    file name and its description.

    """
    if 'tparams' in metafunc.fixturenames:
        test_cases = []
        test_case_id = 0
        for root, dirnames, filenames in os.walk(os.path.dirname(__file__)):
            for json_file in fnmatch.filter(filenames, '*.json'):
                with open(os.path.join(root, json_file)) as f:
                    data = json.load(f)
                    for d in data:
                        if isinstance(d, dict):
                            d['file'] = os.path.basename(json_file)
                            d['id'] = test_case_id
                            test_cases.append(d)
                            test_case_id += 1
        metafunc.parametrize(
            'tparams', [
                pytest.mark.xfail(t) if t.get('xfail') else t
                for t in test_cases
            ],
            ids=[
                '{}_id_{}_{}'.format(
                    t.get('file'), t.get('id'), t.get('description'))
                for t in test_cases
            ])


def test(oft, tparams):
    """Executes each test case based on the parametrized argument.

    :tparams: parametrized args

    """
    ret = oft._test_execute(tparams, tparams.get('description'))
    assert ret == oft.TEST_OK
