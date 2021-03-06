from param_teller.parameter_store import ParameterStore
from moto import mock_ssm
import boto3
from pytest import raises
from botocore.exceptions import ParamValidationError


# In AWS, a leading path is not required, i.e. "/param" and "param" match the same key and are not unique
# see: https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-su-create.html
# However, moto does not support this. Thus we only testing with leading '/'


# TODO: moto does not support pagination for get_parameters_by_path (similar test below by prefix). Maybe use stubber.
@mock_ssm
def test_get_values_by_path():
    client = boto3.client('ssm')
    client.put_parameter(Name='/service1/key1', Value='value1_1', Type='SecureString')
    client.put_parameter(Name='/service1/key2', Value='value1_2', Type='SecureString')
    client.put_parameter(Name='/service2/key1', Value='value2_1', Type='SecureString')

    values = ParameterStore().get_values_by_path('service1')

    assert len(values) is 2
    _assert_key_value(values, '/service1/key1', 'value1_1')
    _assert_key_value(values, '/service1/key2', 'value1_2')


@mock_ssm
def test_get_values_by_path_with_empty_path():
    with raises(ParamValidationError, message='Invalid length for parameter Path'):
        ParameterStore().get_values_by_path(' ')


@mock_ssm
def test_get_values():
    client = boto3.client('ssm')
    client.put_parameter(Name='/service1/key1', Value='value1_1', Type='SecureString')
    client.put_parameter(Name='/service1/key2', Value='value1_2', Type='SecureString')
    client.put_parameter(Name='/service2/key1', Value='value2_1', Type='SecureString')

    values = ParameterStore().get_values('/service1/key1', '/service2/key1')

    assert len(values) is 2
    _assert_key_value(values, '/service1/key1', 'value1_1')
    _assert_key_value(values, '/service2/key1', 'value2_1')


@mock_ssm
def test_get_value():
    client = boto3.client('ssm')
    client.put_parameter(Name='/service1/key1', Value='value1_1', Type='SecureString')
    client.put_parameter(Name='/service1/key2', Value='value1_2', Type='SecureString')
    client.put_parameter(Name='/service2/key1', Value='value2_1', Type='SecureString')

    value = ParameterStore().get_value('/service1/key2')

    assert value == 'value1_2'


@mock_ssm
def test_get_values_with_empty_key_list():
    values = ParameterStore().get_values()
    assert len(values) is 0


@mock_ssm
def test_get_values_by_prefix():
    client = boto3.client('ssm')
    client.put_parameter(Name='service1_key1', Value='value1_1', Type='SecureString')
    client.put_parameter(Name='/service1/key2', Value='value1_2', Type='SecureString')
    client.put_parameter(Name='/service2/key1', Value='value2_1', Type='SecureString')

    values = ParameterStore().get_values_by_prefix('service1')

    assert len(values) is 1
    _assert_key_value(values, 'service1_key1', 'value1_1')


@mock_ssm
def test_get_values_by_prefix_with_pagination():
    client = boto3.client('ssm')
    for i in range(1, 13):
        client.put_parameter(Name='service1_key{0}'.format(i), Value='value1_{0}'.format(i), Type='SecureString')

    values = ParameterStore().get_values_by_prefix('service1')

    assert len(values) is 12
    for i in range(1, 12):
        _assert_key_value(values, 'service1_key{0}'.format(i), 'value1_{0}'.format(i))


def _assert_key_value(dictionary, key, value):
    assert key in dictionary
    assert dictionary.get(key) == value
