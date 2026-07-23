import pytest

from hydrometeorsynth.position import Position

DEFAULT_POSITION = 0.0


def test_position_init_default():
    position = Position()
    assert isinstance(position, Position)


@pytest.mark.parametrize("name", ["x", "y", "z"])
def test_position_default_values(name):
    position = Position()
    value = getattr(position, name)
    assert isinstance(value, float)
    assert value == pytest.approx(DEFAULT_POSITION)


def test_position_init_valid():
    position = Position(x=10.0, y=20.0, z=30.0)
    assert position.x == pytest.approx(10.0)
    assert position.y == pytest.approx(20.0)
    assert position.z == pytest.approx(30.0)


@pytest.mark.parametrize("name", ["x", "y", "z"])
@pytest.mark.parametrize("value", ["input", "90.0", [10.0], bool(True)])
def test_position_init_type_check(name, value):
    kwargs = {"x": DEFAULT_POSITION, "y": DEFAULT_POSITION, "z": DEFAULT_POSITION}
    kwargs[name] = value
    with pytest.raises(TypeError):
        Position(**kwargs)


@pytest.mark.parametrize("name", ["x", "y", "z"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_position_init_not_finite(name, value):
    kwargs = {"x": DEFAULT_POSITION, "y": DEFAULT_POSITION, "z": DEFAULT_POSITION}
    kwargs[name] = value
    with pytest.raises(ValueError):
        Position(**kwargs)


def test_position_repr():
    position = Position(x=10.0, y=20.0, z=30.0)
    assert repr(position) == ("Position(x=10.0, y=20.0, z=30.0)")


@pytest.mark.parametrize("name", ["x", "y", "z"])
def test_position_setter(name):
    position = Position()
    setattr(position, name, 90.0)
    assert getattr(position, name) == pytest.approx(90.0)


@pytest.mark.parametrize("name", ["x", "y", "z"])
@pytest.mark.parametrize("value", ["input", "90.0", [10.0], bool(True)])
def test_position_param_type_check(name, value):
    position = Position()
    with pytest.raises(TypeError):
        setattr(position, name, value)


@pytest.mark.parametrize("name", ["x", "y", "z"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_position_param_not_finite(name, value):
    position = Position()
    with pytest.raises(ValueError):
        setattr(position, name, value)
