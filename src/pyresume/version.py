import importlib.metadata


def get_version() -> str:
    try:
        return importlib.metadata.version("pyresume")
    except importlib.metadata.PackageNotFoundError:
        return "0.0.0-unknown"


__version__ = f"v{get_version()}"
