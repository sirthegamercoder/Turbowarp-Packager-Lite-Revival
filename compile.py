import sys
import shutil
import zipfile
from pathlib import Path
from PyInstaller.__main__ import run
from setuptools import setup

script_dir = Path(__file__).parent.absolute()

name_game_path = script_dir / "name-project.txt"
with open(name_game_path, "r") as file:
    name_game = file.read()

name_game_alt_path = script_dir / "name-project-page.txt"
with open(name_game_alt_path, "r") as file:
    title = file.read()

base_args = [
    "--noconfirm",
    "--onedir",
    "--windowed",
    f"--name={name_game}",
    "--clean",
    "--exclude-module=setuptools",
]

if sys.platform == "win32":
    base_args.append(f'--icon={script_dir / "icon.ico"}')
else:
    pass

if sys.platform == "win32":
    base_args.append(f'--add-data={script_dir / "resources" / "app"};resources/app/')
else:
    base_args.append(f'--add-data={script_dir / "resources" / "app"}:resources/app/')

base_args.append(str(script_dir / "window.py"))

def compile_for_macos():
    APP = ['window.py']
    DATA_FILES = ["resources/app"]
    OPTIONS = {
        'argv_emulation': True,
        'iconfile': 'icon.icns',
    }

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )

def zip_and_cleanup():
    dist_dir = script_dir / "dist"
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
    if sys.platform == "win32" or sys.platform == "linux":
        run(base_args)
    else:
        compile_for_macos()
        
    zip_and_cleanup()
