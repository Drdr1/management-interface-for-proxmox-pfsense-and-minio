import requests

PFSENSE_HOST = 'http://192.168.1.3'
PFSENSE_API_KEY = '7f39f92fb3ddfb4853b4acae70f92e1e'

# Example endpoints, adjust for your pfSense API

def pfsense_list_firewall():
    resp = requests.get(f'{PFSENSE_HOST}/api/firewall/rules', headers={'Authorization': f'Bearer {PFSENSE_API_KEY}'}, verify=False)
    return resp.json()

def pfsense_create_firewall(params):
    resp = requests.post(f'{PFSENSE_HOST}/api/firewall/rules', json=params, headers={'Authorization': f'Bearer {PFSENSE_API_KEY}'}, verify=False)
    return resp.json()
