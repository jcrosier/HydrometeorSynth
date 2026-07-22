import pytest

from hydrometeorsynth.orientation import Orientation

DEFAULT_ROTATION = 0.0
MIN_ROTATION = 0.0
MAX_ROTATION = 360.0


def test_orientation_init_default():
    orientation = Orientation()
    assert isinstance(orientation, Orientation)
    assert isinstance(orientation.x_rotation, float)
    assert isinstance(orientation.y_rotation, float)
    assert isinstance(orientation.z_rotation, float)
    assert orientation.x_rotation == pytest.approx(DEFAULT_ROTATION)
    assert orientation.y_rotation == pytest.approx(DEFAULT_ROTATION)
    assert orientation.z_rotation == pytest.approx(DEFAULT_ROTATION)


def test_orientation_init_valid():
    orientation = Orientation(x_rotation=10.0, y_rotation=20.0, z_rotation=30.0)
    assert orientation.x_rotation == pytest.approx(10.0)
    assert orientation.y_rotation == pytest.approx(20.0)
    assert orientation.z_rotation == pytest.approx(30.0)


def test_orientation_repr():
    orientation = Orientation(x_rotation=10.0, y_rotation=20.0, z_rotation=30.0)
    assert repr(orientation) == (
        "Orientation(x_rotation=10.0, y_rotation=20.0, z_rotation=30.0)"
    )


def test_orientation_init_invalid_x_rotation():
    with pytest.raises(ValueError):
        Orientation(x_rotation=360.0)


def test_orientation_init_invalid_y_rotation():
    with pytest.raises(ValueError):
        Orientation(y_rotation=360.0)


def test_orientation_init_invalid_z_rotation():
    with pytest.raises(ValueError):
        Orientation(z_rotation=360.0)


@pytest.mark.parametrize("name", ["x_rotation", "y_rotation", "z_rotation"])
def test_orientation_setter(name):
    orientation = Orientation()
    setattr(orientation, name, 90.0)
    assert getattr(orientation, name) == pytest.approx(90.0)


@pytest.mark.parametrize("name", ["x_rotation", "y_rotation", "z_rotation"])
@pytest.mark.parametrize("value", ["input", "90.0", [10.0], bool(True)])
def test_orientation_param_type_check(name, value):
    orientation = Orientation()
    with pytest.raises(TypeError):
        setattr(orientation, name, value)


@pytest.mark.parametrize("name", ["x_rotation", "y_rotation", "z_rotation"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_orientation_param_not_finite(name, value):
    orientation = Orientation()
    with pytest.raises(ValueError):
        setattr(orientation, name, value)


@pytest.mark.parametrize("name", ["x_rotation", "y_rotation", "z_rotation"])
@pytest.mark.parametrize("value", [MIN_ROTATION - 0.1, MAX_ROTATION])
def test_orientation_param_limit_reject(name, value):
    orientation = Orientation()
    with pytest.raises(ValueError):
        setattr(orientation, name, value)


@pytest.mark.parametrize("name", ["x_rotation", "y_rotation", "z_rotation"])
@pytest.mark.parametrize("value", [MIN_ROTATION, MAX_ROTATION - 0.01])
def test_orientation_param_limit_accept(name, value):
    orientation = Orientation()
    setattr(orientation, name, value)
    assert getattr(orientation, name) == pytest.approx(value)
