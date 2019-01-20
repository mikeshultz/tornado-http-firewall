from http_firewall.acl import load_config_file
from .const import ACL_CONFIG_1


def test_acl_load_config(temp_dir):
    """ test load_config """

    with temp_dir() as _tmpdir:
        config_file = _tmpdir.joinpath('test.ini')

        with config_file.open('w') as _file:
            _file.write(ACL_CONFIG_1)

        # Write our test config
        loaded = load_config_file(str(config_file))
        assert isinstance(loaded, dict)
        assert 'roles' in loaded
        assert 'public' in loaded['roles']
        assert '127.0.0.1' in loaded['roles']
        assert isinstance(loaded['roles']['public'], list)
        assert isinstance(loaded['roles']['127.0.0.1'], list)
        assert len(loaded['roles']['public']) == 2
        assert len(loaded['roles']['127.0.0.1']) == 1
