from math import sqrt
from hydrometeorsynth.geometry.cube import Cube


def test_cube_dmax():
    """Check the dmax for the canonical cube"""
    unit_cube = Cube()
    assert unit_cube.dmax == sqrt(3.0)


def test_cube_volume():
    """Check the volume for the canonical cube"""
    unit_cube = Cube()
    assert unit_cube.volume == 1.0


def test_cube_surface_area():
    """Check the surface area for the canonical cube"""
    unit_cube = Cube()
    assert unit_cube.surface_area == 6.0