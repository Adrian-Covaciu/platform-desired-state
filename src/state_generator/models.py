from typing import Literal
from pydantic import BaseModel


class Resource(BaseModel):
    name: str
    type : Literal["ecr", "s3"]

class Workload(BaseModel):
    name: str
    type: Literal["api", "cronjob"]
    image: str
    replicas: int = 1
    schedule: str | None = None
    env_variables: dict | None = None
    config_map: dict | None = None

class Service(BaseModel):
    name: str
    workloads: list[Workload]
    # resources: list[Resource]

