from models import *
from yaml_parser import *

if __name__ == "__main__":
    service = parse_service("blueprint")
    print(service)