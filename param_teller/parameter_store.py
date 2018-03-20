from boto3 import client


class ParameterStore(object):
    """
    Retrieves parameters from AWS Parameter Store.
    """

    def __init__(self, ssm_client=None, with_decryption=True):
        # type: (botocore.client.SSM, bool) -> None
        """
        Initialize new parameter store client.

        :param ssm_client: Optional client provided by user. By default, it create a new client using the default
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
        values = {}
        while True:
            response = self._ssm_client.get_parameters_by_path(
                Path=path,
                WithDecryption=self._with_decryption
            )
            values.update({param['Name']: param['Value'] for param in response['Parameters']})

            if not response.get('NextToken'):
                break

        return values

    def get_values(self, *keys):
        # type: (str) -> dict
        """
        Retrieve parameter values by key names.

        :param keys: list of keys to retrieve.
        :return: Dictionary of parameter values indexed by parameter key (includes only found keys).
        """

        if not keys:
            return {}

        values = {}
        while True:
            response = self._ssm_client.get_parameters(
                Names=keys,
                WithDecryption=self._with_decryption
            )
            values.update({param['Name']: param['Value'] for param in response['Parameters']})

            if not response.get('NextToken'):
                break

        return values

    def get_values_by_prefix(self, prefix=''):
        # type: (str) -> dict
        """
        Retrieve all parameter values for keys that start with given prefix.

        :param prefix: Key name prefix.
        :return: Dictionary of parameter values indexed by parameter key.
        """
        keys = []

        while True:
            filters = [{'Key': 'Name', 'Values': ['{prefix}'.format(prefix=prefix)]}] if prefix else []
            response = self._ssm_client.describe_parameters(Filters=filters)
            keys += [param.get('Name') for param in response.get('Parameters', [])]

            if not response.get('NextToken'):
                break

        values = {}
        if keys:
            values = self.get_values(*keys)

        return values
