from pyproj import Proj, transform, Transformer
import numpy as np

beg_x = 370000
end_x = 410000
beg_y = 2030000
end_y = 1990000
step = 100
NAN = -9999
project_name = 'oman'
epsg_local = 3440
# https://epsg.io/
# http://srtm.csi.cgiar.org/srtmdata/
input_1 = '../input/' + project_name + '/srtm_47_08.asc'
input_2 = '../input/' + project_name + '/srtm_47_09.asc'
input_3 = '../input/' + project_name + '/srtm_48_08.asc'
input_4 = '../input/' + project_name + '/srtm_48_09.asc'

xll_corner = 50
yll_corner = 20
cell_size = 0.00083333333333333
n_cols = 6000
with open(input_1, "r") as ins:
    i = 0
    for line in ins:
        if i >= 6:
            break
        print(line)
        param = line.split()
        if param[0] == 'xllcorner':
            xll_corner = float(param[1])
        if param[0] == 'yllcorner':
            yll_corner = float(param[1])
        if param[0] == 'cellsize':
            cell_size = float(param[1])
        if param[0] == 'ncols':
            n_cols = float(param[1])
        i += 1
# srtm_x = xll_corner * 0.2 + 37
# srtm_y = yll_corner * (-0.2) + 12


fileName = '../output/' + project_name
fileName += str(step) + 'x' + str(step) + '.topo'

epsg_global = 4326

transformerBack = Transformer.from_crs(epsg_global, epsg_local)
x1, y1 = transformerBack.transform(yll_corner, xll_corner)
x2, y2 = transformerBack.transform(yll_corner + cell_size * n_cols, xll_corner + cell_size * n_cols)
startXData = min(x1, x2)
endXData = max(x1, x2)
startYData = min(y1, y2)
endYData = max(y1, y2)
print(xll_corner, yll_corner)
print(xll_corner + cell_size * n_cols, yll_corner + cell_size * n_cols)
print('')
print(x1, y1)
print(x2, y2)

print(beg_x, beg_y)
print(end_x, end_y)

ascii_grid = np.loadtxt(input_1, skiprows=6)
ascii_grid2 = np.loadtxt(input_2, skiprows=6)
ascii_grid3 = np.loadtxt(input_3, skiprows=6)
ascii_grid4 = np.loadtxt(input_4, skiprows=6)
my_file = open(fileName, 'w')


print(ascii_grid[0][0])
print(ascii_grid[5999][0])
print(ascii_grid[5999][5999])
print(ascii_grid[0][5999])
print('Loop')
print(beg_x, end_x)
print(beg_y, end_y)


def get_z(la, lo):
    la2 = int(la - n_cols)
    lo2 = int(lo - n_cols)
    if la >= n_cols and lo >= n_cols:
        return ascii_grid4[la2][lo2]
    if la >= n_cols > lo >= 0:
        return ascii_grid3[la2][lo]
    if 0 <= la < n_cols and 0 <= lo < n_cols:
        return ascii_grid[la][lo]
    if 0 <= la < n_cols <= lo:
        return ascii_grid2[la][lo2]
    print('lo=', lo, 'la=', la, 'lo2=', lo2, 'la2=', la2)


def transform_coord(transformer, beg_loop_x, end_loop_x, step_x, beg_loop_y, end_loop_y, step_y,
                    n_cols, xll_corner, yll_corner, cell_size, nan):
    for x in range(beg_loop_x, end_loop_x, step_x):
        print(x)
        data = ""
        for y in range(beg_loop_y, end_loop_y, step_y):
            laVal, loVal = transformer.transform(x, y)
            la_local = int(n_cols - 1 - round((laVal - yll_corner) / cell_size))
            lo_local = int(round((loVal - xll_corner) / cell_size))
            z = get_z(la_local, lo_local)
            if z == nan:
                z = 0
            data += str(x) + "\t" + str(y) + "\t" + str(z) + '\n'
        my_file.write(data)


transform_coord(Transformer.from_crs(epsg_local, epsg_global), beg_x, end_x, step, beg_y, end_y, -step,
                n_cols, xll_corner, yll_corner, cell_size, NAN)