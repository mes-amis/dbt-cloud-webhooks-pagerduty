# stdlib
import hashlib
import hmac
import os
import logging
from typing import Dict

# third party
from fastapi import FastAPI, HTTPException, Request
from requests import Session
from mangum import Mangum

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger()

app = FastAPI(title='PagerDuty')

STATUSES = {
    'fail': 'critical',
    'error': 'critical',
    'Errored': 'critical'
}

RESOURCES = ['models', 'tests', 'seeds', 'snapshots']
EVENTS_URL = 'https://events.pagerduty.com/v2/enqueue'


def build_payload(webhook_response: Dict) -> Dict:
    data = webhook_response['data']
    return {
        'routing_key': os.environ['PD_ROUTING_KEY'],
        'event_action': 'trigger',
        'dedup_key': data['runId'],
        'payload': {
            'timestamp': webhook_response['timestamp'],
            'severity': STATUSES[data['runStatus']],
            'source': 'https://cloud.getdbt.com',
            'summary': f'{data["jobName"]} - {data["runStatus"]}'
            'details': data["runStatusMessage"]
        },
    }


def verify_signature(request_body: bytes, auth_header: str):
    app_secret = os.environ['DBT_CLOUD_AUTH_TOKEN'].encode('utf-8')
    signature = hmac.new(app_secret, request_body, hashlib.sha256).hexdigest()
    return signature == auth_header


@app.post('/', status_code=204)
async def pagerduty_webhook(request: Request):
    request_body = await request.body()
    auth_header = request.headers.get('authorization', None)
    if not verify_signature(request_body, auth_header):
        raise HTTPException(status_code=403, detail='Message not authenticated')

    response = await request.json()
    logger.debug("Webhook Parameters:")
    logger.debug(response)
    if (response['data'].get('runStatus', None) == 'Errored') and (response['data'].get('jobName', None) != 'Pull Request Run - SlimCI '):
        session = Session()
        session.headers = {'Content-Type': 'application/json'}
        payload = build_payload(response)
        session.post(EVENTS_URL, json=payload)

    return

handler = Mangum(app)

if __name__ == '__main__':
    app.run()
