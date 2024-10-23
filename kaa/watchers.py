import os
import time

from .kaa_definition import KaaDefinition


class FileWatcher:
    def __init__(self) -> None:
        self.definition = KaaDefinition()

    def watch(self, callback):
        last_mtime = None
        path = self.definition.get_base_path()
        interval = self.definition.get_polling_interval()
        while True:
            curtent_mtime = max(
                os.path.getmtime(os.path.join(root, f))
                for root, _, files in os.walk(path)
                if self.__is_valid_directory(root)
                for f in files
                if self.__is_valid_file(f)
            )
            if last_mtime and curtent_mtime > last_mtime:
                print("Changes detected.")
                callback("restart")
            last_mtime = curtent_mtime
            time.sleep(interval)

    def __is_valid_directory(self, directory):
        # TODO: use inclusions and exclusions
        excluded_dirs = [
            "__pycache__",
            ".git",
            ".venv",
            "dist",
            "build",
            "tests",
            "docs",
        ]
        return not any(excluded in directory for excluded in excluded_dirs)

    def __is_valid_file(self, file):
        # TODO: use inclusions and exclusions
        excluded_files = ["*.pyc", "*.pyo", "*.pyd", "*.md"]
        if any(file.endswith(excluded) for excluded in excluded_files):
            return False
        allowed_files = ["py", "html", "yaml", "json"]
        valid_file = file.split(".")[-1] in allowed_files
        return valid_file and not file.startswith(".")


class KeyWatcher:
    def watch(self, callback):
        while True:
            a = input("")
            if "r" == a:
                callback("restart")
            if "q" == a:
                callback("quit")
            time.sleep(1)
