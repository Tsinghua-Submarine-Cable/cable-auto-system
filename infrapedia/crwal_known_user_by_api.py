import csv
import json
import re
import os
import requests
import time
from utils import *

def get_user_by_api():
    path = './data_' + formatted_date
    ids = set()
    if os.path.exists(os.path.join(path, 'cable_info.json')):
        f = open(os.path.join(path, 'cable_info.json'), 'r', encoding='utf-8')
        for line in f.readlines():
            for known_user in json.loads(line)['knownUsers']:
                ids.add(known_user['_id'].rstrip('\n'))

    url = "https://www.infrapedia.com/api/organization/view/"

    f = open(os.path.join(path, 'known_users_info.json'), 'w', encoding='utf-8')

    for id in ids:
        try:
            response = requests.get(url + id)
            if response.status_code == 200:
                if len(response.json()['data']['r']) == 0:
                    continue
                print(response.json())
                f.write(json.dumps(response.json()['data']['r'][0]) + '\n')
            else:
                print("请求失败，状态码为：", response.status_code, "id: ", id)
        except Exception as e:
            continue
    f.close()

    table_header = ["Name", "PeeringDB", "ASN", "Address", "More Information:",
                         "Facilities (Ownership)", "Subsea Cables (Ownership)", "Subsea Cables (User)",
                         "Terrestrial Networks (Ownership)", "Cls (Ownership)"]

    f = open(os.path.join(path, 'known_users_info.json'), 'r', encoding='utf-8')
    for line in f.readlines():
        obj = json.loads(line)
        _id = obj['_id']
        name = obj['name']
        peering_db = ''
        if 'ooid' in obj:
            peering_db = obj['ooid']
        asn = ''
        if 'asn' in obj:
            asn = json.dumps(obj['asn'])
        address = []
        for t in obj['address']:
            if 'fullAddress' in t:
                address.append(t['fullAddress'])
        address = json.dumps(address)
        more_info = ''
        if 'url' in obj:
            more_info = obj['url']
        facilities = []
        for t in obj['facilities']:
            facilities.append(t['name'])
        facilities = json.dumps(facilities)
        subsea_cables = []
        for t in obj['subsecables']:
            subsea_cables.append(t['name'])
        subsea_cables = json.dumps(subsea_cables)
        subsea_cables_user = []
        for t in obj['knownUsersSubseaCable']:
            subsea_cables_user.append(t['name'])
        subsea_cables_user = json.dumps(subsea_cables_user)
        terrestrial_networks = []
        for t in obj['terrestrialnetworks']:
            terrestrial_networks.append(t['name'])
        terrestrial_networks = json.dumps(terrestrial_networks)
        cls = []
        for t in obj['cls']:
            cls.append(t['name'])
        cls = json.dumps(cls)

        row = [name, peering_db, asn, address, more_info, facilities, subsea_cables, subsea_cables_user,
               terrestrial_networks, cls]

        dump_file(row, os.path.join(path, 'known_users_info.csv'))


if __name__ == '__main__':
    get_user_by_api()
