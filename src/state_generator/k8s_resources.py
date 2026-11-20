from constructs import Construct
from imports import k8s
from models import Workload
import yaml


class K8sWorkload(Construct):
    def __init__(self, scope: Construct, id: str, *, workload: Workload):
        super().__init__(scope, id)
        env_vars = (
        [k8s.EnvVar(name=k, value=str(v)) for k, v in workload.env_variables.items()]
        if workload.env_variables
        else None
        )
        ports = (
            [k8s.ContainerPort(container_port=workload.container_port)]
            if workload.container_port
            else None
        )
        self.container = k8s.Container(
            name=workload.name,
            image=workload.image,
            ports=ports,
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
        k8s.KubeService(self, "service",
            metadata=k8s.ObjectMeta(
                name=workload.name,
                namespace=service_namespace,
                labels={"app": workload.name},
            ),
            spec=k8s.ServiceSpec(
                type="ClusterIP",
                ports=[
                    k8s.ServicePort(
                        port=workload.service_port,
                        target_port=k8s.IntOrString.from_number(workload.container_port),
                    )
                ],
                selector={"app": workload.name},
            ),
        )
        if workload.config_map:
            k8s.KubeConfigMap(
                self, 'config',
                metadata=k8s.ObjectMeta(
                    name=workload.name,
                    namespace=service_namespace
                ),
                data={
                    'config.yaml': yaml.safe_dump(workload.config_map)
                }
            )

class CronJob(K8sWorkload):
    def __init__(self, scope: Construct, id: str, *, workload: Workload, service_namespace: str):
        super().__init__(scope, id, workload=workload)
        k8s.KubeCronJob(self, "cronjob",
            metadata=k8s.ObjectMeta(
                name=workload.name,
                namespace=service_namespace
            ),
            spec=k8s.CronJobSpec(
                schedule=workload.schedule,
                job_template=k8s.JobTemplateSpec(
                    spec=k8s.JobSpec(
                        template=k8s.PodTemplateSpec(
                            spec=k8s.PodSpec(
                                containers=[self.container],
                                restart_policy="OnFailure",
                            )
                        )
                    )
                )
            )
        )

        
