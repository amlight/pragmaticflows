#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os


def drill_update(element, key=None, current_value=None, refactored_value=None):
    """Drill and refactor an element given its key, current_value and
    refactored_value.

    :element: structured data, either a list or dict
    :key: key to be updated
    :current_value: dictionary value of the key you're looking for
    :current_value: dictionary refactored value of the key you're looking for
    :returns: structured data refactored

    """
    if isinstance(element, list):
        for el in element:
            drill_update(el, key, current_value, refactored_value)
    elif isinstance(element, dict):
        for k, v in element.items():
            if k == key and v == current_value:
                element[key].update(refactored_value)
            drill_update(v, key, current_value, refactored_value)
    return element


def get_json_files(root_path):
    """Get list of json files given a root path

    :root_path:
    :returns: list of json file paths

    """
    json_files = []
    for root, dirs, files in os.walk(root_path):
        for f in files:
            if '.json' in f:
                json_files.append("{}".format(
                    os.path.join(os.path.abspath(root), f)))
    return json_files


def main():
    """Main function

    """
    directory = "tests"
    refactor_list = [{
        'key': 'OFPActionOutput',
        'current_value': {
            "port": 2
        },
        'refactored_value': {
            "port": "target_send_port_1"
        }
    }, {
        'key': 'OFPActionOutput',
        'current_value': {
            "port": 3
        },
        'refactored_value': {
            "port": "target_send_port_2"
        }
    }, {
        'key': 'OXMTlv',
        'current_value': {
            "field": "in_port",
            "value": 1
        },
        'refactored_value': {
            "value": "target_recv_port"
        }
    }, {
        'key': 'OXMTlv',
        'current_value': {
            "field": "in_port",
            "value": 2
        },
        'refactored_value': {
            "value": "target_send_port_1"
        }
    }, {
        'key': 'OXMTlv',
        'current_value': {
            "field": "in_port",
            "value": 3
        },
        'refactored_value': {
            "value": "target_send_port_2"
        }
    }]
    json_files = get_json_files(directory)
    for json_file in json_files:
        refactored_data = None
        with open(json_file) as json_fd:
            json_data = json.load(json_fd)
            for d in refactor_list:
                refactored_data = drill_update(json_data, **d)
        # overwrite
        if refactored_data:
            with open(json_file, "w") as json_fd:
                json.dump(refactored_data, json_fd, indent=4)


if __name__ == "__main__":
    main()
