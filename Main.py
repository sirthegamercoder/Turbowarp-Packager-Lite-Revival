from pathlib import Path
import sys
import re
import webview
import subprocess
from lxml import html


def resource_path(relative_path):
    try:
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path.cwd()
    return str(base_path / relative_path)


def determine_app_icon():
    if sys.platform == "win32":
        return resource_path("resources/app/icon.ico")
    elif sys.platform == "darwin":
        return resource_path("resources/app/icon.icns")
    else:
        return resource_path("resources/app/icon.png")


def ensure_index_html():
    root = Path.cwd()
    main_dir = root / "resources" / "app"
    index_file = main_dir / "index.html"

    if index_file.exists():
        return

    html_files = sorted(main_dir.glob("*.html"))
    if not html_files:
        print("Error: No HTML file found in resources/app directory.")
        sys.exit(1)

    source_file = html_files[0]
    try:
        source_file.rename(index_file)
        print(f"Renamed '{source_file.name}' to 'index.html'.")
    except OSError as e:
        print(f"Error: Could not rename '{source_file.name}' to 'index.html': {e}")
        sys.exit(1)


def extract_title_from_html(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    tree = html.fromstring(content)
    title_elements = tree.xpath("//title/text()")
    if not title_elements:
        return None
    return title_elements[0].strip()


def sanitize_name(title):
    name = re.sub(r"[^\-a-zA-Z ]", "", title)
    name = name.strip()
    name = name.replace(" ", "-")
    return name.lower()


def preview_game(name_game):
    html_file = resource_path("resources/app/index.html")
    icon_app_game = determine_app_icon()

    width, height = 482, 440

    try:
        screen = webview.screens[0]
        x = (screen.width - width) // 2
        y = (screen.height - height) // 2
    except Exception:
        x, y = None, None

    webview.create_window(name_game, html_file, width=width, height=height, x=x, y=y)
    webview.start(icon=icon_app_game, http_server=True)


def run_build():
    if sys.platform == "win32":
        subprocess.run(["build.bat"], shell=True)
    else:
        subprocess.run(["build.sh"])


def main():
    ensure_index_html()

    html_file = resource_path("resources/app/index.html")
    name_game_app = resource_path("name-project.txt")
    name_game_app_alt = resource_path("name-project-page.txt")

    title = extract_title_from_html(html_file)
    if not title:
        print("Error: Could not find a <title> in index.html")
        sys.exit(1)

    project_name = sanitize_name(title)
    if not project_name:
        print("Error: Project name is empty after sanitization.")
        sys.exit(1)

    with open(name_game_app, "w", encoding="utf-8") as file:
        file.write(project_name)

    title_alt = extract_title_from_html(html_file)
    if not title_alt:
        print("Error: Could not find a <title> in index.html")
        sys.exit(1)

    with open(name_game_app_alt, "w", encoding="utf-8") as file:
        file.write(title_alt)

    while True:
        choice = (
            input(
                'Type "test" to preview or "compile" to convert to EXE (or "exit" to quit): '
            )
            .strip()
            .lower()
        )

        if choice == "test":
            preview_game(title_alt)
        elif choice == "compile":
            run_build()
        elif choice == "exit":
            break
        else:
            print("Invalid user's input.")
            continue


if __name__ == "__main__":
    main()
