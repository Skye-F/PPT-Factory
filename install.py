import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from urllib.request import urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
SKILLS = ROOT / ".agents" / "skills"


def install():
    sources = json.loads((ROOT / "config/skills-lock.json").read_text(encoding="utf-8"))
    SKILLS.mkdir(parents=True, exist_ok=True)
    for item in sources:
        target = SKILLS / item["name"]
        if target.exists():
            if not (target / "SKILL.md").is_file():
                raise RuntimeError(f"Incomplete install: {target}")
            print(f"Keeping existing {item['name']}", flush=True)
            continue
        url = f"https://codeload.github.com/{item['repo']}/zip/{item['commit']}"
        print(f"Installing {item['name']} from {url}", flush=True)
        with tempfile.TemporaryDirectory(prefix=".install-", dir=ROOT) as tmp:
            stage = Path(tmp) / "skill"
            stage.mkdir()
            with urlopen(url, timeout=120) as response:
                data = response.read()
            with ZipFile(io.BytesIO(data)) as archive:
                for member in archive.infolist():
                    name = member.filename.partition("/")[2]
                    prefix = item["source"] + "/" if item["source"] else ""
                    if member.is_dir() or not name.startswith(prefix):
                        continue
                    relative = name[len(prefix):]
                    if not prefix and relative.startswith("plugins/"):
                        continue
                    path = (stage / relative).resolve()
                    if not path.is_relative_to(stage.resolve()):
                        raise ValueError(f"Invalid archive member: {name}")
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(member) as src, path.open("wb") as dst:
                        shutil.copyfileobj(src, dst)
                if not (stage / "LICENSE").is_file():
                    license_member = next(m for m in archive.namelist() if m.partition("/")[2] == "LICENSE")
                    (stage / "LICENSE").write_bytes(archive.read(license_member))
            if not (stage / "SKILL.md").is_file():
                raise RuntimeError(f"Missing Skill entry: {item['name']}")
            stage.rename(target)

    env = ROOT / ".venv"
    python = env / "Scripts/python.exe"
    if not python.exists():
        subprocess.run([sys.executable, "-m", "venv", str(env)], check=True)
    subprocess.run([str(python), "-m", "pip", "install", "--only-binary=:all:",
                    "-r", str(ROOT / "config/requirements-lock.txt")], check=True)
    subprocess.run([str(python), "-m", "pip", "check"], check=True)
    (ROOT / "projects").mkdir(exist_ok=True)


if __name__ == "__main__":
    install()
