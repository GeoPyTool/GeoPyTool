from shapely.ops import cascaded_union, polygonize
from scipy.spatial import Delaunay
import numpy as np
import math
import pylab as pl
import fiona
import shapely.geometry as geometry
from descartes import PolygonPatch


def plot_polygon(polygon):
    fig = pl.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    margin = .3

    print(polygon)

    x_min, y_min, x_max, y_max = polygon.bounds
    ax.set_xlim([x_min - margin, x_max + margin])
    ax.set_ylim([y_min - margin, y_max + margin])
    patch = PolygonPatch(polygon, fc='#999999',
                         ec='#000000', fill=True,
                         zorder=-1)
    ax.add_patch(patch)
    return fig


def add_edge(edges, edge_points, coords, i, j):
    """
    Add a line between the i-th and j-th points,
    if not in the list already
    """
    if (i, j) in edges or (j, i) in edges:
        # already added
        return( edges.add((i, j)), edge_points.append(coords[[i, j]]))



def alpha_shape(points, alpha):
    """
    Compute the alpha shape (concave hull) of a set
    of points.
    @param points: Iterable container of points.
    @param alpha: alpha value to influence the
        gooeyness of the border. Smaller numbers
        don't fall inward as much as larger numbers.
        Too large, and you lose everything!
    """
    if len(points) < 4:
        # When you have a triangle, there is no sense
        # in computing an alpha shape.
        return geometry.MultiPoint(list(points)).convex_hull

    #coords = np.array([point.coords[0] for point in points])

    coords = np.array(points)

    print(coords)

    tri = Delaunay(coords)
    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the
    # triangle
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]
        # Lengths of sides of triangle
        a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
        b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
        c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)
        # Semiperimeter of triangle
        s = (a + b + c)/2.0
        # Area of triangle by Heron's formula
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        circum_r = a*b*c/(4.0*area)
        # Here's the radius filter.
        #print circum_r
        if circum_r < 1.0/alpha:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)
    m = geometry.MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return (cascaded_union(triangles), edge_points)

    print (cascaded_union(triangles), edge_points)




a = np.array([ 0.46421546,  0.50670312,  0.76935034,  0.75152631,  0.41167491,
    0.75871446,  0.54695894,  0.36280667,  0.08900743,  0.32331662])
b = np.array([ 0.57476821,  0.34486742,  0.41292409,  0.95925496,  0.48904496,
    0.69459014,  0.92621067,  0.18750462,  0.28832875,  0.85921044])

points=[]

for i in range(len(a)):
    points.append([a[i],b[i]])

point_collection = geometry.MultiPoint(list(points))
point_collection.envelope


alpha = .4
concave_hull, edge_points = alpha_shape(points,alpha=alpha)

print(concave_hull)

_ = plot_polygon(point_collection.envelope)
_ = plot_polygon(concave_hull)
_ = pl.plot(a, b, 'o', color='#f16824')

pl.show()




