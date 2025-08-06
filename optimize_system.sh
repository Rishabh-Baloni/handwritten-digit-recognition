#!/bin/bash

# Script to optimize system settings for TensorFlow performance
# This script should be run with sudo privileges

echo "Optimizing system settings for TensorFlow performance..."

# Disable CPU throttling
echo "Disabling CPU throttling..."
for governor in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
  if [ -f "$governor" ]; then
    echo performance > "$governor"
  fi
done

# Set memory management parameters
echo "Setting memory management parameters..."
echo 1 > /proc/sys/vm/overcommit_memory
echo 65536 > /proc/sys/vm/min_free_kbytes
echo 65536 > /proc/sys/vm/swappiness

# Set I/O scheduler to deadline for better performance
echo "Setting I/O scheduler to deadline..."
for disk in /sys/block/sd*; do
  if [ -d "$disk" ]; then
    echo deadline > "$disk/queue/scheduler"
  fi
done

# Disable transparent hugepages
echo "Disabling transparent hugepages..."
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag

# Set process priority for Python processes
echo "Setting process priority for Python processes..."
renice -n -10 $(pgrep -f python) 2>/dev/null

echo "System optimization complete!"