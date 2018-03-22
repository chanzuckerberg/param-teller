# Param-Teller: Retrieve parameters from AWS Parameter Store.

[![Build Status](https://travis-ci.com/chanzuckerberg/param-teller.svg?token=qxcH9zWp4qxw9qDaKK3b&branch=master)](https://travis-ci.com/chanzuckerberg/param-teller)

Helper library to load values form AWS Parameter Store and decrypt values using a KMS key.

# Usage

```python
from param_teller import ParameterStore

parameter_store = ParameterStore(with_decryption=True)

parameter_store = parameter_store.get_value(key='/base/super-secret1')
# {'/base/super-secret1': 'super-secret-value1'}

parameter_store = parameter_store.get_values_by_path(path='/base')
# {'/base/super-secret1': 'super-secret-value1', '/base/super-secret2': 'super-secret-value2'}
```

## Projects following CZI's Service Name Convention

```python
from param_teller import ProjectParameterStore

parameter_store = ProjectParameterStore(
    project='projx', 
    services='servicey', 
    env='prod', 
    with_decryption=True)

parameter_store = parameter_store.get_value(key='super-secret1')
# {'/projx-prod-servicey/super-secret1': 'super-secret-value1'}

parameter_store = parameter_store.get_service_parameters()
# {'/projx-prod-servicey/super-secret1': 'super-secret-value1', '/projx-prod-servicey/super-secret2': 'super-secret-value2'}
```


