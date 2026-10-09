import numpy as np

class PointCoordinateGrid:
        
    def __init__(self, point_coordinates: np.ndarray[np.number]) -> None:
        if np.size(point_coordinates) == 0:
            raise ValueError("Cannot pass None or an empty array")
        self._point_coordinates: np.ndarray = np.copy(point_coordinates)
        self._x_min: np.float_ | None = None
        self._x_max: np.float_ | None = None
        self._y_min: np.float_ | None = None
        self._y_max: np.float_ | None = None
        self._z_min: np.float_ | None = None
        self._z_max: np.float_ | None = None
        self._x_step: np.float_ | None = None
        self._y_step: np.float_ | None = None
        self._z_step: np.float_ | None = None
        self.__parse_coordinates()

    def __eq__(self, value: object) -> bool:
        if type(self) != type(value):  
            return False
        if np.ndim(self._point_coordinates) != np.ndim(value._point_coordinates) or not np.allclose(self._point_coordinates, value._point_coordinates):
            return False
        # check auxiliary attributes as well
        if self._x_min != value._x_min or self._x_max != value._x_max or \
           self._y_min != value._y_min or self._y_max != value._y_max or \
           self._z_min != value._z_min or self._z_max != value._z_max:
            return False
        return True

    def __parse_coordinates(self) -> None:
        """Parse the point coordinates the user put in. Generates x_min, x_max, y_min, y_max, z_min, z_max, and x_step, y_step, z_step. This function assumes the positions the user passes into the SNRMapper class are already on a rectangular grid (but does not have to form a full rectangular region).

        Raises:
            ValueError: error if there exists duplicates in point_coordinates
        """
        coordinate_unique, coordinate_count = np.unique(self._point_coordinates, axis=0, return_counts=True)
        if np.any(coordinate_count > 1):
            raise ValueError("Duplicates in coordinates found. The duplicates are\n{}".format(coordinate_unique[coordinate_count > 1]))
        self._x_min, self._y_min, self._z_min = np.min(self._point_coordinates, 0)
        self._x_max, self._y_max, self._z_max = np.max(self._point_coordinates, 0)
        delta_xyz = np.abs(np.diff(self._point_coordinates, axis=0))
        delta_x_with_0, delta_y_with_0, delta_z_with_0 = delta_xyz.T
        delta_x_without_0: np.ndarray = delta_x_with_0[np.nonzero(delta_x_with_0)]
        delta_y_without_0: np.ndarray = delta_y_with_0[np.nonzero(delta_y_with_0)]
        delta_z_without_0: np.ndarray = delta_z_with_0[np.nonzero(delta_z_with_0)]
        self._x_step, self._y_step, self._z_step = 0.0, 0.0, 0.0
        if delta_x_without_0.size != 0:
            self._x_step = delta_x_without_0.min()
        if delta_y_without_0.size != 0:
            self._y_step = delta_y_without_0.min()
        if delta_z_without_0.size != 0:
            self._z_step = delta_z_without_0.min()

    def find_nearest_point(self, point_xyz: np.ndarray[np.number]) -> tuple[np.integer, np.ndarray]:
        """Find the point nearest to point_xyz among an array of point coordinates. Returns the array index of the point nearest to point_xyz, and the nearest point itself. 

        Args:
            point_xyz (np.ndarray[np.number]): the coordinates of a point. It must have shape (3,) or (1, 3) and contain only real numbers.

        Returns:
            tuple[np.integer, np.ndarray]: the first element is the array index of the point nearest to point_xyz. The second element is the nearest point itself.
        """
        if not ((np.ndim(point_xyz) == 1 and np.size(point_xyz) == 3) or (np.ndim(point_xyz) == 2 and np.shape(point_xyz) == (1, 3))):
            raise ValueError("point_xyz must be an array of size (3,) or (1, 3)")
        if point_xyz.dtype == np.complexfloating:
            raise ValueError("array and point_xyz must contain only real numbers")
        p_xyz: np.ndarray = np.copy(point_xyz)
        if np.ndim(point_xyz) == 1:
            p_xyz = point_xyz[np.newaxis, :]
        dist_sq = np.sum((self._point_coordinates - p_xyz) ** 2, axis=1)
        m: np.integer = np.abs(dist_sq).argmin()
        point_at_m: np.ndarray[np.number] = np.copy(self._point_coordinates[m, ...])
        return m, point_at_m