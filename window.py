from pathlib import Path
import sys
import webview


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


def main():
    html_file = resource_path("resources/app/index.html")
    name_game_app_alt = resource_path("name-project-page.txt")
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
    webview.start(icon=icon_app_game, http_server=True)


if __name__ == "__main__":
    main()
