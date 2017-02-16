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

    def test_piecewiselinear(self):
        t =    [[0.00, 0.000, 0.800],
                [0.04, 0.005, 0.650],
                [0.08, 0.013, 0.513],
                [0.12, 0.026, 0.400],
                [0.16, 0.040, 0.315],
                [0.20, 0.058, 0.250],
                [0.24, 0.078, 0.196],
                [0.28, 0.100, 0.150],
                [0.32, 0.126, 0.112],
                [0.36, 0.156, 0.082],
                [0.40, 0.187, 0.060],
                [0.44, 0.222, 0.040],
                [0.48, 0.260, 0.024],
                [0.52, 0.300, 0.012],
                [0.56, 0.348, 0.005],
                [0.60, 0.400, 0.000],
                [0.64, 0.450, 0.000],
                [0.68, 0.505, 0.000],
                [0.72, 0.562, 0.000],
                [0.76, 0.620, 0.000],
                [0.80, 0.680, 0.000],
                [0.84, 0.740, 0.000]]
        l = sunbeam.piecewiselinear(t)

        # f(0.00) = (0.000, 0.800)
        # f(0.10) = (0.020, 0.457)
        # f(0.30) = (0.113, 0.131)
        # f(0.50) = (0.280, 0.018)
        # f(0.70) = (0.533, 0.000)
        # f(0.90) = (0.740, 0.000)
        v1,v2 = l(0)
        self.assertClose(0.0, v1, 0.01)
        self.assertClose(0.8, v2, 0.01)
        v1,v2 = l(0.1)
        self.assertClose(0.02, v1, 0.01)
        self.assertClose(0.45, v2, 0.01)
        v1,v2 = l(0.3)
        self.assertClose(0.113, v1, 0.01)
        self.assertClose(0.131, v2, 0.01)
        v1,v2 = l(0.5)
        self.assertClose(0.280, v1, 0.01)
        self.assertClose(0.018, v2, 0.01)
        v1,v2 = l(0.7)
        self.assertClose(0.53, v1, 0.01)
        self.assertClose(0.00, v2, 0.01)
        v1,v2 = l(0.9)
        self.assertClose(0.74, v1, 0.01)
        self.assertClose(0.00, v2, 0.01)
