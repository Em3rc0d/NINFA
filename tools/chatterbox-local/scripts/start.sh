#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ ! -f .env ]; then
  cp .env.example .env
fi

mkdir -p voices inputs outputs hf-cache pkuseg-cache

echo "Checking Docker GPU access..."
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi >/dev/null

echo "Building and starting Chatterbox..."
docker compose up --build -d

echo
docker exec chatterbox-local python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'); print('VRAM GB:', round(torch.cuda.get_device_properties(0).total_memory/1024**3,2) if torch.cuda.is_available() else 0)"
echo
echo "Open: http://localhost:${CHATTERBOX_PORT:-7860}"
echo "Logs: docker logs -f chatterbox-local"
