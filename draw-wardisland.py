
# References used
# Python & OpenGL for Scientific Visualization, Nicolas P. Rougier
# - https://www.labri.fr/perso/nrougier/python-opengl/

from random import randint
import numpy as np
from glumpy import app, gloo, gl, glm, transforms
from glumpy.ext import png
from scipy import interpolate

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

# Colors
debug = np.array((255, 0, 0)) / 255
sand = np.array((245, 240, 188)) / 255
light_green = np.array((171, 191, 157)) /255

bldgs  = [ np.array((221, 232, 240)) / 255,
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

# Shapes, curves
shapes = []
curves = []

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
xstart = -1
xstop  = 1

nudges = [ [0.0, 0.0],
           [0.00, 0.000],
           [0.001, 0.00],
           [0.005, 0.000],
           [0.005, 0.000 ],
           [0.007, 0.0000 ],
           [0.005 ,0.0000 ],
           [0.007 , 0.000],
           [0.005,0.00],
           [0.012,0.000],
           [0.014,0.000],
           [0.004,0.000],
           [0.008,0.0001],
           [0.0072,0.0001],
           [0.0075,0.0002],
           [0.008 ,0.0003],
           [0.006 ,00.001],
           [0.011 ,0.001],
           [0.0021 ,0.001],
           [0.0051 ,0.001],
           [0.0054 ,0.001],
           [0.012 ,0.001],
           [0.0101 ,0.001],
           [0.0011 ,0.001],
           [0.027 ,0.001],
           [0.007 ,0.004],
           [0.0201 ,0.014],
           [0.0102 ,0.014],
           [0.0072 ,0.014],
           [0.016 ,0.014],
           [0.0172 ,0.014],
           [0.0015 ,0.014],
           [0.0063 ,-0.00004],
           [0.0065,-0.00004],
           [0.06,-0.014],  ########
           [0.0063,-0.00004],
           [-0.0047,-0.00004],
           [0.0046,0.0015],
           [-0.0001,0.015],
           [0.0025,0.016],
           [-0.011,0.0145],
           [-0.0034,0.013],
           [0.002,-0.003],
           [0.0013,0.0145],
           [-0.0116,0.016],
           [0.0025,0.0167],
           [0.0144,0.014],
           [0.0053,0.012],
           [0.0035,0.008],
           [0.0028,0.008],
           [0.0027,0.0086],
           [0.0035,0.0085],
           [0.0035,0.008],
           [0.0047,0.008],
           [0.0037,0.008],
           [0.0035,0.008],
           [0.0035,0.008],
           [0.0035,0.008],
           [0.0035,0.008],
           [0.0033,0.008],
           [0.0033,0.004],
           [0.0033,0.00145],
           [0.0035,0.0019],
           [0.0041,0.0013],
           [-0.0001,0.00135],
           [-0.0005,0.0043],
           [0.0031,0.0013],
           [0.0035,0.0045],
           [0.0021,0.003],
           [0.0022,0.0037],
           [0.0021,-0.000001],
           [-0.0005,0.0002],
           [0.0022,-0.0001],
           [0.0035,-0.0003],
           [0.0025,-0.001],
           [0.0025,0.001],
           [0.0025,0.01],
           [0.0025,0.0014],
           [0.0025,0.004],
           [0.0025,0.004],
           [0.0025,0.008],
           [0.0025,0.007],
           [0.0025,0.007], #####
           [0.0065,0.007],
           [0.0175,0.007],
           [0.0185,0.0075],
           [0.0085,0.007],
           [0.0195,0.007],
           [0.0035,0.0075],
           [0.0125,0.0047],
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
           [0.01,0.0045],
           [0.01,0.004],
           [0.01,0.004],
           [0.01,0.0045],
           [0.001,0.047],
           [0.001,0.007],
           [0.001,0.004],
           [0.01,0.004],
           [0.011,0.0047],
           [0.02,0.004],
           [0.01,0.004],
           [0.02,0.005],
           [0.01,0.004],
           [0.03,0.006],
           [0.005,0.0095],
           [-0.015, 0.015],
           [-0.025,0.022],
           [-0.045,0.013],
           [0.025,0.0194],
           [0.0315,0.0234],
           [0.03015,0.024],
           [0.020127,0.018],
           [0.0004,0.003],
           [0.004,0.001],
           [0.0004,0.003],
           [0.001,0.006],
           [0.011,0.017],
           [0.0101,0.017],
           [0.011,0.0175],
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

# Corpus Christi Hall (CCH)
bldg_cch_vertices      = np.array([ (-0.7, 0.2), (0.1, 0.2), (0.1, 1),
                           (0.1, -1),   (-0.4, 0.2), (0.1, 0.2),
                           (-0.4, -1), (0.1, -1), (0.1, 0.2)
                         ])
bldg_cch               = gloo.Program(vertex_m, fragment_uni, count = len(bldg_cch_vertices))
bldg_cch["position"]   = bldg_cch_vertices
bldg_cch["color"]      = (*bldgs[0], 0.9)
bldg_cch_model = np.eye(4, dtype=np.float32)
glm.rotate(bldg_cch_model, 0.3, 0, 0, 1)
glm.scale(bldg_cch_model, 0.1, 0.1, 1)
glm.translate(bldg_cch_model, -0.08, .65, 0.0)
bldg_cch["model"] = bldg_cch_model
shapes.append(bldg_cch)

# Center for the Arts (CA)
bldg_ca_vertices =    np.array([ (0, 0), (.7, 0), (0, 0.5),
                                 (.7, .5), (.7, 0), (0, 0.5),
                                 (.7, 0), (.7, .5), (1, 0.0),
                                 (1, 0.0), (1, 0.5), (.7, 0.5),
                                 (0.5, 0), (1, 0.0), (0.7, 0.7),
                                 (1, 0.0), (1, 0.7), (.7, 0.7),
                                 (1, 0), (1.5, 0.0), (1, 0.6),
                                 (1.5, 0.0), (1.5, 0.6), (1, 0.6),
                                 (.2, 0), (.2, -0.15), (1.6, 0),
                                 (.2, -0.15), (1.6, 0), (1.6, -0.15),

                      ])
bldg_ca               = gloo.Program(vertex_m, fragment_uni, count = len(bldg_ca_vertices))
bldg_ca["position"]   = bldg_ca_vertices
bldg_ca["color"]      = (*bldgs[0], 0.9)
bldg_ca_model = np.eye(4, dtype=np.float32)
glm.rotate(bldg_ca_model, 0.3, 0, 0, 1)
glm.scale(bldg_ca_model, 0.13, 0.1, 1)
glm.translate(bldg_ca_model, -0.04, .55, 0.0)
bldg_ca["model"] = bldg_ca_model
shapes.append(bldg_ca)

# O'Conner
bldg_ocon_vertices =    np.array([ (0.0, 0.0), (1, 0.0), (0.0, 1),
                                  (1, 0.0), (0.0, 1), (1, 1),
                                  (0.0, 0.6), (-0.2, 0.6), (0.0, 0.4),
                                  (-0.2, 0.6), (0.0, 0.4), (-0.2, 0.4),
                                  (.6, 1), (.9, 1), (.6, 1.2),
                                  (.9, 1), (.6, 1.2), (.9, 1.2),
                      ])
bldg_ocon               = gloo.Program(vertex_m, fragment_uni, count = len(bldg_ocon_vertices))
bldg_ocon["position"]   = bldg_ocon_vertices
bldg_ocon["color"]      = (*bldgs[0], 0.9)
bldg_ocon_model = np.eye(4, dtype=np.float32)
glm.rotate(bldg_ocon_model, 0.2, 0, 0, 1)
glm.scale(bldg_ocon_model, 0.14, 0.12, 1)
glm.translate(bldg_ocon_model, -0.2, .35, 0.0)
bldg_ocon["model"] = bldg_ocon_model
shapes.append(bldg_ocon)

# Mary & Jeff Bell Library
bldg_lib_vertices =    np.array([ (0.0, 0.0), (1, 0.0), (0.0, 1),
                                  (1, 0.0), (0.0, 1), (1, 1),
                      ])
bldg_lib               = gloo.Program(vertex_m, fragment_uni, count = len(bldg_lib_vertices))
bldg_lib["position"]   = bldg_lib_vertices
bldg_lib["color"]      = (*bldgs[0], 0.9)
bldg_lib_model = np.eye(4, dtype=np.float32)
#glm.rotate(bldg_lib_model, 0.5, 1, 1, 1)
glm.scale(bldg_lib_model, 0.05, .15, 1)
glm.translate(bldg_lib_model, -0.11, .164, 0.0)
bldg_lib["model"] = bldg_lib_model
shapes.append(bldg_lib)

# Bay Hall (BH)
bldg_bay_vertices =    np.array([ (0.0, 0.0), (1, 0.0), (0.0, 1),
                                  (1, 0.0), (0.0, 1), (1, 1),
                      ])
bldg_bay               = gloo.Program(vertex_m, fragment_uni, count = len(bldg_bay_vertices))
bldg_bay["position"]   = bldg_bay_vertices
bldg_bay["color"]      = (*bldgs[0], 0.9)
bldg_bay_model = np.eye(4, dtype=np.float32)
#glm.rotate(bldg_bay_model, 0.5, 1, 1, 1)
glm.scale(bldg_bay_model, 0.06, .13, 1)
glm.translate(bldg_bay_model, 0.05, .38, 0.0)
bldg_bay["model"] = bldg_bay_model
shapes.append(bldg_bay)

# Faculty Center (FC)
bldg_fc_vertices =    np.array([ (0.0, 0.0), (1, 0.0), (0.0, 1),
                                  (1, 0.0), (0.0, 1), (1, 1),
                                  (0.2, 0.0), (0.2, -0.25), (.9, 0.0),
                                  (.9, 0.0), (0.2, -0.25), (.9, -0.25),


                      ])
bldg_fc               = gloo.Program(vertex_m, fragment_uni, count = len(bldg_fc_vertices))
bldg_fc["position"]   = bldg_fc_vertices
bldg_fc["color"]      = (*bldgs[0], 0.9)
bldg_fc_model = np.eye(4, dtype=np.float32)
#glm.rotate(bldg_fc_model, 0.5, 1, 1, 1)
glm.scale(bldg_fc_model, 0.15, .04, 1)
glm.translate(bldg_fc_model, -.045, .32, 0.0)
bldg_fc["model"] = bldg_fc_model
shapes.append(bldg_fc)

# Center for Instruction (CI)
bldg_ci_vertices = np.array([ (0, 0), (2, 0), (2, 7),
                              (0, 0), (2, 7), (0, 7),
                              (-3, 0), (3, 0), (0, -4),
                              (-3, 0), (0, 0), (0, 8.5),
                              (-3, 8.5), (0, 8.5), (-3, 0),
                              (-3, 0), (-11, 0), (-11, 3),
                              (-3, 3), (-3, 0),(-11, 3),
                              (-11, 3), (-11, 4.5), (-4, 3),
                              (-4, 4.5), (-11, 3), (-4, 3),
                  ])
bldg_ci               = gloo.Program(vertex_m, fragment_uni, count = len(bldg_ci_vertices))
bldg_ci["position"]   = bldg_ci_vertices
bldg_ci["color"]      = (*bldgs[0], 0.9)
bldg_ci_model = np.eye(4, dtype=np.float32)
#glm.rotate(bldg_ci_model, 0.5, 1, 1, 1)
glm.scale(bldg_ci_model, 0.011, .011, 1)
glm.translate(bldg_ci_model, .1, .175, 0.0)
bldg_ci["model"] = bldg_ci_model
shapes.append(bldg_ci)

# University Services Center (USC)
bldg_usc_vertices   = np.array([ (0, 0), (7, 0), (0, 4),
                                 (7, 0), (0, 4), (7, 4),
                                 (-4, 4), (0, 0), (0, 4),
                                 (3.5, 0), (7, 0), (9, -5),
                                 (7, 0), (7, 4), (12, -1),
                                 (12, -1), (9, -5), (7, 0),
                              ])
bldg_usc_vertices = bldg_usc_vertices
bldg_usc               = gloo.Program(vertex_m, fragment_uni, count = len(bldg_usc_vertices))
bldg_usc["position"]   = bldg_usc_vertices
bldg_usc["color"]      = (*bldgs[0], 0.9)
bldg_usc_model = np.eye(4, dtype=np.float32)
#glm.rotate(bldg_usc_model, 0.5, 1, 1, 1)
glm.scale(bldg_usc_model, 0.0075, .0075, 1)
glm.translate(bldg_usc_model, -.045, .7, 0.0)
bldg_usc["model"] = bldg_usc_model
shapes.append(bldg_usc)

# Dugan Wellness Center (DWC)
bldg_dwc_vertices = np.array([ (0, 0), (0, 1), (1, 0),
                               (0, 1), (1, 0), (1, 1),
                               (0, 0), (1, 0), (-.02, -0.25),
                               (0, 1), (-0.255, 0.94), (-.02, -0.25),

                            ])
bldg_dwc               = gloo.Program(vertex_m, fragment_uni, count = len(bldg_dwc_vertices))
bldg_dwc["position"]   = bldg_dwc_vertices
bldg_dwc["color"]      = (*bldgs[0], 0.9)
bldg_dwc_model = np.eye(4, dtype=np.float32)
#glm.rotate(bldg_dwc_model, 0.5, 1, 1, 1)
glm.scale(bldg_dwc_model, 0.075, .075, 1)
glm.translate(bldg_dwc_model, .062, .02, 0.0)
bldg_dwc["model"] = bldg_dwc_model
shapes.append(bldg_dwc)

# Glasscock Student Success Center (GSSC)
bldg_gssc_vertices = np.array([ (0, 0), (7, 0), (0, -1.5),
                                (7, -1.5), (7, 0), (0, -1.5),
                                (4, 0), (4, 2),(0, 2),
                                (0, 0), (0, 2), (4, 0),
                                (0, 2), (0, 3.5), (7, 3.5),
                                (7, 2), (7, 3.5),(0, 2),
                             ])
bldg_gssc               = gloo.Program(vertex_m, fragment_uni, count = len(bldg_gssc_vertices))
bldg_gssc["position"]   = bldg_gssc_vertices
bldg_gssc["color"]      = (*bldgs[0], 0.9)
bldg_gssc_model = np.eye(4, dtype=np.float32)
#glm.rotate(bldg_gssc_model, 0.5, 1, 1, 1)
glm.scale(bldg_gssc_model, 0.012, .014, 1)
glm.translate(bldg_gssc_model, -.225, .25, 0.0)
bldg_gssc["model"] = bldg_gssc_model
shapes.append(bldg_gssc)

# Engineering (EN)
bldg_en_vertices = np.array([ (0, 0), (0, 1), (6, 1),
                              (6, 0), (6, 1), (0, 0),
                              (1.5, 0), (1.5, -.7), (0, 0),
                              (0, -.7), (1.5, -.7), (0, 0),
                              (-1, 1), (0, 1), (0, -.7),
                              (0, 1.5), (5.5, 1.5), (0, 1),
                              (5.5, 1.5), (5.5, 1), (0, 1),
                             ])
bldg_en               = gloo.Program(vertex_m, fragment_uni, count = len(bldg_en_vertices))
bldg_en["position"]   = bldg_en_vertices
bldg_en["color"]      = (*bldgs[0], 0.9)
bldg_en_model = np.eye(4, dtype=np.float32)
#glm.rotate(bldg_en_model, 0.5, 1, 1, 1)
glm.scale(bldg_en_model, 0.02, .04, 1)
glm.translate(bldg_en_model, -.25, .16, 0.0)
bldg_en["model"] = bldg_en_model
shapes.append(bldg_en)

########
# Wind #
########
Xres = 100
Yres = 100
wind_mag = np.array([ [1.0, 1.0, 1.0, 1.0, 1.0],
                      [1.0, 1.0, 1.0, 1.0, 1.0],
                      [.5, .5, 1.5, 1.5, 1.5],
                      [.4, 1.5, 2.5, 1.5, 2],
                      [.4, .4, .0, 2.0, 2.0],
                    ])
wind_dir = np.array([ [-1.6, -1.6, -1.6, -1.3, 1.3],
                      [-0.35, -1.6, 1.6, 0.8, 1.3],
                      [-0.35, -0.8, -0.3, 0.8, 1.5],
                      [0, -0.2, 0.5, 0.7, 2.7],
                      [0.2, 0.5, 0.6, 1.7, 2.7],
                    ])

# Convert original, not upsampled since cos/sin expensive
wind_v = wind_mag * np.cos(wind_dir)
wind_u = wind_mag * np.sin(wind_dir)

# Interpolate (upsample) u, v to Xres, Yres
x = np.array(range(wind_v.shape[1]))
y = np.array(range(wind_v.shape[0]))
xx, yy = np.meshgrid(x, y)
f_v = interpolate.interp2d(x, y, wind_v, kind = 'linear')
f_u = interpolate.interp2d(x, y, wind_u, kind = 'linear')
xnew = np.linspace(0, 5, Xres)
ynew = np.linspace(0, 5, Yres)
inter_v = f_v(xnew, ynew)
inter_u = f_u(xnew, ynew)

# Setup environment
env = { "v"  : inter_v,
        "u"  : inter_u,
        "wi" : abs(1 - (-1)),
        "hi" : abs(1 - (-1)),
        "wj" : Xres,
        "hj" : Yres,
      }

numAgents = 5500
dirs = np.linspace(-np.pi/2, np.pi/2, numAgents)
mags = np.cos(np.linspace(0, 100, numAgents))
ypos = np.linspace(-1, 1, numAgents)
xpos = -1 * np.ones((numAgents))
vvec = mags * np.sin(dirs)
uvec = mags * np.cos(dirs)

agents = np.column_stack((ypos, xpos, vvec, uvec))

def moveAgent(agent, time = 0.05, env = None):
    # Agent : (y, x, v, u)
    e_v = 0.0
    e_u = 0.0
    if env is not None:
        # Convert world coords to env coords
        ylen = agent[0] + 1
        xlen = agent[1] + 1
        erow = int(np.floor(env["hj"] * (ylen / env["hi"])))
        ecol = int(np.floor(env["wj"] * (xlen / env["wi"])))
        if erow < 0 and ecol < env["u"].shape[1]:
            e_v =  4.7
            e_u =  1.7
        elif erow < 0 and ecol >= env["u"].shape[1]:
            e_v =  4.3
            e_u = -2.5
        try:
            e_v  = env["v"][erow][ecol]
            e_u  = env["u"][erow][ecol]
        except:
            pass

    # Move agent with velocity for duration
    # (pos_new = pos_old + velocity * tme)
    agent[0] = agent[0] + (agent[2] + e_v) * time
    agent[1] = agent[1] + (agent[3] + e_u) * time

def recordAgent(agent, time = 0.05, duration = 10, env = None):
    iters = int(np.ceil(duration / time))
    trajectory = np.zeros((iters, 2))
    for i in range(iters):
        trajectory[i] = (agent[1], (-1) * agent[0])
        moveAgent(agent, time, env)
    trajectory[i] = (agent[1], (-1) * agent[0])
    return trajectory

for agent in agents:
    traj = recordAgent(agent, time = 0.005, env = env)
    # Trajectory to line object
    traj_line               = gloo.Program(vertex_m, fragment_uni, count = traj.shape[0])
    traj_line["position"]   = traj
    traj_line["color"]      = (*bldgs[0], 0.4)
    traj_line_model = np.eye(4, dtype=np.float32)
    ##glm.rotate(bldg_en_model, 0.5, 1, 1, 1)
    #glm.scale(bldg_en_model, 0.02, .04, 1)
    #glm.translate(bldg_en_model, -.25, .16, 0.0)
    traj_line["model"] = traj_line_model
    curves.append(traj_line)


################
# Setup OpenGL #
################

# Create a window with a valid GL context
window = app.Window()
framebuffer = np.zeros((window.height, window.width * 3), dtype=np.uint8)

# Tell glumpy what needs to be done at each redraw
@window.event
def on_draw(dt):
    window.clear()
    for shape in shapes:
        shape.draw(gl.GL_TRIANGLE_STRIP)

    gl.glReadPixels(0, 0, window.width, window.height,
           gl.GL_RGB, gl.GL_UNSIGNED_BYTE, framebuffer)
    png.from_array(np.flipud(framebuffer), 'RGB').save('wardisland_a.png')

    for curve in curves:
        curve.draw(gl.GL_LINES)

    gl.glReadPixels(0, 0, window.width, window.height,
           gl.GL_RGB, gl.GL_UNSIGNED_BYTE, framebuffer)
    png.from_array(np.flipud(framebuffer), 'RGB').save('wardisland_b.png')

# Run the app
app.run()
