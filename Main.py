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
        return resource_path("assets/icon.ico")
    elif sys.platform == "darwin":
        return resource_path("assets/icon.icns")
    else:
        return resource_path("assets/icon.png")


def extract_title_from_html(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    tree = html.fromstring(content)
    title_elements = tree.xpath("//title/text()")

    if not title_elements:
        return None

    return title_elements[0].strip()


def sanitize_name(title):
    name = re.sub(r"\d+", "", title)
    name = name.lower()
    name = re.sub(r"\s+", "-", name)
    name = re.sub(r"-+", "-", name)
    name = name.strip("-")
    return name


def preview_game():
    html_file = resource_path("assets/index.html")
    name_game_app_alt = resource_path("assets/name-project-page.txt")
    icon_app_game = determine_app_icon()

    with open(name_game_app_alt, "r", encoding="utf-8") as file:
        name_game = file.read()

    width, height = 482, 440

    try:
        screen = webview.screens[0]
        x = (screen.width - width) // 2
        y = (screen.height - height) // 2
    except Exception:
        x, y = None, None

    window = webview.create_window(
        name_game, html_file, width=width, height=height, x=x, y=y
    )
    webview.start(http_server=True, icon=icon_app_game)


def main():
    html_file = resource_path("assets/index.html")
    name_game_app = resource_path("assets/name-project.txt")
    name_game_app_alt = resource_path("assets/name-project-page.txt")

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

    choice = (
        input('Type "test" to preview or "compile" to convert to EXE: ').strip().lower()
    )

    if choice == "test":
        preview_game()
    elif choice == "compile":
        if sys.platform == "win32":
            subprocess.run(["build.bat"], shell=True)
        else:
            subprocess.run(["build.sh"])
    else:
        print("Invalid user's input.")
        sys.exit(1)


if __name__ == "__main__":
    main()
