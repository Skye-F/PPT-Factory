from pathlib import Path
import subprocess
import sys
from zipfile import ZipFile
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / ".agents/skills/ppt-master/scripts"
OUTPUT = ROOT / "tests/smoke/output"
PROJECT = OUTPUT / "fixture"
SVG = PROJECT / "svg_output"
SVG.mkdir(parents=True, exist_ok=True)

for n in range(1, 4):
    (SVG / f"slide_{n:02}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" lang="en-US">'
        f'<rect width="1280" height="720" fill="#F4F1E9"/>'
        f'<g id="title"><text x="80" y="170" font-family="Arial" font-size="56" fill="#142F39">PPT-Factory sample {n}</text></g>'
        '</svg>', encoding="utf-8")

def run(script, *args):
    subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], check=True)

run("svg_quality_checker.py", PROJECT, "--quick-generate", "--stage", "final", "--json")
deck = OUTPUT / "sample.pptx"
run("svg_to_pptx.py", PROJECT, "--quick-generate", "-o", deck)
with ZipFile(deck) as archive:
    for n in range(1, 4):
        xml = ElementTree.fromstring(archive.read(f"ppt/slides/slide{n}.xml"))
        assert any(e.text == f"PPT-Factory sample {n}" for e in xml.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t"))
print(f"Verified native text on 3 slides: {deck}")
