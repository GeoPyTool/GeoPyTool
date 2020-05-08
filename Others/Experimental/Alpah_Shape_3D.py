import sys
import re
import numba as nb
import numpy as np
import scipy.spatial as spat


@nb.jit
def nb_dot(x, y):
    val = 0
    for x_i, y_i in zip(x, y):
        val += x_i * y_i
    return val


@nb.jit
def nb_cross(x, y):
    val = np.array([x[1] * y[2] - x[2] * y[1],
                    x[2] * y[0] - x[0] * y[2],
                    x[0] * y[1] - x[1] * y[0]])
    return val


@nb.jit
def r2_circumsphere_tetrahedron_single(a, b, c, d):
    ad = a - d
    bd = b - d
    cd = c - d

    ad2 = nb_dot(ad, ad)
    bd2 = nb_dot(bd, bd)
    cd2 = nb_dot(cd, cd)

    cross_1 = nb_cross(bd, cd)
    cross_2 = nb_cross(cd, ad)
    cross_3 = nb_cross(ad, bd)

    q = ad2 * cross_1 + bd2 * cross_2 + cd2 * cross_3
    p = 2 * np.abs(nb_dot(ad, cross_1))
    if p < 1e-10:
        return np.infty

    r2 = nb_dot(q, q) / p ** 2

    return r2


@nb.jit(nopython=True)
def r2_circumsphere_tetrahedron(a, b, c, d):
    len_a = len(a)
    r2 = np.zeros((len_a,))
    for i in range(len_a):
        r2[i] = r2_circumsphere_tetrahedron_single(a[i], b[i], c[i], d[i])
    return r2


@nb.jit
def get_faces(tetrahedron):
    faces = np.zeros((4, 3))
    for n, (i1, i2, i3) in enumerate([(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]):
        faces[n] = tetrahedron[i1], tetrahedron[i2], tetrahedron[i3]
    return faces


def get_single_faces(triangulation):
    num_faces_single = 4
    num_tetrahedrons = triangulation.shape[0]
    num_faces = num_tetrahedrons * num_faces_single
    faces = np.zeros((num_faces, 3), np.int_)  # 3 is the dimension of the model
    mask = np.ones((num_faces,), np.bool_)
    for n in range(num_tetrahedrons):
        faces[num_faces_single * n: num_faces_single * (n + 1)] = get_faces(triangulation[n])
    orderlist = ["x{}".format(i) for i in range(faces.shape[1])]
    dtype_list = [(el, faces.dtype.str) for el in orderlist]
    faces.view(dtype_list).sort(axis=0)
    for k in range(num_faces - 1):
        if mask[k]:
            if np.all(faces[k] == faces[k + 1]):
                mask[k] = False
                mask[k + 1] = False
    single_faces = faces[mask]
    return single_faces


def get_alpha_shape(pointcloud, alpha):
    pointcloud = np.asarray(pointcloud)

    print(pointcloud,'\n',pointcloud.shape[1])

    assert pointcloud.ndim == 2
    assert pointcloud.shape[1] == 3, "for now, only 3-dimensional analysis is implemented"

    triangulation = spat.Delaunay(pointcloud)

    tetrahedrons = pointcloud[triangulation.simplices]  # remove this copy step, could be fatal
    radii2 = r2_circumsphere_tetrahedron(tetrahedrons[:, 0, :], tetrahedrons[:, 1, :], tetrahedrons[:, 2, :],
                                         tetrahedrons[:, 3, :])
    reduced_triangulation = triangulation.simplices[radii2 < alpha ** 2]
    del radii2, triangulation, tetrahedrons

    outer_triangulation = get_single_faces(reduced_triangulation)

    return outer_triangulation



def main():

    a = np.array([ 0.46421546,  0.50670312,  0.76935034,  0.75152631,  0.41167491,
        0.75871446,  0.54695894,  0.36280667,  0.08900743,  0.32331662])
    b = np.array([ 0.57476821,  0.34486742,  0.41292409,  0.95925496,  0.48904496,
        0.69459014,  0.92621067,  0.18750462,  0.28832875,  0.85921044])

    c = np.array([ 0.28563033,  0.32286582,  0.70590688,  0.21250345,  0.16658889,
        0.80191428,  0.22324416,  0.0867027 ,  0.87449543,  0.55770228])



    d=[]
    for i in range(len(a)):
        d.append((a[i],b[i],c[i]))

    e = get_alpha_shape(d,1)
    print(e,'\n',len(e))




if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
