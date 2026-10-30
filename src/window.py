from pathlib import Path
import json
import sys
import webview


def resource_path(relative_path):
    try:
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path.cwd()
    return str(base_path / relative_path)

def determine_icon():
    if sys.platform == "win32":
        return resource_path("icons/icon.ico")
    elif sys.platform == "darwin":
        return resource_path("icons/icon.icns")
    else:
        return resource_path("resources/app/icon.png")

def main():
    html_file = resource_path("resources/app/index.html")
    name_app = resource_path("resources/app/package.json")
    icon_app = determine_icon()

    with open(name_app, "r", encoding="utf-8") as file:
        data = json.load(file)
        name_game = data["name"]

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
    webview.start(icon=icon_app, http_server=True)


if __name__ == "__main__":
    main()
