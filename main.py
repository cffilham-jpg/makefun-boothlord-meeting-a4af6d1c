"""Write the one-line meeting-killer entry for make.fun."""

import hashlib
import os
import tempfile
from pathlib import Path

LINE = "The projector is the only one presenting."
CHAR_LIMIT = 200


def _resolve_output_dir() -> Path:
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        path = Path(env_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    try:
        out = Path("out")
        out.mkdir(parents=True, exist_ok=True)
        return out
    except OSError:
        return Path(tempfile.mkdtemp(prefix="makefun-boothlord-meeting-a4af6d1c-"))


def validate(path: Path) -> None:
    data = path.read_bytes()
    text = data.decode("utf-8")
    if text != LINE:
        raise ValueError("entry.txt content does not match LINE")
    if not 1 <= len(text) <= CHAR_LIMIT:
        raise ValueError("line must be 1-200 chars")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")


def main() -> None:
    out_dir = _resolve_output_dir()
    target = out_dir / "entry.txt"
    target.write_text(LINE, encoding="utf-8")
    validate(target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"wrote {target} ({len(LINE)} chars, sha256 {digest})")


if __name__ == "__main__":
    main()
