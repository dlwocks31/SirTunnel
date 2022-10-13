#!/usr/bin/env python3

import json
import sys
import time
from urllib import request

if __name__ == '__main__':

    host = sys.argv[1]
    port = sys.argv[2]
    tunnel_id = host + '-' + port

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        print('Cleaning up any existing tunnels...', end=' ')
        existing_tunnel_request = request.Request(
            method='GET', url='http://localhost:2019/config/')
        with request.urlopen(existing_tunnel_request) as response:
            existing_tunnels = json.loads(response.read().decode('utf-8'))

        existing_ids = map(lambda a: a['@id'],
                           existing_tunnels['apps']['http']['servers']['sirtunnel']['routes'])
        for id in existing_ids:
            if host in id:
                delete_request = request.Request(
                    method='DELETE', url='http://localhost:2019/id/' + id)
                request.urlopen(delete_request)
    except Exception as e:
        print('Error while cleaning tunnel: ' + str(e))
    else:
        print('Done.')

    caddy_add_route_request = {
        "@id": tunnel_id,
        "match": [{
            "host": [host],
        }],
        "handle": [{
            "handler": "reverse_proxy",
            "upstreams": [{
                "dial": ':' + port
            }]
        }]
    }

    body = json.dumps(caddy_add_route_request).encode('utf-8')

    create_url = 'http://127.0.0.1:2019/config/apps/http/servers/sirtunnel/routes'
    req = request.Request(method='POST', url=create_url, headers=headers)
    request.urlopen(req, body)

    print("Tunnel created successfully")

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:

            print("Cleaning up tunnel")
            delete_url = 'http://127.0.0.1:2019/id/' + tunnel_id
            req = request.Request(method='DELETE', url=delete_url)
            request.urlopen(req)
            break
