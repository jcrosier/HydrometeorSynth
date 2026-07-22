from math import isfinite

MIN_ROTATION = 0.0
MAX_ROTATION = 360.0


class Orientation:
    """Represents the orientation of a particle."""

    def __init__(
        self,
        *,
        x_rotation: float = 0.0,
        y_rotation: float = 0.0,
        z_rotation: float = 0.0,
    ):
        self.x_rotation = x_rotation
        self.y_rotation = y_rotation
        self.z_rotation = z_rotation

    def __repr__(self) -> str:
        return (
            f"Orientation("
            f"x_rotation={self.x_rotation}, "
            f"y_rotation={self.y_rotation}, "
            f"z_rotation={self.z_rotation})"
        )

    def _validate_rotation(self, value: float | int, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be an int or float")
        if not isfinite(value):
            raise ValueError(f"{name} must be a real number")
        if not MIN_ROTATION <= value < MAX_ROTATION:
            raise ValueError(
                f"{name} must satisfy {MIN_ROTATION} <= {name} < {MAX_ROTATION}"
            )
        return float(value)

    @property
    def x_rotation(self) -> float:
        return self._x_rotation

    @x_rotation.setter
    def x_rotation(self, value: float | int):
        self._x_rotation = self._validate_rotation(value, "x_rotation")

    @property
    def y_rotation(self) -> float:
        return self._y_rotation

    @y_rotation.setter
    def y_rotation(self, value: float | int):
        self._y_rotation = self._validate_rotation(value, "y_rotation")

    @property
    def z_rotation(self) -> float:
        return self._z_rotation

    @z_rotation.setter
    def z_rotation(self, value: float | int):
        self._z_rotation = self._validate_rotation(value, "z_rotation")
