import pytest
import docker_hosts_update
import os
import shutil
from pathlib import Path

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


    print(actual)
    print(len(actual))
    
    print("---")

    print(expected)
    print(len(expected))
    
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

    print(actual)
    print(len(actual))
    
    print("---")

    print(expected)
    print(len(expected))
    
    assert actual == expected
