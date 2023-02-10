import requests
import pytest


def apiPost(url, data):
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code

def apiGet(url, params = None):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code

@pytest.fixture
def supply_webhook_endpoint():
    webhook_endpoint = 'http://127.0.0.1:8000/api/webhook'
    return webhook_endpoint

@pytest.fixture
def supply_sensors_endpoint():
    sensors_endpoint = 'http://127.0.0.1:8000/api/sensors'
    return sensors_endpoint

def test_webhook(supply_webhook_endpoint):
    peopleCounters = [
        {"sensor":"a1","ts":"2021-05-01T10:00:00Z","in_count":10,"out_count":0},
        {"sensor":"b1","ts":"2021-05-01T10:00:00Z","in_count":7,"out_count":0},
        {"sensor":"a1","ts":"2021-05-01T10:25:00Z","in_count":7,"out_count":4},
        {"sensor":"b1","ts":"2021-05-01T11:00:00Z","in_count":6,"out_count":3},
        {"sensor":"b1","ts":"2021-05-01T12:30:00Z","in_count":3,"out_count":4},
        {"sensor":"b1","ts":"2021-05-01T12:30:00Z","in_count":0,"out_count":9},
        {"sensor":"a1","ts":"2021-05-01T13:00:00Z","in_count":0,"out_count":13}
    ]
    for peopleCounter in peopleCounters:
        assert apiPost(supply_webhook_endpoint, peopleCounter)['status'] == 200

def test_webhook_invalid_request(supply_webhook_endpoint):
    peopleCounter = {}
    assert apiPost(supply_webhook_endpoint, peopleCounter) == 422

def test_webhook_invalid_request2(supply_webhook_endpoint):
    peopleCounter = {"sensor":"a1"}
    assert apiPost(supply_webhook_endpoint, peopleCounter) == 422

def test_get_sensors(supply_sensors_endpoint):
    assert set(apiGet(supply_sensors_endpoint)['sensors']) == set(['a1', 'b1'])

def test_get_sensor_by_id(supply_sensors_endpoint):
    for sensor in apiGet(supply_sensors_endpoint)['sensors']:
        assert apiGet(supply_sensors_endpoint + f'/{sensor}/occupancy') == {"sensor": f'{sensor}', "inside": 0}

def test_get_sensor_by_id_invalid_sensor(supply_sensors_endpoint):
    assert apiGet(supply_sensors_endpoint + '/c1/occupancy') == 404

def test_get_sensor_atinstant(supply_sensors_endpoint):
    getParams = {
        "atInstant": '2021-05-01T12:00:10Z'
    }
    assert apiGet(supply_sensors_endpoint + f'/b1/occupancy', getParams) == {"sensor": 'b1', "inside": 10}

def test_get_sensor_atinstant_invalid_timestamp_format(supply_sensors_endpoint):
    getParams = {
        "atInstant": '05-01-2021T12:00:00Z'
    }
    assert apiGet(supply_sensors_endpoint + f'/b1/occupancy', getParams) == 422