from __future__ import division

def interpolate(x, val_below, val_above):
    """0 <= x <= 1, val_below and val_above are tuples (v1,v2,v3,...) and
    (u1,u2,u3,...).

    Return value will be (x1,x2,x3,...) with xi being x-parts between (vi,ui).
    Note that vi and ui can be arbitrary numbers.

    """
    x_vals = []
    for i in range(len(val_below)):
        xp = x # in case we need to do x:=1-x below
        vi,ui = val_below[i], val_above[i]
        if ui < vi: # vi is above ui, flip sign and use x = 1 - x
            xp = 1 - x
            ui,vi = val_below[i], val_above[i]
        ran = ui-vi
        xi  = ran*xp + vi
        x_vals.append(xi)
    return tuple( x_vals )

def piecewiselinear(table):
    """A table is something like this:

       [[0.00, 0.000, 0.800],
        [0.08, 0.013, 0.513],
        [0.24, 0.078, 0.196],
        [0.40, 0.187, 0.060],
        [0.56, 0.348, 0.005],
        [0.72, 0.562, 0.000],
        [0.84, 0.740, 0.000],
        ]

    From this we will generate a function that takes the values in the first
    column to the values in the second column.

    Then we will return a function that is the piecewise linear interpolation
    (and extension) of this function.

    """
    fn = []
    key_min = table[0][0]
    key_max = table[-1][0]
    num_vals= len(table)
    for i in range(num_vals):
        row = table[i]
        fn.append((row[0], tuple(row[1:])))
    def linear(x):
        if x <= key_min:
            return fn[0][1]
        if x >= key_max:
            return fn[-1][1]
        for i in range(num_vals):
            if fn[i][0] >= x:
                key_below = fn[i-1][0]
                val_below = fn[i-1][1]
                key_above = fn[i  ][0]
                val_above = fn[i  ][1]
                xp        = x - key_below # x'
                ran       = key_above - key_below # range
                return interpolate(xp/ran, val_below, val_above)



    return linear
