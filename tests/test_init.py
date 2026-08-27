import importlib.metadata
import subprocess
import sys

import bcra_sdk


def test_version_no_empty():
    assert bcra_sdk.__version__


def test_version_matches_installed_distribution():
    dist = subprocess.run(
        [
            sys.executable,
            "-c",
            "import importlib.metadata as m; print(m.version('bcra-sdk'))",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert bcra_sdk.__version__ == dist.stdout.strip()


def test_version_fallback_when_not_installed(monkeypatch):
    import bcra_sdk

    def _not_found(pkg: str) -> str:
        from importlib.metadata import PackageNotFoundError

        raise PackageNotFoundError(pkg)

    monkeypatch.setattr(importlib.metadata, "version", _not_found)
    importlib.reload(bcra_sdk)
    assert bcra_sdk.__version__ == "0.0.0.dev"
    monkeypatch.undo()
    importlib.reload(bcra_sdk)
    assert bcra_sdk.__version__


def test_all_exports_public_api():
    assert set(bcra_sdk.__all__) == {
        "BCRAClient",
        "BCRAConnectionError",
        "BCRAEndpointVersionError",
        "BCRAError",
        "BCRAHTTPError",
        "BCRATimeoutError",
        "RetryPolicy",
    }
