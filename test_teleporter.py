import unittest
import lib.grid as grid
import lib.teleporter as teleporter
import lib.laser as laser

class TeleporterTest(unittest.TestCase):
    """
       Test class to ensure every teleportation-related features are working.
    """
    def setUp(self):
        self.grid_height = 3
        self.grid_width = 3
        self._laser_x = 1
        self._laser_y = 0
        self._laser_direction = '>'
        
    def test_random_teleportation(self):
        """
           Tests the exit data of a laser teleported at random between two
           teleporters.
        """
        items = self.build_teleporters([(1, 0), (0, 2), (2, 2)])
        _grid = self.build_grid(items)
        _laser = self.build_laser(_grid)
        exit_data = _grid.compute_laser_exit(_laser)
        self.assertTrue(exit_data == [(0, 3, '>')]
                        or exit_data == [(2, 3, '>')])
    
    def test_vanish(self):
        """
           Tests the exit data of a laser which encounters a lone teleporter.
        """
        items = self.build_teleporters([(1, 0)])
        _grid = self.build_grid(items)
        _laser = self.build_laser(_grid)
        exit_data = _grid.compute_laser_exit(_laser)
        self.assertEqual(exit_data, [(1, 0, '>')])
        
    def test_determinist_teleportation(self):
        """
           Tests the exit data of a laser which can exit from two different
           points.
        """
        items = self.build_teleporters([(1, 0), (0, 2), (2, 2)])
        _grid = self.build_grid(items)
        _laser = self.build_laser(_grid)
        exit_data = _grid.compute_all_laser_exits(_laser)
        self.assertTrue(exit_data == [(0, 3, '>'), (2, 3, '>')]
                        or exit_data == [(2, 3, '>'), (0, 3, '>')])
            
    def test_finite_teleportation(self):
        """
           Tests the finition of the computations when a laser may pass
           infinitely through the same mirrors without escaping the grid.
        """
        items = self.build_teleporters([(1, 0), (1, 1), (1, 2)])
        _grid = self.build_grid(items)
        _laser = self.build_laser(_grid)
        exit_data = _grid.compute_all_laser_exits(_laser)
        self.assertEqual(exit_data, [(1, 3, '>')])
        
    def build_teleporters(self, teleporters_coordinates):
        return [(xy[0], xy[1], teleporter.Teleporter(xy[0], xy[1])) for xy in
                teleporters_coordinates]
        
    def build_grid(self, items):
        return grid.Grid(self.grid_height, self.grid_width, items)
        
    def build_laser(self, _grid):
        return laser.Laser(self._laser_x, self._laser_y, self._laser_direction,
                           _grid)

if __name__ == '__main__':
    unittest.main()