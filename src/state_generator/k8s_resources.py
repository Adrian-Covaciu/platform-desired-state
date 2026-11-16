from constructs import Construct
from imports import k8s
from models import Workload


class K8sWorkload(Construct):
    def __init__(self, scope: Construct, id: str, *, workload: Workload):
        super().__init__(scope, id)
        env_vars = (
        [k8s.EnvVar(name=k, value=str(v)) for k, v in workload.env_variables.items()]
        if workload.env_variables
        else None
        )
        self.container = k8s.Container(
            name=workload.name,
            image=workload.image,
            env=env_vars,
            )

class Api(K8sWorkload):
    def __init__(self, scope: Construct, id: str, *, workload: Workload, service_namespace: str):
        super().__init__(scope, id, workload=workload)
        k8s.KubeDeployment(self, "deployment",
                           metadata=k8s.ObjectMeta(
                                name=workload.name,
                                namespace=service_namespace,
                                labels={"app": workload.name},
                            ),
                           spec=k8s.DeploymentSpec(
                               replicas=workload.replicas,
                               selector=k8s.LabelSelector(match_labels={"app": workload.name}),
                               template=k8s.PodTemplateSpec(
                                   spec=k8s.PodSpec(
                                       containers=[self.container]
                                   )
                               )
                           )
                        )
        
