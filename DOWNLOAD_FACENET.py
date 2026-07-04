"""Download FaceNet512 ONNX model into models_local/."""

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "models_local" / "facenet512.onnx"


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)

    if TARGET.exists():
        print(f"Model already exists at {TARGET}")
        return

    print("Attempting Kaggle download (requires kaggle CLI + credentials)...")
    try:
        subprocess.run(
            ["kaggle", "kernels", "output", "ruicampos/facenet512", "-p", str(TARGET.parent)],
            check=True,
        )
        downloaded = next(TARGET.parent.glob("*.onnx"), None)
        if downloaded and downloaded != TARGET:
            shutil.move(str(downloaded), str(TARGET))
        print(f"Saved model to {TARGET}")
    except Exception as exc:
        print(f"Automatic download failed: {exc}")
        print(
            "\nManual steps:\n"
            "1. Download facenet512.onnx from Kaggle: ruicampos/facenet512\n"
            f"2. Place it at: {TARGET}\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
