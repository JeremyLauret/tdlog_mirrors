import unittest
import lib.grid as grid
import lib.mirrors as mirrors
import lib.laser as laser

class MirrorsTest(unittest.TestCase):
    """
       Test class to ensure every mirrors-related features are working.
    """
    def setUp(self):
        self.grid_height = 3
        self.grid_width = 3
        
    def test_backslash_mirrors(self):
        """
           Tests the exit data of two lasers reflected by a backslash mirror.
        """
        data_left, data_bottom, data_right, data_top = self.compute_data('\\')
        self.assertEqual(data_left[0], (3, 1, 'v'))
        self.assertEqual(data_top[0], (1, 3, '>'))
    
    def test_dash_mirrors(self):
        """
           Tests the exit data of two lasers reflected by a dash mirror.
        """
        data_left, data_bottom, data_right, data_top = self.compute_data('-')
        self.assertEqual(data_left[0], (1, 3, '>'))
        self.assertEqual(data_top[0], (-1, 1, '^'))
        
    def test_empty_mirrors(self):
        """
           Tests the exit data of a laser crossing an empty grid.
        """
        data_left, data_bottom, data_right, data_top = self.compute_data(' ')
        self.assertEqual(data_left[0], (1, 3, '>'))
        
    def test_hash_mirrors(self):
        """
           Tests the exit data of two lasers reflected by a hash mirror.
        """
        data_left, data_bottom, data_right, data_top = self.compute_data('#')
        self.assertEqual(data_left[0], (1, -1, '<'))
        self.assertEqual(data_top[0], (-1, 1, '^'))
        
    def test_pipe_mirrors(self):
        """
           Tests the exit data of two lasers reflected by a pipe mirror.
        """
        data_left, data_bottom, data_right, data_top = self.compute_data('|')
        self.assertEqual(data_left[0], (1, -1, '<'))
        self.assertEqual(data_top[0], (3, 1, 'v'))
        
    def test_slash_mirrors(self):
        """
           Tests the exit data of a laser reflected by two backslash mirrors.
        """
        data_left, data_bottom, data_right, data_top = self.compute_data('/')
        self.assertEqual(data_left[0], (-1, 1, '^'))
        self.assertEqual(data_bottom[0], (1, 3, '>'))
        
    def build_mirror(self, type):
        if type == '\\' :
            return [(1, 1, mirrors.BackslashMirror())]
        if type == '/' :
            return [(1, 1, mirrors.SlashMirror())]
        if type == '#' :
            return [(1, 1, mirrors.HashMirror())]
        if type == '|' :
            return [(1, 1, mirrors.PipeMirror())]
        if type == '-' :
            return [(1, 1, mirrors.DashMirror())]
        return []    # Useful to test empty mirrors
        
    def build_grid(self, items):
        return grid.Grid(self.grid_height, self.grid_width, items)
        
    def build_left_laser(self, _grid):
        return laser.Laser(1, 0, '>', _grid)
        
    def build_bottom_laser(self, _grid):
        return laser.Laser(self.grid_height - 1, 1, '^', _grid)
        
    def build_right_laser(self, _grid):
        return laser.Laser(1, self.grid_width - 1, '<', _grid)
        
    def build_top_laser(self, _grid):
        return laser.Laser(0, 1, 'v', _grid)
        
    def compute_data(self, mirror_type):
        items = self.build_mirror(mirror_type)
        _grid = self.build_grid(items)
        left_laser = self.build_left_laser(_grid)
        bottom_laser = self.build_bottom_laser(_grid)
        right_laser = self.build_right_laser(_grid)
        top_laser = self.build_top_laser(_grid)
        data_left = _grid.compute_laser_exit(left_laser)
        data_bottom = _grid.compute_laser_exit(bottom_laser)
        data_right = _grid.compute_laser_exit(right_laser)
        data_top = _grid.compute_laser_exit(top_laser)
        return (data_left, data_bottom, data_right, data_top)

if __name__ == '__main__':
    unittest.main()