import os
import re
import time
import uuid
import subprocess
from pathlib import Path

import gradio as gr
import torch
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

ROOT = Path("/workspace")
OUTPUTS = ROOT / "outputs"
TMP = ROOT / "inputs" / "_tmp"
OUTPUTS.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)

REQUESTED_DEVICE = os.getenv("DEVICE", "auto").strip().lower()

if REQUESTED_DEVICE == "auto":
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
elif REQUESTED_DEVICE == "cuda" and not torch.cuda.is_available():
    raise RuntimeError(
        "DEVICE=cuda was requested but PyTorch cannot see CUDA. "
        "Run scripts/setup-wsl-cuda.sh and verify Docker GPU access first."
    )
else:
    DEVICE = REQUESTED_DEVICE

print(f"[chatterbox] torch={torch.__version__}")
print(f"[chatterbox] device={DEVICE}")
if DEVICE == "cuda":
    print(f"[chatterbox] gpu={torch.cuda.get_device_name(0)}")
    print(
        "[chatterbox] vram_gb="
        f"{torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f}"
    )

_model = None


def get_model():
    global _model
    if _model is None:
        # PyPI chatterbox-tts==0.1.7 does NOT accept t3_model="v3".
        # Keep this call aligned with the pinned release API.
        _model = ChatterboxMultilingualTTS.from_pretrained(device=DEVICE)
    return _model


def normalize_reference(path: str) -> str:
    if not path:
        raise gr.Error("Upload a reference audio or video file.")

    src = Path(path)
    if not src.exists():
        raise gr.Error(f"Reference file does not exist: {src}")

    out = TMP / f"ref-{uuid.uuid4().hex}.wav"
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(src),
        "-map",
        "0:a:0",
        "-vn",
        "-ac",
        "1",
        "-ar",
        "24000",
        "-c:a",
        "pcm_s16le",
        str(out),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        detail = result.stderr.strip()[-1200:]
        raise gr.Error(f"FFmpeg could not normalize the reference. {detail}")
    return str(out)


def chunk_text(text: str, max_chars: int = 260):
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, current = [], ""

    for sentence in sentences:
        parts = (
            [sentence[i : i + max_chars] for i in range(0, len(sentence), max_chars)]
            if len(sentence) > max_chars
            else [sentence]
        )

        for part in parts:
            candidate = (current + " " + part).strip()
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                current = part

    if current:
        chunks.append(current)

    return chunks


def synthesize(text, language, reference, cfg_weight, exaggeration, temperature):
    if not text or not text.strip():
        raise gr.Error("Enter text to synthesize.")

    ref_wav = normalize_reference(reference)
    model = get_model()
    chunks = chunk_text(text)

    if not chunks:
        raise gr.Error("No usable text found.")

    pieces = []
    silence = None
    started = time.perf_counter()

    try:
        for index, chunk in enumerate(chunks, 1):
            wav = model.generate(
                chunk,
                language_id=language,
                audio_prompt_path=ref_wav,
                cfg_weight=float(cfg_weight),
                exaggeration=float(exaggeration),
                temperature=float(temperature),
            ).cpu()

            pieces.append(wav)

            if index < len(chunks):
                if silence is None:
                    silence = torch.zeros((1, int(model.sr * 0.22)))
                pieces.append(silence)

    except torch.OutOfMemoryError as exc:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        raise gr.Error(
            "CUDA ran out of memory. Close other GPU-heavy apps, retry a shorter "
            "section, or set DEVICE=cpu as a fallback."
        ) from exc

    final = torch.cat(pieces, dim=-1)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    out = OUTPUTS / f"narration-{language}-{stamp}.wav"
    ta.save(str(out), final, model.sr)

    elapsed = time.perf_counter() - started
    duration = final.shape[-1] / model.sr
    rtf = elapsed / duration if duration else 0.0

    status = (
        f"Generated {duration:.1f}s audio in {elapsed:.1f}s | "
        f"RTF={rtf:.2f} | device={DEVICE} | chunks={len(chunks)}"
    )
    return str(out), status


with gr.Blocks(title="Chatterbox Local — Does It Automate") as demo:
    gr.Markdown(
        "# Chatterbox Local\n"
        "Local multilingual voice cloning for Does It Automate."
    )

    with gr.Row():
        with gr.Column():
            text = gr.Textbox(
                label="Narration",
                lines=12,
                placeholder="Paste the script here...",
            )
            language = gr.Dropdown(
                choices=[
                    ("Spanish", "es"),
                    ("English", "en"),
                    ("Portuguese", "pt"),
                    ("French", "fr"),
                    ("German", "de"),
                    ("Italian", "it"),
                ],
                value="en",
                label="Narration text language",
            )
            reference = gr.File(
                label="Voice reference — audio or video",
                file_types=["audio", "video"],
                type="filepath",
            )

            with gr.Accordion("Advanced", open=False):
                cfg = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    step=0.05,
                    value=0.0,
                    label="CFG weight",
                )
                exaggeration = gr.Slider(
                    minimum=0.25,
                    maximum=2.0,
                    step=0.05,
                    value=0.5,
                    label="Exaggeration",
                )
                temperature = gr.Slider(
                    minimum=0.05,
                    maximum=2.0,
                    step=0.05,
                    value=0.8,
                    label="Temperature",
                )

            run = gr.Button("Generate narration", variant="primary")

        with gr.Column():
            audio = gr.Audio(label="Generated narration", type="filepath")
            status = gr.Textbox(label="Benchmark", interactive=False)
            gr.Markdown(
                "**Cross-language tip:** Spanish reference + English narration "
                "worked well with CFG weight = **0.0** in the validated NINFA setup."
            )

    run.click(
        synthesize,
        inputs=[text, language, reference, cfg, exaggeration, temperature],
        outputs=[audio, status],
    )

demo.queue().launch(server_name="0.0.0.0", server_port=7860)
