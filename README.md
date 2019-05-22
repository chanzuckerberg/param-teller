# DEPRECATED Param-Teller: Retrieve parameters from AWS Parameter Store.

[![Build Status](https://travis-ci.com/chanzuckerberg/param-teller.svg?token=qxcH9zWp4qxw9qDaKK3b&branch=master)](https://travis-ci.com/chanzuckerberg/param-teller)

Helper library to load values form AWS Parameter Store and decrypt values using a KMS key.

# Usage

## Direct from AWS Backend

### Parameter Store

```python
from param_teller import ParameterStore

parameter_store = ParameterStore(with_decryption=True)

parameter_store.get_value(key='/base/super-secret1')
# 'super-secret-value1'

parameter_store.get_values_by_path(path='/base')
# {'/base/super-secret1': 'super-secret-value1', '/base/super-secret2': 'super-secret-value2'}
```

### Secrets Manager

```python
from param_teller import SecretsManager

secrets_manager = SecretsManager()

secrets_manager.get_value(key='/base/super-secret1')
# {'secret': 'super-secret-value1'}

secrets_manager.get_values_by_prefix(path='base')
# {'/projx-prod-servicey/super-secret1': {'secret': 'super-secret-value1'}, '/projx-prod-servicey/super-secret2': {'secret': 'super-secret-value2'}}
```

## Project module following CZI's Service Name Convention

### Parameter Store

```python
from param_teller import ProjectParameterStore

parameter_store = ProjectParameterStore(
    project='projx',
    services='servicey',
    env='prod',
    with_decryption=True)

parameter_store = parameter_store.get_service_parameter(key='super-secret1')
# 'super-secret-value1'

parameter_store = parameter_store.get_service_parameters()
# {'/projx-prod-servicey/super-secret1': 'super-secret-value1', '/projx-prod-servicey/super-secret2': 'super-secret-value2'}
```

### Secrets Manager

```python
from param_teller import ProjectSecretsManager

secrets_manager = ProjectSecretsManager(
    project='projx',
    services='servicey',
    env='prod')

secrets_manager.get_service_parameter(key='super-secret1')
# {'secret': 'super-secret-value1'}

secrets_manager.get_service_parameters()
# {'/projx-prod-servicey/super-secret1': {'secret': 'super-secret-value1'}, '/projx-prod-servicey/super-secret2': {'secret': 'super-secret-value2'}}
```

