import psycopg2
import docker
from docker.models.containers import Container
from typing import Tuple


def get_connection():
    container = get_docker_container_by_name('pg-docker')
    ip_address, port = get_network_settings_from_container(container)
    conn = psycopg2.connect(dbname='evs',
                            user='postgres',
                            password='docker',
                            host=ip_address,
                            port=port)
    return conn


def get_docker_container_by_name(name: str) -> Container:
    client = docker.from_env()
    container_list = client.containers.list(filters={'name': name})
    assert len(container_list) == 1, f'Could not find Docker container with name: {name}'
    return container_list[0]


def get_network_settings_from_container(container: Container) -> Tuple[str, int]:
    settings = container.attrs['NetworkSettings']
    ip_address = settings['IPAddress']

    ports = list(settings['Ports'].keys())
    assert len(ports) == 1, f'Found multiple ports in Docker container: {container.name}'
    port = int(ports[0].split('/')[0])  # '5432/tcp' -> 5432

    return ip_address, port
