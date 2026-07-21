import pytest

from hydrometeorsynth.geometry.cube import Cube
from hydrometeorsynth.particle import Particle

MIN_DMAX = 0.01
MAX_DMAX = 100.0

MIN_DENSITY = 100.0
MAX_DENSITY = 1500.0


def test_particle_initialises_properties():
    cube = Cube()
    density = 917.0
    dmax = 2.5
    test_particle = Particle(cube, dmax, density)
    assert isinstance(test_particle, Particle)
    assert test_particle.geometry is cube
    assert test_particle.dmax == dmax
    assert test_particle.density == density
    assert test_particle.orientation is None


@pytest.mark.parametrize("geometry", [1, 1.0, "sphere"])
def test_particle_geometry_type_validation(geometry):
    with pytest.raises(TypeError):
        Particle(geometry, 1.0, 1000.0)


def test_particle_geometry_setter():
    cube1 = Cube()
    cube2 = Cube()
    particle = Particle(cube1, 1.0, 1000.0)
    assert particle.geometry is cube1
    particle.geometry = cube2
    assert particle.geometry is cube2


@pytest.mark.parametrize("geometry", [1, 1.0, "sphere"])
def test_particle_geometry_setter_type_validation(geometry):
    particle = Particle(Cube(), 1.0, 1000.0)
    with pytest.raises(TypeError):
        particle.geometry = geometry


@pytest.mark.parametrize("dmax_val", [MIN_DMAX * 0.9, MAX_DMAX * 1.1])
def test_particle_dmax_range_validation(dmax_val):
    with pytest.raises(ValueError):
        Particle(Cube(), dmax_val, 1000.0)


@pytest.mark.parametrize("dmax_val", [float("nan"), float("inf"), float("-inf")])
def test_particle_dmax_requires_finite_value(dmax_val):
    with pytest.raises(ValueError):
        Particle(Cube(), dmax_val, 1000.0)


@pytest.mark.parametrize("dmax_val", [MIN_DMAX * 0.9, MAX_DMAX * 1.1])
def test_particle_dmax_setter_range_validation(dmax_val):
    test_particle = Particle(Cube(), 1.0, 1000.0)
    with pytest.raises(ValueError):
        test_particle.dmax = dmax_val


@pytest.mark.parametrize("dmax_val", [float("nan"), float("inf"), float("-inf")])
def test_particle_dmax_setter_requires_finite_value(dmax_val):
    test_particle = Particle(Cube(), 1.0, 1000.0)
    with pytest.raises(ValueError):
        test_particle.dmax = dmax_val


@pytest.mark.parametrize("dmax_val", ["dmax", "1.0", [2]])
def test_particle_dmax_setter_type_validation(dmax_val):
    particle = Particle(Cube(), 1.0, 1000.0)

    with pytest.raises(TypeError):
        particle.dmax = dmax_val


@pytest.mark.parametrize("dmax_val", ["dmax", "1.0", [2]])
def test_particle_dmax_type_validation(dmax_val):
    with pytest.raises(TypeError):
        Particle(Cube(), dmax_val, 1000.0)


def test_particle_dmax_can_be_modified():
    dmax_v1 = 1.0
    dmax_v2 = 2.0
    test_particle = Particle(Cube(), dmax_v1, 1000.0)
    assert test_particle.dmax == dmax_v1
    test_particle.dmax = dmax_v2
    assert test_particle.dmax == dmax_v2


@pytest.mark.parametrize("density_val", [MIN_DENSITY * 0.9, MAX_DENSITY * 1.1])
def test_particle_density_range_validation(density_val):
    with pytest.raises(ValueError):
        Particle(Cube(), 1.0, density_val)


@pytest.mark.parametrize("density_val", [float("nan"), float("inf"), float("-inf")])
def test_particle_density_requires_finite_value(density_val):
    with pytest.raises(ValueError):
        Particle(Cube(), 1.0, density_val)


@pytest.mark.parametrize("density_val", ["density_val", "1.0", [2]])
def test_particle_density_type_validation(density_val):
    with pytest.raises(TypeError):
        Particle(Cube(), 1.0, density_val)


def test_particle_density_can_be_modified():
    density_v1 = 950.0
    density_v2 = 1250.0
    test_particle = Particle(Cube(), 1.0, density_v1)
    assert test_particle.density == density_v1
    test_particle.density = density_v2
    assert test_particle.density == density_v2


@pytest.mark.parametrize("density_val", [MIN_DENSITY * 0.9, MAX_DENSITY * 1.1])
def test_particle_density_setter_range_validation(density_val):
    particle = Particle(Cube(), 1.0, 1000.0)
    with pytest.raises(ValueError):
        particle.density = density_val


@pytest.mark.parametrize("density_val", [float("nan"), float("inf"), float("-inf")])
def test_particle_density_setter_requires_finite_value(density_val):
    particle = Particle(Cube(), 1.0, 1000.0)
    with pytest.raises(ValueError):
        particle.density = density_val


@pytest.mark.parametrize("density_val", ["density", "1.0", [2]])
def test_particle_density_setter_type_validation(density_val):
    particle = Particle(Cube(), 1.0, 1000.0)

    with pytest.raises(TypeError):
        particle.density = density_val


def test_particle_orientation_defaults_to_none():
    particle = Particle(Cube(), 1.0, 1000.0)
    assert particle.orientation is None


def test_particle_orientation_can_be_assigned():
    particle = Particle(Cube(), 1.0, 1000.0)
    marker = object()
    particle.orientation = marker
    assert particle.orientation is marker
