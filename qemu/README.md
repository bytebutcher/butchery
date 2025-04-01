# q-toolkit (QEMU Toolkit)

q-toolkit is a collection of utility scripts for managing and interacting with QEMU virtual machines. 

## Setup

The following command bundles the individual q-tools into a single command:

```
bundle -s cp:q-cp,exec:q-exec,ps:q-ps,ssh:q-ssh -o q-ctl
```

## Usage

```
Usage: q-ctl [command] [args...]

Available commands:
  exec
  ps
  ssh
  cp
```


## Components

The following components can also be used individually.

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


### q-ps

A script for listing QEMU virtual machines.

**Usage:**
```
q-ps [-a]
```

**Options:**
```
-a    Show all VMs (including stopped)
```

**Example output:**
```
VM ID        NAME                 STATUS          CPU%      MEM%
1234         ubuntu-vm           running         2.5       4.2
5678         debian-vm           running         1.8       3.1
-            centos-vm           stopped         -         -
```


### q-ssh

```
Usage:
  q-ssh [options] <domain> [-- command]

Options:
  -p, --port PORT        Specify SSH port
  -u, --user USER        Specify SSH user
  -i, --identity FILE    Specify SSH private key path
  -h, --help             Show this help message

Examples:
  # SSH into VM
  q-ssh my_vm

  # SSH as ubuntu user
  q-ssh -u ubuntu my_vm

  # Use custom SSH port
  q-ssh -p 2222 my_vm

  # Run command in VM
  q-ssh my_vm -- ls -la
```

