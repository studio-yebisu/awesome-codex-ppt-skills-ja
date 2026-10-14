from __future__ import annotations

import io
import zipfile
from pathlib import Path

_FIXED_ZIP_DT = (1980, 1, 1, 0, 0, 0)


def canonicalize_pptx_bytes(raw: bytes) -> bytes:
    """Normalize ZIP metadata ordering and timestamps for deterministic output bytes."""
    in_buffer = io.BytesIO(raw)
    out_buffer = io.BytesIO()

    with zipfile.ZipFile(in_buffer, "r") as zin:
        infos = sorted(zin.infolist(), key=lambda i: i.filename)
        with zipfile.ZipFile(
            out_buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as zout:
            for info in infos:
                payload = zin.read(info.filename)
                zinfo = zipfile.ZipInfo(filename=info.filename, date_time=_FIXED_ZIP_DT)
                zinfo.compress_type = zipfile.ZIP_DEFLATED
                zinfo.create_system = 0
                zinfo.external_attr = 0
                zinfo.flag_bits = 0
                zout.writestr(zinfo, payload)

    return out_buffer.getvalue()


def write_bytes(path: str | Path, data: bytes) -> None:
    Path(path).write_bytes(data)
