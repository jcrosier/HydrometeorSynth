from math import sqrt

import numpy as np
import pytest
from scipy.spatial.distance import pdist
from trimesh import Trimesh

from hydrometeorsynth.geometry.hexagonal_plate import HexagonalPlate

CANONICAL_RADIUS = 1.0
CANONICAL_DIAMETER = 2.0 * CANONICAL_RADIUS


@pytest.mark.parametrize("aspect_ratio", [0.2, 0.5, 1.2])
def test_hex_plate_dmax(aspect_ratio):
    hex_plate = HexagonalPlate(aspect_ratio)
    thickness = aspect_ratio * CANONICAL_DIAMETER
    expected = sqrt(CANONICAL_DIAMETER**2 + thickness**2)
    assert hex_plate.dmax == pytest.approx(expected, rel=1e-12)


@pytest.mark.parametrize("value", ["aspect_ratio", ["aspect_ratio"], ["1.2"]])
def test_hex_plate_aspect_ratio_type_error(value):
    with pytest.raises(TypeError):
        HexagonalPlate(value)


@pytest.mark.parametrize(
    "value", [0.0, -1.0, float("nan"), float("inf"), float("-inf")]
)
def test_hex_plate_aspect_ratio_value_error(value):
    with pytest.raises(ValueError):
        HexagonalPlate(value)


def test_hex_plate_aspect_ratio_type():
    hex_plate = HexagonalPlate(1)
    assert isinstance(hex_plate.aspect_ratio, float)
    assert hex_plate.aspect_ratio == 1.0


def test_hex_plate_default_aspect_ratio():
    hex_plate = HexagonalPlate()
    assert hex_plate.aspect_ratio == 0.1


def test_hex_plate_aspect_ratio_invalidation():
    hex_plate = HexagonalPlate(0.2)
    _ = hex_plate.mesh
    assert hex_plate._mesh is not None
    hex_plate.aspect_ratio = 1.2
    assert hex_plate._mesh is None


def test_hex_plate_mesh_type():
    hex_plate = HexagonalPlate()
    assert isinstance(hex_plate.mesh, Trimesh)


def test_hex_plate_mesh_is_cached():
    hex_plate = HexagonalPlate()
    mesh1 = hex_plate.mesh
    mesh2 = hex_plate.mesh
    assert mesh1 is mesh2


def test_hex_plate_mesh_centroid():
    hex_plate = HexagonalPlate(0.2)
    assert hex_plate.mesh.centroid == pytest.approx([0, 0, 0])


@pytest.mark.parametrize("aspect_ratio", [0.2, 1.2, 2.2])
def test_hex_plate_mesh_extents(aspect_ratio):
    hex_plate = HexagonalPlate(aspect_ratio)
    thickness = aspect_ratio * CANONICAL_DIAMETER
    assert hex_plate.mesh.extents[2] == pytest.approx(thickness)


def test_hex_plate_vertices_have_unit_circumradius():
    hex_plate = HexagonalPlate()
    xy = hex_plate.mesh.vertices[:, :2]
    radii = np.linalg.norm(xy, axis=1)
    assert np.max(radii) == pytest.approx(CANONICAL_RADIUS)


@pytest.mark.parametrize("aspect_ratio", [0.2, 1.2])
def test_hex_plate_analytical_volume(aspect_ratio):
    hex_plate = HexagonalPlate(aspect_ratio)
    thickness = aspect_ratio * CANONICAL_DIAMETER
    analytical_volume = thickness * 3 * sqrt(3) * CANONICAL_RADIUS**2 / 2
    assert analytical_volume == pytest.approx(hex_plate.volume)


@pytest.mark.parametrize("aspect_ratio", [0.2, 1.2])
def test_hex_plate_analytical_surface_area(aspect_ratio):
    hex_plate = HexagonalPlate(aspect_ratio)
    thickness = aspect_ratio * CANONICAL_DIAMETER
    analytical_surface_area = (6 * CANONICAL_RADIUS * thickness) + (
        3 * sqrt(3) * CANONICAL_RADIUS**2
    )
    assert analytical_surface_area == pytest.approx(hex_plate.surface_area)


@pytest.mark.parametrize("aspect_ratio", [0.2, 1.2])
def test_hex_plate_analytical_vs_mesh_dmax(aspect_ratio):
    hex_plate = HexagonalPlate(aspect_ratio)
    hull = hex_plate.mesh.convex_hull
    mesh_dmax = pdist(hull.vertices).max()
    assert mesh_dmax == pytest.approx(hex_plate.dmax, rel=1e-3)
