from cdk8s import App, Chart, YamlOutputType
from k8s_resources import Api
from yaml_parser import *
from from_root import from_root
import os

def generate_service(service_name):
    outdir = from_root(f"rendered/k8s/{service_name}")
    app = App(outdir=str(outdir), output_file_extension=".yaml", yaml_output_type=YamlOutputType.FILE_PER_RESOURCE)
    chart = Chart(app, service_name)
    parsed_service = parse_service(service_name)
    for workload in parsed_service.workloads:
        Api(chart, workload.name, workload=workload, service_namespace=parsed_service.name)
    app.synth()

def generate_all_services():
    service_list = os.listdir(from_root("services"))
    for service in service_list:
        generate_service(service)