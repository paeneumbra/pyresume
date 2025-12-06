import toml

from pyresume.settings import PROJECT_ROOT
from pyresume.version import __version__


class TestVersion:
    """Test version consistency across project"""

    def test_version_matches_pyproject_toml(self):
        """Verify package version matches pyproject.toml"""
        pyproject_path = PROJECT_ROOT / "pyproject.toml"

        assert pyproject_path.exists(), "pyproject.toml not found"

        with pyproject_path.open(encoding="utf-8") as toml_file:
            pyproject_data = toml.load(toml_file)

        project_version = pyproject_data["project"]["version"]

        assert __version__ == f"v{project_version}", (
            f"Version mismatch: package has {__version__}, "
            f"pyproject.toml has v{project_version}"
        )
