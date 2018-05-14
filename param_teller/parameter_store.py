import botocore
from boto3 import client


class ParameterStore(object):
    """
    Retrieves parameters from AWS Parameter Store.
    """

    def __init__(self, ssm_client=None, with_decryption=True):
        # type: (botocore.client.SSM, bool) -> None
        """
        Initialize new parameter store client.

        :param ssm_client: Optional client provided by user. By default, it creates a new client using the default
            session.
        :param with_decryption: If true, parameter store will decrypt values.
        """
        self._ssm_client = ssm_client or client('ssm')
        self._with_decryption = with_decryption

    def get_value(self, key):
        # type: (str) -> str
        """
        Retrieve single parameter from store.

        :param key:
        :return:
        """
        response = self._ssm_client.get_parameter(
            Name=key,
            WithDecryption=self._with_decryption
        )
        return response.get('Parameter', {}).get('Value')

    def get_values_by_path(self, path):
        # type: (str) -> dict
        """
        Retrieve all parameter values in a user provider path.

        :param path: Path where the parameters are store.
        :return: Dictionary of parameter values indexed by parameter key.
        """

        # In AWS, a leading path is not required, i.e. "/param" and "param" match the same key and are not unique
        # However, boto3 and moto (corresponding mocking library) require a leading path:
        # http://boto3.readthedocs.io/en/latest/reference/services/ssm.html#SSM.Client.get_parameters_by_path
        # Therefore we are enforcing the leading '/'
        path = path.strip()
        if path and not path.startswith("/"):
            path = "/{path}".format(path=path)

        values = {}
        extra_args = {}
        while True:
            response = self._ssm_client.get_parameters_by_path(
                Path=path,
                WithDecryption=self._with_decryption,
                **extra_args
            )
            values.update({param['Name']: param['Value'] for param in response['Parameters']})

            next_token = response.get('NextToken')
            if not next_token:
                break

            extra_args['NextToken'] = next_token

        return values

    def get_values(self, *keys):
        # type: (str) -> dict
        """
        Retrieve parameter values by key names.

        :param keys: keys to retrieve.
        :return: Dictionary of parameter values indexed by parameter key (includes only found keys).
        """

        if not keys:
            return {}

        values = {}
        extra_args = {}
        while True:
            response = self._ssm_client.get_parameters(
                Names=keys,
                WithDecryption=self._with_decryption,
                **extra_args
            )
            values.update({param['Name']: param['Value'] for param in response['Parameters']})

            next_token = response.get('NextToken')
            if not next_token:
                break

            extra_args['NextToken'] = next_token

        return values

    def get_values_by_prefix(self, prefix=''):
        # type: (str) -> dict
        """
        Retrieve all parameter values for keys that start with given prefix.

        :param prefix: Key name prefix.
        :return: Dictionary of parameter values indexed by parameter key.
        """
        keys = []

        filters = [{'Key': 'Name', 'Values': ['{prefix}'.format(prefix=prefix)]}] if prefix else []
        extra_args = {}
        while True:
            response = self._ssm_client.describe_parameters(
                Filters=filters,
                **extra_args
            )
            keys += [param.get('Name') for param in response.get('Parameters', [])]

            next_token = response.get('NextToken')
            if not next_token:
                break

            extra_args['NextToken'] = next_token

        values = {}
        if keys:
            values = self.get_values(*keys)

        return values
