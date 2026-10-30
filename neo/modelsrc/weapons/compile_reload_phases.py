"""Compile all reload-phase QCs to a chosen output directory.

Run: python compile_reload_phases.py --compiler PATH --output PATH
Runtime depends on the number of QCs and Source SDK Base 2013 MP version.
"""
import argparse
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile


def model_output(qc, staging):
    text = qc.read_text(encoding="utf-8")
    match = re.search(r'^\$modelname\s+"([^"]+)"', text, re.MULTILINE)
    if not match:
        raise RuntimeError(f"No $modelname in {qc}")
    model = staging / "models" / Path(*PurePosixPath(match.group(1)).parts)
    return model.with_suffix("") if model.suffix.lower() == ".mdl" else model


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--compiler", type=Path, required=True,
        help="Source SDK Base 2013 Multiplayer/bin/studiomdl.exe",
    )
    parser.add_argument(
        "--output", type=Path, required=True,
        help="Directory to receive compiled model files",
    )
    args = parser.parse_args()
    compiler = args.compiler.resolve()
    output = args.output.resolve()
    if not compiler.is_file():
        parser.error("Compiler does not exist: " + str(compiler))
    root = Path(__file__).resolve().parent
    qcs = sorted(root.glob("*/*.qc"))
    if not qcs:
        raise RuntimeError(f"No QC files found under {root}")

    with tempfile.TemporaryDirectory(prefix="neo-reload-phases-") as temporary:
        staging = Path(temporary)
        (staging / "gameinfo.txt").write_text(
            '"GameInfo" { "game" "Reload phase compile" "FileSystem" { '
            '"SteamAppId" "243750" "SearchPaths" { '
            '"Game" "|gameinfo_path|." } } }\n',
            encoding="ascii",
        )
        for qc in qcs:
            subprocess.run(
                [str(compiler), "-nop4", "-game", str(staging), str(qc)],
                cwd=qc.parent,
                check=True,
            )
            model = model_output(qc, staging)
            for extension in (".mdl", ".vvd", ".dx90.vtx"):
                if not Path(str(model) + extension).is_file():
                    raise RuntimeError(
                        f"Compiler did not create {model}{extension} for {qc}"
                    )

        model_dir = staging / "models" / "weapons"
        outputs = sorted(model_dir.glob("*"))
        if not outputs:
            raise RuntimeError("Compiler produced no models")
        output.mkdir(parents=True, exist_ok=True)
        for path in outputs:
            shutil.copy2(path, output / path.name)
            print("COMPILED", path.name, "->", output / path.name)
        print(f"COMPILE_PASS {len(qcs)} QCs, {len(outputs)} output files")


if __name__ == "__main__":
    main()
