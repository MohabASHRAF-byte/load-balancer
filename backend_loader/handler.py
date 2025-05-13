from backend_loader.version1 import Version1
from backend_loader.version2 import Version2


def get_version_instance(name: str):
    versions = {
        "version1": Version1,
        "version2": Version2
    }

    version_class = versions.get(name.lower())
    if version_class is None:
        raise ValueError(f"Unsupported version: {name}")

    return version_class()
