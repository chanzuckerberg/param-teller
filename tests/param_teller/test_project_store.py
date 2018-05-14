from moto import mock_ssm
from param_teller.project_store import ProjectParameterStore, ProjectSecretsManager
from mock import patch, MagicMock
import boto3
import pytest


@mock_ssm
class TestProjectParameterStore(object):

    @pytest.fixture(autouse=True)
    def ssm_store(self):
        client = boto3.client('ssm')
        client.put_parameter(Name='proj1-prod-service1.key1', Value='value1_prod_1_1_no_path', Type='SecureString')
        client.put_parameter(Name='.proj1-prod-service1.key1', Value='value1_prod_1_1_no_path_with_lead', Type='SecureString')
        client.put_parameter(Name='/proj1-prod-service1/key1', Value='value1_prod_1_1', Type='SecureString')
        client.put_parameter(Name='/proj1-prod-service1/key2', Value='value1_prod_1_2', Type='SecureString')
        client.put_parameter(Name='/proj1-test-service1/key3', Value='value1_test_1_3', Type='SecureString')
        client.put_parameter(Name='/proj1-prod-service2/key1', Value='value1_prod_2_1', Type='SecureString')
        client.put_parameter(Name='/proj2-prod-service1/key1', Value='value2_prod_1_1', Type='SecureString')

    def test_get_service_parameters(self):
        values = ProjectParameterStore(project='proj1', env='prod', service='service1').get_service_parameters()

        assert len(values) is 2
        assert_key_value(values, '/proj1-prod-service1/key1', 'value1_prod_1_1')

    def test_get_service_parameters_by_prefix(self):
        values = ProjectParameterStore(project='proj1', env='prod', service='service1', key_separator=".").get_service_parameters()

        assert len(values) is 1
        assert_key_value(values, 'proj1-prod-service1.key1', 'value1_prod_1_1_no_path')

    def test_get_service_parameter(self):
        value = ProjectParameterStore(project='proj1', env='prod', service='service1').get_service_parameter('key2')

        assert value == 'value1_prod_1_2'

    def test_get_service_parameter_by_prefix(self):
        value = ProjectParameterStore(project='proj1', env='prod', service='service1', key_separator=".").get_service_parameter('key1')

        assert value == 'value1_prod_1_1_no_path'


def mock_secrets_manager():
    mock_sm = MagicMock()
    secrets = {
        'proj1-prod-service1/key1': 'value1_prod_1_1',
        'proj1-prod-service1/key2': 'value1_prod_1_2',
        'proj1-test-service1/key3': 'value1_test_1_3',
        'proj1-prod-service2/key1': 'value1_prod_2_1',
        'proj2-prod-service1/key1': 'value2_prod_1_1'
    }
    mock_sm.return_value.get_secret_value.side_effect = lambda **args: {
        'SecretString': secrets.get(args.get('SecretId'))
    }
    mock_sm.return_value.list_secrets.side_effect = lambda **args: {
        'SecretList': [{'Name': key} for key in secrets.keys()]}
    return mock_sm


@patch('param_teller.secrets_manager.client', new_callable=mock_secrets_manager)
class TestProjectSecretsManager(object):

    def test_get_service_parameters(self, store):
        values = ProjectSecretsManager(project='proj1', env='prod', service='service1').get_service_parameters()

        assert len(values) is 2
        assert_key_value(values, 'proj1-prod-service1/key1', 'value1_prod_1_1')
        assert_key_value(values, 'proj1-prod-service1/key2', 'value1_prod_1_2')

    def test_get_service_parameter(self, store):
        value = ProjectSecretsManager(project='proj1', env='prod', service='service1').get_service_parameter('key2')

        assert value == 'value1_prod_1_2'


def assert_key_value(dictionary, key, value):
    assert key in dictionary
    assert dictionary.get(key) == value
