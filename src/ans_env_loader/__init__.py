# vars_plugins/import_env_vars.py

import os
from pathlib import Path

from ansible.errors import AnsibleError
from ansible.plugins.vars import BaseVarsPlugin


class VarsModule(BaseVarsPlugin):
    def get_vars(self, loader, path, entities, cache=True):
        env_vars_path = Path(path) / 'env-var-names.yaml'

        if not env_vars_path.exists():
            raise AnsibleError('Expected "env-var-names.yaml" to exist')

        var_names = loader.load_from_file(env_vars_path.as_posix())
        if not isinstance(var_names, list):
            raise AnsibleError('Expected "env-var-names.yaml" to be a list of env variable names')

        missing = []
        result = {}
        for var in var_names:
            val = os.environ.get(var)
            if val is None:
                missing.append(var)
            else:
                result[var] = val

        if missing:
            raise AnsibleError('Required env variables not set: {}'.format(', '.join(missing)))

        return result
