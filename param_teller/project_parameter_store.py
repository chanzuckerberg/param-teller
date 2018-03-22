from param_teller.parameter_store import ParameterStore


class ProjectParameterStore(object):
    """
    Wrapper to the parameter store to access keys using CZI's service name conventions.
    """

    def __init__(self, project, env, service, with_decryption=True, key_separator=None):
        """
        Initialization.

        :param project: Project name.
        :param env: Environment name (e.g. prod, staging, dev)
        :param service: Service name.
        :param key_separator: Custom separator to use if we do not want to use paths.
        """
        self._parameter_store = ParameterStore(with_decryption=with_decryption)
        self._path = self._get_path(project, env, service)
        self._separator = key_separator

    def get_service_parameters(self):
        # type: () -> dict
        """
        Retrieve values for the current service.

        :return: Dictionary of parameter values indexed by parameter key.
        """
        return self._parameter_store.get_values_by_path(path=self._path) \
            if not self._separator \
            else self._parameter_store.get_values_by_prefix(
                prefix="{path}{separator}".format(path=self._path, separator=self._separator))

    def get_service_parameter(self, key):
        # type: (str) -> str
        """
        Retrieve single value for the current service.
        :param key: Parameter name.
        :return: Parameter Value
        """
        fullkey = "{path}/{key}".format(path=self._path, key=key) \
            if not self._separator \
            else "{path}.{key}".format(path=self._path, key=key)
        return self._parameter_store.get_value(fullkey)

    @staticmethod
    def _get_path(project, env, service):
        """
        Compute prefix according to CZI's convention
        :param project: Project name.
        :param env: Environment name (e.g. prod, staging, dev)
        :param service: Service name.
        :return: Full service name.
        """
        # type: (str, str, str) -> str
        return "{project}-{env}-{service}".format(project=project, env=env, service=service)


