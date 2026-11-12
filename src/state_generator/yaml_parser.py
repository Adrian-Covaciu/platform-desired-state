import yaml
import os
from models import *
from pathlib import Path

def open_file(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)

def parse_workload(file):
    data = open_file(file)
    return data

def parse_service(service_name):
    service = os.path.join("services/", service_name)
    path = Path(service)
    workloads_data = []
    for file in path.rglob("*wl.yaml"):
        workloads_data.append(parse_workload(file))
    service_instance = Service(name=service_name, workloads=workloads_data)
    return service_instance