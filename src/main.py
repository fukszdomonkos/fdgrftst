#!/usr/bin/env python3
import argparse
import importlib
import pkgutil
import sys
import types

import src
from src.base import BaseApp


def import_submodules(package: types.ModuleType) -> None:
    """Import all submodules of a package."""
    if not hasattr(package, "__path__"):
        raise ValueError(f"The module {package.__name__} is not a package.")
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{package.__name__}.{module_name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an application")
    parser.add_argument("--application", type=str, required=True, help="Name of the application class")
    parser.add_argument("--screen_width", type=int, default=800, help="Width of the screen")
    parser.add_argument("--screen_height", type=int, default=450, help="Height of the screen")
    parser.add_argument("--window_title", type=str, help="Title of the window")
    parser.add_argument("--fps", type=int, default=60, help="Frames per second")
    parser.add_argument("--random_seed", type=int, default=186484546135, help="Random seed")
    parser.add_argument("--rendering", action="store_true", help="Enable rendering mode")
    parser.add_argument("--rendering_output_dir", type=str, default="output", help="Rendering output directory")
    parser.add_argument("--rendering_seconds", type=float, default=10.0, help="Rendering duration in seconds")

    args = parser.parse_args()

    # Set default title if not provided
    if not args.window_title:
        args.window_title = args.application

    # Import all submodules in the src package
    import_submodules(src)

    # Retrieve all subclasses of BaseApp
    available_apps = BaseApp.__subclasses__()
    matching_apps = [app for app in available_apps if app.__name__ == args.application]

    # Handle errors if no matching or multiple matching classes are found
    if not matching_apps:
        raise ValueError(f"Application '{args.application}' not found.")
    elif len(matching_apps) > 1:
        raise ValueError(f"Multiple applications with the name '{args.application}' found.")

    # Instantiate and run the selected application
    app_class = matching_apps[0]
    app_instance = app_class(
        screen_width=args.screen_width,
        screen_height=args.screen_height,
        window_title=args.window_title,
        fps=args.fps,
        random_seed=args.random_seed,
        rendering=args.rendering,
        rendering_output_dir=args.rendering_output_dir,
        rendering_seconds=args.rendering_seconds,
    )
    app_instance.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())
