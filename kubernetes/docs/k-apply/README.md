# k-apply

k-apply is an enhanced version of `kubectl apply` that allows patching of Kubernetes manifests before applying them to the cluster. 

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Patch Types](#patch-types)
4. [Advanced Usage](#advanced-usage)
5. [Verbose Mode](#verbose-mode)
6. [Limitations and Troubleshooting](#limitations-and-troubleshooting)

## Installation

Ensure you have Python 3.6+ installed. Then, clone the repository and add the directory to your PATH.

```bash
git clone https://github.com/your-repo/k-toolkit.git
export PATH=$PATH:/path/to/k-toolkit
```

## Basic Usage

```
k-apply -f <base_yaml_file> [-p <patch>...] [kubectl_options]
```

### Options

- `-f, --filename`: Path to the base YAML file or `-` for stdin (required)
- `-p, --patch`: Patch file(s), string(s) or `-` for stdin (can be specified multiple times)
- `-v, --verbose`: Increase output verbosity
- `-h, --help`: Show help message and exit

All other `kubectl apply` options are supported and passed through to kubectl.

## Patch Types

k-apply supports both string-based and file-based patches. Let's look at examples of each:

### 1. Modifying a Single Value

String-based:
```bash
k-apply -f deployment.yaml -p "spec.replicas=3"
```

File-based (`patch.yaml`):
```yaml
spec:
  replicas: 3
```
```bash
k-apply -f deployment.yaml -p patch.yaml
```

### 2. Updating Nested Structures

String-based:
```bash
k-apply -f deployment.yaml -p "spec.template.spec.containers[0].image=nginx:latest"
```

File-based (`patch.yaml`):
```yaml
spec:
  template:
    spec:
      containers:
        - image: nginx:latest
```
```bash
k-apply -f deployment.yaml -p patch.yaml
```

### 3. Adding to Lists

String-based:
```bash
k-apply -f deployment.yaml -p "spec.template.spec.containers[0].ports+=[{containerPort: 8080}]"
```

File-based (`patch.yaml`):
```yaml
spec:
  template:
    spec:
      containers:
        - ports:
            +:
              - containerPort: 8080
```
```bash
k-apply -f deployment.yaml -p patch.yaml
```

### 4. Multiple Patches

String-based:
```bash
k-apply -f deployment.yaml -p "metadata.labels.env=prod" -p "spec.replicas=5"
```

File-based (`patch.yaml`):
```yaml
metadata:
  labels:
    env: prod
spec:
  replicas: 5
```
```bash
k-apply -f deployment.yaml -p patch.yaml
```

## Advanced Usage

### Complex Structure Modifications

String-based:
```bash
k-apply -f deployment.yaml \
  -p "spec.template.spec.containers[0].image=nginx:latest" \
  -p "spec.template.spec.containers[1].resources.limits.cpu=500m"
```

File-based (`patch.yaml`):
```yaml
spec:
  template:
    spec:
      containers:
        - image: nginx:latest
        - resources:
            limits:
              cpu: 500m
```
```bash
k-apply -f deployment.yaml -p patch.yaml
```

### Complex List Operations

String-based:
```bash
k-apply -f deployment.yaml \
  -p "spec.template.spec.containers[0].env+=[{name: DEBUG, value: 'true'}]" \
  -p "spec.template.spec.containers[0].ports+=[{containerPort: 8080}, {containerPort: 8081}]"
```

File-based (`patch.yaml`):
```yaml
spec:
  template:
    spec:
      containers:
        - env:
            +:
              - name: DEBUG
                value: 'true'
          ports:
            +:
              - containerPort: 8080
              - containerPort: 8081
```
```bash
k-apply -f deployment.yaml -p patch.yaml
```

## Verbose Mode

Use `-v` or `--verbose` to see detailed diff output:

```bash
k-apply -f deployment.yaml -p patch.yaml -v
```

This will show you exactly what changes are being made to your YAML before it's applied.

## Troubleshooting

If you encounter issues:

1. Use verbose mode (`-v`) to see detailed patch applications.
2. Ensure your base YAML and patches are valid YAML/JSON.
3. Check that your kubectl context is set correctly.

For more complex scenarios or if you're unsure about the patch syntax, consider using file-based patches for better readability and easier debugging.
