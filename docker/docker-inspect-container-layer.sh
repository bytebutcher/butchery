#!/bin/bash
# ##################################################
# NAME:
#   docker-inspect-container-layers
# DESCRIPTION:
#   Lists the filesystem layer paths of a Docker 
#   container starting from the base image layer 
#   to the container's read-write layer.
# HISTORY:
#   2024-03-08: Initial version
# AUTHOR:
#   bytebutcher
# ##################################################

if [ -z "$1" ]; then
    echo "Usage: $0 <container-name>"
    exit 1
fi

container_name="$1"

# Get container information
container_info=$(docker inspect "$container_name")

# Extract container ID
container_id=$(echo "$container_info" | jq -r '.[0].Id')

# Extract the container's root directory from the inspect command
container_root_dir=$(echo "$container_info" | jq -r '.[0].GraphDriver.Data.MergedDir')

# List layers in the correct order
layers=$(echo "$container_info" | jq -r '.[0].GraphDriver.Data.LowerDir' | tr ':' '\n' | tac)

# Print layer paths
echo "Layers for container $container_name ($container_id):"

# Loop through each layer
counter=1
for layer in $layers; do
    echo "LAYER $counter: $layer"
    ((counter++))
done

# The last layer is the merged directory
echo "LAYER $counter: $container_root_dir"

