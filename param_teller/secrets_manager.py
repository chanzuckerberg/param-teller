import botocore
from boto3 import client


class SecretsManager(object):
    """
    Retrieves secrets from AWS Secrets Manager
    """

    def __init__(self, sm_client=None):
        # type: (botocore.client.SecretsManager) -> None
        """
        Initialize new Secrets Manager client.

        :param sm_client: Optional client provided by user. By default, it creates a new client using the default
            session.
        """
        self._sm_client = sm_client or client('secretsmanager')

    def _list_secret_keys(self):
        # type: () -> list
        """
        List all secrets available.
        :return: list of all the secrets available to the executor of this function.
        """
        keys = []
        extra_args = {}
        while True:
            response = self._sm_client.list_secrets(**extra_args)
            keys += [secret.get('Name') for secret in response.get('SecretList', []) if secret.get('Name') is not None]

            next_token = response.get('NextToken')
            if not next_token:
                break

            extra_args['NextToken'] = next_token

        return keys

    def get_value(self, key):
        # type: (str) -> str
        """
        Retrieve single secret from store.

        :param key: the name of the secret.
        :return: the value of the secret.
        """
        response = self._sm_client.get_secret_value(
            SecretId=key
        )
        return response.get('SecretString')

    def get_values(self, *keys):
        # type: (str) -> dict
        """
        Retrieve secrets by key names.

        :param keys: keys to retrieve.
        :return: Dictionary of secret values indexed by parameter key (includes only found keys).
        """

        if not keys:
            return {}

        return {key: value for key, value in ((key, self.get_value(key)) for key in keys) if
                value is not None}

    def get_values_by_prefix(self, prefix=''):
        # type: (str) -> dict
        """
        Retrieve all secret values for keys that start with given prefix.

        :param prefix: Key name prefix.
        :return: Dictionary of secret values indexed by parameter key.
        """
        keys = [key for key in self._list_secret_keys() if key.startswith(prefix)]
        return self.get_values(*keys)
