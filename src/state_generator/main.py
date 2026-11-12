from models import *
from parser import *

if __name__ == "__main__":
    service_obj = parse_service("blueprint")
    print(service_obj)