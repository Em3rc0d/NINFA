#!/usr/bin/env bash
set -euo pipefail

echo "== NINFA Chatterbox: WSL2 + NVIDIA Docker bootstrap =="

if ! grep -qi microsoft /proc/version; then
  echo "[ERROR] This script is intended for Linux running under WSL2."
  exit 1
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo "[ERROR] Automatic bootstrap currently supports Debian/Ubuntu-based WSL distributions."
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "[ERROR] Docker Engine is not installed in this WSL distribution."
  echo "Install Docker Engine first, then run this script again."
  exit 1
fi

if ! command -v nvidia-smi >/dev/null 2>&1; then
  echo "[ERROR] WSL cannot see an NVIDIA GPU."
  echo "Update the Windows NVIDIA driver and verify: nvidia-smi"
  exit 1
fi

echo "[1/7] GPU visible from WSL:"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader

echo "[2/7] Installing prerequisites..."
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg2

echo "[3/7] Adding NVIDIA Container Toolkit repository..."
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor --yes \
      -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L \
  https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list >/dev/null

echo "[4/7] Installing NVIDIA Container Toolkit..."
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

echo "[5/7] Configuring Docker NVIDIA runtime..."
sudo nvidia-ctk runtime configure --runtime=docker

echo "[6/7] Restarting Docker..."
if command -v systemctl >/dev/null 2>&1; then
  sudo systemctl restart docker || sudo service docker restart
else
  sudo service docker restart
fi

echo "[7/7] Validating GPU inside Docker..."
docker info | grep -i "Runtimes" || true
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi

echo
echo "SUCCESS: Docker can access the NVIDIA GPU from WSL2."
