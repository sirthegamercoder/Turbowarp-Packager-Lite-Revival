import sys
import shutil
import zipfile
from pathlib import Path
from PyInstaller.__main__ import run

script_dir = Path(__file__).parent.absolute()

name_game_path = script_dir / "assets" / "name-project.txt"
with open(name_game_path, "r") as file:
    name_game = file.read()

name_game_alt_path = script_dir / "assets" / "name-project-page.txt"
with open(name_game_alt_path, "r") as file:
    title = file.read()

base_args = [
    "--noconfirm",
    "--onedir",
    "--windowed",
    f'--distpath={script_dir / "export" / "dist"}',
    f'--workpath={script_dir / "export" / "build"}',
    f'--specpath={script_dir / "export"}',
    f"--name={name_game}",
    "--clean",
    "--exclude-module=setuptools",
]

if sys.platform == "win32":
    base_args.append(f'--icon={script_dir / "assets" / "icon.ico"}')
elif sys.platform == "darwin":
    base_args.append(f'--icon={script_dir / "assets" / "icon.icns"}')
else:
    pass

if sys.platform == "win32":
    base_args.append(f'--add-data={script_dir / "assets"};assets/')
else:
    base_args.append(f'--add-data={script_dir / "assets"}:assets/')

base_args.append(str(script_dir / "app" / "window.py"))


def zip_and_cleanup():
    dist_dir = script_dir / "export" / "dist"
    app_dir = dist_dir / name_game
    zip_path = dist_dir / f"{title}.zip"

    if not app_dir.exists():
        print(f"Build directory not found: {app_dir}")
        return

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in app_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(app_dir.parent)
                zipf.write(file_path, arcname)

    shutil.rmtree(app_dir)


if __name__ == "__main__":
    run(base_args)
    zip_and_cleanup()
