# platform-desired-state

## The goal of this repository is to ease the deployment and self-service of applications.
Decisions made for this implementation:
* shift left the validation (kubeconform, yamllint, pydantic models, kubescape)
* one operator for the cluster and namespaces
* complexity is hidden from user (example: an application can have public exposure from a configuration but the implementation is left out from user control)

---

## Repository Structure

```text
root/
├── .github/                  # GitHub workflows and actions
│   └── actions/
|   └── workflows/
│       └── validation.yml
├── services/                 # Collection of services for a cluster
│   ├── blueprint/            # Microservice 
|       └── web               # Kubernetes workload
|       └── storage           # Cloud resource
│   └── homepage/
├── src/                      # Main source code
│   └── generator/        
│       ├── __init__.py
|       ├── main.py                 # Entrypoint for the project
│       ├── models.py               # Pydantic models
|       ├── yaml_parser.py          # Parser YAML -> Python for Workloads
|       ├── k8s_generator.py        # Generator for k8s resources
├── .gitignore            # Files and directories to ignore in git
└── README.md             # Project documentation
└── pyproject.toml        # Poetry dependency manager
└── poetry.lock           # Record of installed packages and dependencies