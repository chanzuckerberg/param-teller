from param_teller.secrets_manager import SecretsManager
from mock import patch, MagicMock


# TODO: Replace by moto mock for SecretsManager when available
def mock_secrets_manager():
    mock_sm = MagicMock()
    secrets = {
        'service1/key1': 'value1_1',
        'service1/key2': 'value1_2',
        'service2/key1': 'value2_1',
        'service1_key1': 'value1_1'
    }
    mock_sm.return_value.get_secret_value.side_effect = lambda **args: {
        'SecretString': secrets.get(args.get('SecretId'))
    }
    mock_sm.return_value.list_secrets.side_effect = lambda **args: {
        'SecretList': [{'Name': key} for key in secrets.keys()]}
    return mock_sm


@patch('param_teller.secrets_manager.client', new_callable=mock_secrets_manager)
def test_get_values(client):
    values = SecretsManager().get_values('service1/key1', 'service2/key1')

    assert len(values) is 2
    _assert_key_value(values, 'service1/key1', 'value1_1')
    _assert_key_value(values, 'service2/key1', 'value2_1')


@patch('param_teller.secrets_manager.client', new_callable=mock_secrets_manager)
def test_get_value(client):
    value = SecretsManager().get_value('service1/key2')

    assert value == 'value1_2'


@patch('param_teller.secrets_manager.client', new_callable=mock_secrets_manager)
def test_get_values_with_empty_key_list(client):
    values = SecretsManager().get_values()
    assert len(values) is 0


@patch('param_teller.secrets_manager.client', new_callable=mock_secrets_manager)
def test_get_values_by_prefix(client):
    values = SecretsManager().get_values_by_prefix('service1')

    assert len(values) is 3
    _assert_key_value(values, 'service1_key1', 'value1_1')
    _assert_key_value(values, 'service1/key1', 'value1_1')
    _assert_key_value(values, 'service1/key2', 'value1_2')


def _assert_key_value(dictionary, key, value):
    assert key in dictionary
    assert dictionary.get(key) == value
