# q-toolkit (QEMU Toolkit)

q-toolkit is a collection of utility scripts for managing and interacting with QEMU virtual machines. 

## Tools

### q-cp

A script for copying files between the host and QEMU virtual machines.

**Usage:**
```
q-cp <source_path> <destination_path>
```

**Examples:**

```
# Copy from host to VM
$ q-cp /path/on/host domain:/path/in/vm

# Copy from VM to host
$ q-cp domain:/path/in/vm /path/on/host
```

### q-exec

A script for executing commands in QEMU virtual machines.

**Usage:**
```
q-exec [-it] <domain> -- <command>
```

**Examples:**
```
# Execute command in VM
q-exec my_vm -- ls -la /home

# Start interactive shell in VM
q-exec -it my_vm -- /bin/sh
```
