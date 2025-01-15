# k-toolkit (Kubernetes Toolkit)

k-toolkit is a collection of utility scripts for working with Kubernetes clusters. 
This toolbox provides enhanced functionality and convenience for common Kubernetes operations.

## Tools

### k-apply

An enhanced version of kubectl apply that allows patching of Kubernetes manifests before applying them to the cluster.

**Key Features:**
- Apply patches to YAML manifests
- Support for file-based, string-based, and stdin patches
- Handles nested structures and lists in YAML
- Compatible with all kubectl apply options

**Usage:**
```
k-apply -f <base_yaml_file> [-p <patch_file>...] [kubectl_options]
```

For detailed usage instructions and advanced features, see the [k-apply README.md](docs/k-apply/README.md).
