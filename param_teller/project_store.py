from param_teller.parameter_store import ParameterStore
from param_teller.secrets_manager import SecretsManager


class ProjectStore(object):
    """
    Wrapper to the parameter store to access keys using CZI's service name conventions.
    """

    def __init__(self, backend, project, env, service, key_separator='/', lead_separator=False):
        """
        Initialize a project store for the specified backen.

        :param backend: Data storage backend.
        :param project: Project name.
        :param env: Environment name (e.g. prod, staging, dev)
        :param service: Service name.
        :param key_separator: Custom separator to use if we do not want to use paths.
        """
        self._backend_store = backend
        self._path = self._get_path(project, env, service)
        self._separator = key_separator
        self._lead_separator = lead_separator

    def get_service_parameters(self):
        # type: () -> dict
        """
        Retrieve values for the current service.

        :return: Dictionary of parameter values indexed by parameter key.
        """
        return self._backend_store.get_values_by_prefix(
                prefix="{lead}{path}{separator}".format(
                    path=self._path,
                    separator=self._separator,
                    lead=(self._separator if self._lead_separator else "")))

    def get_service_parameter(self, key):
        # type: (str) -> str
        """
        Retrieve single value for the current service.
        :param key: Parameter name.
        :return: Parameter Value
        """
        return self._backend_store.get_value("{lead}{path}{separator}{key}".format(
            path=self._path,
            key=key,
            separator=self._separator,
            lead=(self._separator if self._lead_separator else "")))

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


class ProjectParameterStore(ProjectStore):
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
        super(ProjectParameterStore, self).__init__(
            ParameterStore(with_decryption=with_decryption),
            project,
            env,
            service,
            key_separator or '/',
            key_separator is None)

    def get_service_parameters(self):
        # type: () -> dict
        """
        Retrieve values for the current service.

        :return: Dictionary of parameter values indexed by parameter key.
        """
        return self._backend_store.get_values_by_path(path=self._path) \
            if not self._separator \
            else super(ProjectParameterStore, self).get_service_parameters()


class ProjectSecretsManager(ProjectStore):

    def __init__(self, project, env, service, key_separator='/'):
        """
        Initialization.

        :param project: Project name.
        :param env: Environment name (e.g. prod, staging, dev)
        :param service: Service name.
        :param key_separator: Custom separator to use if we do not want to use paths.
        """
        super(ProjectSecretsManager, self).__init__(
            SecretsManager(),
            project,
            env,
            service,
            key_separator)
