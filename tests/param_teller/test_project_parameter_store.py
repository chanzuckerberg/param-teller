from moto import mock_ssm
from param_teller.project_parameter_store import ProjectParameterStore
import boto3


@mock_ssm
def initialize_store():
    client = boto3.client('ssm')
    client.put_parameter(Name='proj1-prod-service1_key1', Value='value1_prod_1_1_no_path', Type='SecureString')
    client.put_parameter(Name='proj1-prod-service1/key1', Value='value1_prod_1_1', Type='SecureString')
    client.put_parameter(Name='proj1-prod-service1/key2', Value='value1_prod_1_2', Type='SecureString')
    client.put_parameter(Name='proj1-test-service1/key3', Value='value1_test_1_3', Type='SecureString')
    client.put_parameter(Name='proj1-prod-service2/key1', Value='value1_prod_2_1', Type='SecureString')
    client.put_parameter(Name='proj2-prod-service1/key1', Value='value2_prod_1_1', Type='SecureString')


@mock_ssm
def test_get_service_parameters():
    initialize_store()

    values = ProjectParameterStore(project='proj1', env='prod', service='service1').get_service_parameters()

    assert len(values) is 2
    _assert_key_value(values, 'proj1-prod-service1/key1', 'value1_prod_1_1')
    _assert_key_value(values, 'proj1-prod-service1/key2', 'value1_prod_1_2')


@mock_ssm
def test_get_service_parameters_with_prefix():
    initialize_store()
    values = ProjectParameterStore(project='proj1', env='prod', service='service1').get_service_parameters()

    assert len(values) is 2
    _assert_key_value(values, 'proj1-prod-service1/key1', 'value1_prod_1_1')
    _assert_key_value(values, 'proj1-prod-service1/key2', 'value1_prod_1_2')


@mock_ssm
def test_get_service_parameter():
    initialize_store()
    value = ProjectParameterStore(project='proj1', env='prod', service='service1').get_service_parameter('key2')

    assert value == 'value1_prod_1_2'


@mock_ssm
def test_get_service_parameter_with_prefix():
    initialize_store()

    value = ProjectParameterStore(project='proj1', env='prod', service='service1').get_service_parameter('key2')

    assert value == 'value1_prod_1_2'


def _assert_key_value(dictionary, key, value):
    assert key in dictionary
    assert dictionary.get(key) == value
