from http_firewall.acl import (
    ALLOW,
    load_config_file,
    build_acl,
    load_acl_config,
    check_allowed,
)
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


def test_acl_build_acl(temp_dir):
    """ test build_acl """

    with temp_dir() as _tmpdir:
        config_file = _tmpdir.joinpath('test.ini')

        with config_file.open('w') as _file:
            _file.write(ACL_CONFIG_1)

        # Write our test config
        loaded = load_config_file(str(config_file))
        new_acl = build_acl(loaded)

        assert new_acl is not None
        assert new_acl.check('public', '/api/v0/get', ALLOW)
        assert new_acl.check('public', '/api/v0/pin/ls', ALLOW)
        assert new_acl.check('127.0.0.1', '/api/v0/ping', ALLOW)
        assert not new_acl.check('127.0.0.1', '/api/v0/get', ALLOW)
        assert not new_acl.check('127.0.0.1', '/api/v0/pin/ls', ALLOW)
        assert not new_acl.check('public', '/api/v0/ping', ALLOW)


def test_acl_load_acl_config(temp_dir):
    """ test build_acl """

    with temp_dir() as _tmpdir:
        config_file = _tmpdir.joinpath('test.ini')

        with config_file.open('w') as _file:
            _file.write(ACL_CONFIG_1)

        # Write our test config
        new_acl = load_acl_config(str(config_file))

        assert new_acl is not None
        assert new_acl.check('public', '/api/v0/get', ALLOW)
        assert new_acl.check('public', '/api/v0/pin/ls', ALLOW)
        assert new_acl.check('127.0.0.1', '/api/v0/ping', ALLOW)
        assert not new_acl.check('127.0.0.1', '/api/v0/get', ALLOW)
        assert not new_acl.check('127.0.0.1', '/api/v0/pin/ls', ALLOW)
        assert not new_acl.check('public', '/api/v0/ping', ALLOW)


def test_acl_check_allowed(temp_dir):
    """ test build_acl """

    with temp_dir() as _tmpdir:
        config_file = _tmpdir.joinpath('test.ini')

        with config_file.open('w') as _file:
            _file.write(ACL_CONFIG_1)

        # Write our test config
        new_acl = load_acl_config(str(config_file))

        assert check_allowed('/api/v0/get')
        assert check_allowed('/api/v0/pin/ls')
        assert check_allowed('/api/v0/pin/ls', '127.0.0.1')
        assert check_allowed('/api/v0/ping', '127.0.0.1')
        assert not check_allowed('/api/v0/ping')
