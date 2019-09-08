from random import randint
import numpy as np
from glumpy import app, gloo, gl, glm, transforms


def drawStrip(xstart, ystart, xstop, dx, dy):
    n = int ((xstop - xstart) / dx)
    numvertices = n * 6
    vertices = [[0.0, 0.0] for v in range(numvertices)]
    a = xstart
    ytop = ystart
    ybot = ystart - dy

    count = count = 0
    for i in range(n):
        b = a + dx
        vertices[count + 0][0] = a
        vertices[count + 0][1] = ytop
        vertices[count + 1][0] = a
        vertices[count + 1][1] = ybot
        vertices[count + 2][0] = b
        vertices[count + 2][1] = ytop
        vertices[count + 3][0] = b
        vertices[count + 3][1] = ytop
        vertices[count + 4][0] = a
        vertices[count + 4][1] = ybot
        vertices[count + 5][0] = b
        vertices[count + 5][1] = ybot
        count = count + 6
        a = b
    return vertices

def upd(y, deltay, xl, xr, lnudge, rnudge):
    return y - deltay, (xl + lnudge, xr - rnudge)

def drawVarBlock(ystart, xstart, xstop, deltax, deltay, nudges):
    vertices = []
    xran = (xstart, xstop)
    for nudgepair in nudges:
        vertices = vertices + drawStrip(xran[0], ystart, xran[1], deltax, deltay)
        ystart, xran = upd(ystart, deltay, xran[0], xran[1], nudgepair[0], nudgepair[1])
    return vertices

def eucdist(x0, y0, x1, y1):
    return pow(pow(x0 - x1, 2) + pow(y0 - y1, 2), 0.5)

def gradiantOpacity(vertices, source):
    dists = np.array([eucdist(source[0], source[1], v[0], v[1]) for v in vertices])
    dists = pow(dists, 10)
    dists = (dists - np.min(dists))/np.ptp(dists)
    return dists


vertex = """
    attribute vec2 position;
    attribute vec4 color;
    varying vec4 v_color;
    void main(){
        gl_Position = vec4(position, 0.0, 1.0);
        v_color = color;
    } """

vertex_m = """
    uniform mat4   model;         // Model matrix
    uniform mat4   view;          // View matrix
    uniform mat4   projection;    // Projection matrix
    attribute vec2 position;      // Vertex position
    void main()
    {
        gl_Position = model * vec4(position, 0.0, 1.0);
    }
    """



fragment_uni = """
    uniform vec4 color;
        void main() { gl_FragColor = color; } """

fragment_var = """
    varying vec4 v_color;
    void main() { gl_FragColor = v_color; } """

# Create a window with a valid GL context
window = app.Window()

# Colors
sand = np.array((245, 240, 188)) / 255
light_green = np.array((171, 191, 157)) /255

bldgs  = [ np.array((250, 250, 242)) / 255,
         ]

greens = [ np.array((138, 168, 146)) / 255,
           np.array((171, 191, 157)) / 255,
           np.array((122, 145, 128)) / 255,
           np.array((171, 194, 177)) / 255,
           np.array(( 90, 105, 94))  / 255,
           np.array((175, 199, 181)) / 255,
           np.array((141, 179, 151)) / 255,
         ]

sands =  [ np.array((212, 209, 178)) / 255,
           np.array((214, 208, 186)) / 255,
           np.array((237, 235, 225)) / 255,
           np.array((232, 227, 204)) / 255,
           np.array((222, 214, 204)) / 255,
           np.array((201, 196, 181)) / 255,
           np.array((201, 192, 167)) / 255,
         ]
waters = [ np.array((163, 201, 196)) / 255,
           np.array((99, 120, 117)) / 255,
           np.array((176, 191, 207)) / 255,
           np.array((142, 153, 163)) / 255,
           np.array((161, 183, 204)) / 255,
           np.array((100, 130, 128)) / 255,
           np.array((173, 192, 204)) / 255,
         ]

# Shapes
shapes = []

#########
# Water #
#########
deltay =  0.01
deltax =  0.01
ystart = 1.0
xstart = -1.0
xstop  =  1.0
nudges = [(0,0) for n in range(250)]
water_vertices = drawVarBlock(ystart, xstart, xstop, deltax, deltay, nudges)
water_colors              = [(*waters[randint(0, len(waters) - 1)], 0.6) for v in range(len(water_vertices))]
water = gloo.Program(vertex, fragment_var, count = len(water_vertices))
water["position"]         = water_vertices
water["color"]            = water_colors
shapes.append(water)


###############
# Ward Island #
###############

vertices = []
deltay =  0.01
deltax =  0.01
ystart =  0.84
xstart = -0.95
xstop  = 0.95

nudges = [ [0.0, 0.0],
           [0.01, 0.015],
           [0.012, 0.02],
           [0.014, 0.001],
           [0.008, 0.006 ],
           [0.00, 0.005 ],
           [0.004 ,0.004 ],
           [0.004 , 0.013],
           [0.006,0.01],
           [0.006,0.022],
           [0.004,0.011],
           [0.004,0.002],
           [0.0033,0.004],
           [0.0032,0.001],
           [0.0035,0.002],
           [0.003 ,0.009],
           [0.002 ,00.004],
           [0.002 ,0.004],
           [-0.0021 ,0.004],
           [0.0021 ,0.004],
           [0.0034 ,0.004],
           [-0.002 ,0.004],
           [-0.001 ,0.004],
           [-0.0001 ,0.004],
           [0.002 ,0.004],
           [0.004 ,0.004],
           [-0.001 ,0.004],
           [-0.002 ,0.004],
           [0.0032 ,0.004],
           [0.003 ,0.004],
           [0.0052 ,0.004],
           [0.003 ,0.004],
           [0.0013 ,-0.004],
           [0.0025,-0.004],
           [0.001,-0.004],
           [0.0023,-0.004],
           [0.0037,-0.004],
           [0.0036,0.0045],
           [-0.001,0.005],
           [0.0025,0.006],
           [-0.001,0.0045],
           [0.0034,0.003],
           [0.002,-0.003],
           [0.0013,0.0045],
           [-0.0016,0.006],
           [0.0025,0.0067],
           [0.0044,-0.004],
           [0.0053,-0.002],
           [0.0035,-0.001],
           [0.0028,-0.003],
           [0.0027,0.0046],
           [0.0035,0.0045],
           [0.0035,0.007],
           [0.0047,0.004],
           [0.0037,0.004],
           [0.0035,0.004],
           [0.0035,-0.004],
           [0.0035,-0.004],
           [0.0035,-0.004],
           [0.0033,-0.004],
           [0.0033,-0.004],
           [0.0033,0.0045],
           [0.0035,0.009],
           [0.0041,0.003],
           [-0.0001,0.0035],
           [-0.0005,-0.043],
           [0.0031,-0.003],
           [0.0035,0.0045],
           [0.0021,0.006],
           [0.0022,0.0067],
           [0.0021,-0.004],
           [-0.0005,-0.002],
           [0.0022,-0.001],
           [0.0035,-0.003],
           [0.0025,0.0076],
           [0.0035,0.0075],
           [0.0035,0.02],
           [0.0035,0.054],
           [0.0035,0.004],
           [0.0035,0.004],
           [0.0035,0.008],
           [0.0065,0.007],
           [0.0065,0.007],
           [0.0065,0.007],
           [0.0175,0.007],
           [0.0185,0.0075],
           [0.0085,0.007],
           [0.0195,0.007],
           [0.0035,0.0075],
           [0.0125,0.047],
           [0.0075,0.007],
           [0.0195,0.0075],
           [0.0205,0.006],
           [0.0125,0.0067],
           [0.0055,0.005],
           [0.0095,0.005],
           [0.0700,0.005],
           [0.065,0.005],
           [0.07,0.006],
           [0.013,0.0075],
           [0.011,-0.002],
           [-0.004,0.054],
           [0.01,0.004],
           [0.01,0.004],
           [0.04,0.008],
           [0.04,-0.003],
           [0.04,-0.001],
           [0.04,-0.003],
           [0.01,0.002],
           [0.01,0.0075],
           [0.01,0.007],
           [0.01,0.007],
           [0.01,0.0075],
           [0.001,0.047],
           [0.001,0.007],
           [0.001,0.008],
           [0.01,0.008],
           [0.001,0.0087],
           [0.01,0.007],
           [0.01,0.007],
           [0.01,0.005],
           [0.01,0.007],
           [0.01,0.006],
           [0.005,0.0095],
           [0.005, -0.005],
           [0.005,-0.012],
           [0.005,-0.003],
           [0.005,0.0094],
           [0.005,0.0034],
           [0.005,0.004],
           [0.0027,0.008],
           [0.04,0.003],
           [0.04,0.001],
           [0.04,0.003],
           [0.01,0.002],
           [0.01,0.007],
           [0.01,0.007],
           [0.01,0.0075],
           [0.001,0.047],
           [0.001,0.008],
           [0.01,0.008],
           [0.001,0.0087],
           [0.01,0.007],
           [0.01,0.001],
           [0.01,0.005],
           [0.01,0.002],
           [0.01,0.003],
           [0.015,0.0005],
           [0.005, 0.005],
           [0.005,0.0012],
           [0.005,0.003],
           [0.005,0.004],
           [0.005,0.004],
           [0.025,0.004],
         ]

vertices                    = drawVarBlock(ystart, xstart, xstop, deltax, deltay, nudges)
islanda_colors              = [(*greens[randint(0, len(greens) - 1)], 1) for v in range(len(vertices))]
islanda                     = gloo.Program(vertex, fragment_var, count = len(vertices))
islanda["position"]         = vertices
islanda["color"]            = islanda_colors
shapes.append(islanda)

islandb_opacities           = gradiantOpacity(vertices, (0,1)) + gradiantOpacity(vertices, (1,1)) * 0.2 + gradiantOpacity(vertices, (-1,-.5))
islandb_colors              = [(*sands[randint(0, len(greens) - 1)], islandb_opacities[v]) for v in range(len(vertices))]
islandb                     = gloo.Program(vertex, fragment_var, count = len(vertices))
islandb["position"]         = vertices
islandb["color"]            = islandb_colors
shapes.append(islandb)

#############
# Buildings #
#############

bldg_cch_vertices      = np.array([ (-0.5, 0.2), (0.1, 0.2), (0.1, 1),
                           (0.1, -1),   (-0.4, 0.2), (0.1, 0.2),
                           (-0.4, -1), (0.1, -1), (0.1, 0.2)
                         ])

bldg_cch               = gloo.Program(vertex_m, fragment_uni, count = len(bldg_cch_vertices))
bldg_cch["position"]   = bldg_cch_vertices
bldg_cch["color"]      = (*bldgs[0], 1)
model = np.eye(4, dtype=np.float32)
glm.rotate(model, 0.3, 0, 0, 1)
glm.scale(model, 0.1, 0.1, 1)
glm.translate(model, -0.1, .5, 0.0)
bldg_cch["model"] = model
shapes.append(bldg_cch)

# Tell glumpy what needs to be done at each redraw
@window.event
def on_draw(dt):
    window.clear()
    for shape in shapes:
        shape.draw(gl.GL_TRIANGLE_STRIP)

# Run the app
app.run()
