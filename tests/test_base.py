import pytest

from bcra_sdk._base import Resource
from bcra_sdk.exceptions import BCRAEndpointVersionError


class _FakeModel:
    @classmethod
    def from_dict(cls, data):
        return data


def test_versions_default_single_version():
    resource = Resource(object())
    resource._register_version("get_foo", "1.0", path="/foo", model=_FakeModel)
    assert resource.versions("get_foo") == {"1.0": {"deprecated": False}}


def test_versions_multiple_with_deprecated():
    resource = Resource(object())
    resource._register_version(
        "get_foo", "1.0", path="/v1/foo", model=_FakeModel, deprecated=True
    )
    resource._register_version("get_foo", "2.0", path="/v2/foo", model=_FakeModel)
    assert resource.versions("get_foo") == {
        "1.0": {"deprecated": True},
        "2.0": {"deprecated": False},
    }


def test_resolve_version_defaults_to_latest():
    resource = Resource(object())
    resource._register_version("get_foo", "1.0", path="/v1/foo", model=_FakeModel)
    resource._register_version("get_foo", "2.0", path="/v2/foo", model=_FakeModel)
    spec = resource._resolve_version("get_foo", None)
    assert spec.path == "/v2/foo"


def test_resolve_version_explicit():
    resource = Resource(object())
    resource._register_version("get_foo", "1.0", path="/v1/foo", model=_FakeModel)
    resource._register_version("get_foo", "2.0", path="/v2/foo", model=_FakeModel)
    spec = resource._resolve_version("get_foo", "1.0")
    assert spec.path == "/v1/foo"


def test_resolve_version_unknown_raises():
    resource = Resource(object())
    resource._register_version("get_foo", "1.0", path="/foo", model=_FakeModel)
    with pytest.raises(BCRAEndpointVersionError) as exc_info:
        resource._resolve_version("get_foo", "9.0")
    assert "no tiene version '9.0'" in str(exc_info.value)
    assert "1.0" in str(exc_info.value)


def test_resolve_version_no_versions_raises():
    resource = Resource(object())
    with pytest.raises(BCRAEndpointVersionError):
        resource._resolve_version("get_foo", None)


def test_resolve_version_deprecated_warns():
    resource = Resource(object())
    resource._register_version(
        "get_foo", "1.0", path="/foo", model=_FakeModel, deprecated=True
    )
    with pytest.deprecated_call():
        resource._resolve_version("get_foo", "1.0")
