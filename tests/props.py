import unittest
import sunbeam

class TestProps(unittest.TestCase):
    spe3 = None

    def assertClose(self, expected, observed, epsilon=1e-18):
        diff = abs(expected - observed)
        if diff > epsilon:
            raise AssertionError('|%g - %g| = %g > %g' % (expected, observed, diff, epsilon))

    def setUp(self):
        if self.spe3 is None:
            self.spe3 = sunbeam.parse('spe3/SPE3CASE1.DATA')
        self.props = self.spe3.props()

    def test_repr(self):
        self.assertTrue('Eclipse3DProperties' in repr(self.props))

    def test_contains(self):
        p = self.props
        self.assertTrue('PORO'  in p)
        self.assertFalse('NONO' in p)
        self.assertFalse('PORV' in p)

    def test_getitem(self):
        p = self.props
        poro = p['PORO']
        self.assertEqual(324, len(poro))
        self.assertEqual(0.13, poro[0])
        self.assertTrue( 'PERMX' in p )
        px = p['PERMX']
        print(len(px))
        self.assertEqual(324, len(px))

    def test_regions(self):
        p = self.props
        reg = p.getRegions('SATNUM')
        self.assertEqual(0, len(reg))

    def test_permx_values(self):
        def md2si(md):
            """millidarcy->SI"""
            return md * 1e-3 * 9.869233e-13
        e3dp  = self.props
        grid  = self.spe3.grid()
        permx = e3dp['PERMX']
        print('set(PERMX) = %s' % set(permx))
        # 130mD, 40mD, 20mD, and 150mD, respectively, top to bottom
        darcys = {0:md2si(130), 1:md2si(40), 2:md2si(20), 3:md2si(150)}
        for i in range(grid.getNX()):
            for j in range(grid.getNY()):
                for k in range(grid.getNZ()):
                    g_idx = grid.globalIndex(i,j,k)
                    perm  = permx[g_idx]
                    darcy = darcys[k]
                    self.assertClose(darcy, perm)
