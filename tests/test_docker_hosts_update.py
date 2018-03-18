import pytest
import docker_hosts_update
import docker
import os
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock
from click.testing import CliRunner

def test_update_hosts_file_initial(tmpdir, monkeypatch):
    def map_hosts():
        return { 'nginx.corp.internal': ['172.0.0.2'] }
    monkeypatch.setattr(docker_hosts_update, 'map_hosts', map_hosts)

    testfile = "tests/default_hosts"
    fn = tmpdir.join("default_hosts")
    fn.write(Path(testfile).read_text())
    shutil.copyfile(testfile, fn)
    docker_hosts_update.update_hosts_file(filename=fn)
    
    expected = Path('tests/default_hosts_expected').read_text()    
    actual = Path(fn).read_text()
    
    assert actual == expected


def test_update_hosts_file_replace(tmpdir, monkeypatch):
    def map_hosts():
        return { 'nginx.corp.internal': ['172.0.0.3'] }
    monkeypatch.setattr(docker_hosts_update, 'map_hosts', map_hosts)

    testfile = "tests/preexisting_section_hosts"
    fn = tmpdir.join("preexisting_section_hosts")
    fn.write(Path(testfile).read_text())
    shutil.copyfile(testfile, fn)
    docker_hosts_update.update_hosts_file(filename=fn)
    
    expected = Path('tests/preexisting_section_hosts_expected').read_text()    
    actual = Path(fn).read_text()
    
    assert actual == expected


def test_main_no_events(tmpdir, monkeypatch):
    mock_update_hosts_file = Mock(return_value=True)
    mocked_docker_client = Mock()
    mocked_docker_client.events.return_value = []
    
    monkeypatch.setattr(docker_hosts_update, 'update_hosts_file', mock_update_hosts_file)
    monkeypatch.setattr(docker, 'from_env', Mock(return_value=mocked_docker_client))

    runner = CliRunner()
    result = runner.invoke(docker_hosts_update.main, [])
    assert result.exit_code == 0
    mock_update_hosts_file.assert_called_once_with('/etc/hosts')


def test_main_once(tmpdir, monkeypatch):
    mock_update_hosts_file = Mock(return_value=True)
    mocked_docker_client = Mock()
    mocked_docker_client.events.return_value = []
    
    monkeypatch.setattr(docker_hosts_update, 'update_hosts_file', mock_update_hosts_file)
    monkeypatch.setattr(docker, 'from_env', Mock(return_value=mocked_docker_client))

    runner = CliRunner()
    result = runner.invoke(docker_hosts_update.main, ['--once'])
    assert result.exit_code == 0
    mock_update_hosts_file.assert_called_once_with('/etc/hosts')
    mocked_docker_client.events.assert_not_called()


def test_main_skip_initial(tmpdir, monkeypatch):
    mock_update_hosts_file = Mock(return_value=True)
    mocked_docker_client = Mock()
    mocked_docker_client.events.return_value = []
    
    monkeypatch.setattr(docker_hosts_update, 'update_hosts_file', mock_update_hosts_file)
    monkeypatch.setattr(docker, 'from_env', Mock(return_value=mocked_docker_client))

    runner = CliRunner()
    result = runner.invoke(docker_hosts_update.main, ['--skip-initial'])
    assert result.exit_code == 0
    assert mock_update_hosts_file.call_count == 0


def test_main_non_triggering(tmpdir, monkeypatch):
    mock_update_hosts_file = Mock(return_value=True)
    mocked_docker_client = Mock()
    mocked_docker_client.events.return_value = [
        {'status': 'create', 'id': 'a4f9371f5fe97da062f3bd3341fdabc63c69f76936cc39c5d4e6e30c051bb25d', 'from': 'nginx', 'Type': 'container', 'Action': 'create', 'Actor': {'ID': 'a4f9371f5fe97da062f3bd3341fdabc63c69f76936cc39c5d4e6e30c051bb25d', 'Attributes': {'image': 'nginx', 'maintainer': 'NGINX Docker Maintainers <docker-maint@nginx.com>', 'name': 'sad_blackwell'}}, 'scope': 'local', 'time': 1521391634, 'timeNano': 1521391634051801951},
        {'status': 'resize', 'id': 'a4f9371f5fe97da062f3bd3341fdabc63c69f76936cc39c5d4e6e30c051bb25d', 'from': 'nginx', 'Type': 'container', 'Action': 'resize', 'Actor': {'ID': 'a4f9371f5fe97da062f3bd3341fdabc63c69f76936cc39c5d4e6e30c051bb25d', 'Attributes': {'height': '24', 'image': 'nginx', 'maintainer': 'NGINX Docker Maintainers <docker-maint@nginx.com>', 'name': 'sad_blackwell', 'width': '80'}}, 'scope': 'local', 'time': 1521391634, 'timeNano': 1521391634447606018}
    ]
    
    monkeypatch.setattr(docker_hosts_update, 'update_hosts_file', mock_update_hosts_file)
    monkeypatch.setattr(docker, 'from_env', Mock(return_value=mocked_docker_client))

    runner = CliRunner()
    result = runner.invoke(docker_hosts_update.main, ['--skip-initial'])
    assert result.exit_code == 0
    assert mock_update_hosts_file.call_count == 0


def test_main_triggering(tmpdir, monkeypatch):
    mock_update_hosts_file = Mock(return_value=True)
    mocked_docker_client = Mock()
    mocked_docker_client.events.return_value = [
        {'status': 'start', 'id': 'a4f9371f5fe97da062f3bd3341fdabc63c69f76936cc39c5d4e6e30c051bb25d', 'from': 'nginx', 'Type': 'container', 'Action': 'start', 'Actor': {'ID': 'a4f9371f5fe97da062f3bd3341fdabc63c69f76936cc39c5d4e6e30c051bb25d', 'Attributes': {'image': 'nginx', 'maintainer': 'NGINX Docker Maintainers <docker-maint@nginx.com>', 'name': 'sad_blackwell'}}, 'scope': 'local', 'time': 1521391634, 'timeNano': 1521391634444290501}
    ]
    
    monkeypatch.setattr(docker_hosts_update, 'update_hosts_file', mock_update_hosts_file)
    monkeypatch.setattr(docker, 'from_env', Mock(return_value=mocked_docker_client))

    runner = CliRunner()
    result = runner.invoke(docker_hosts_update.main, ['--skip-initial'])
    assert result.exit_code == 0
    mock_update_hosts_file.assert_called_once_with('/etc/hosts')
    assert mock_update_hosts_file.call_count == 1

