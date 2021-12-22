from pyproj import Proj, transform, Transformer
import numpy as np

startX = 370000
endX = 410000
startY = 2030000
endY = 1990000
step = 100
NAN = -9999
project_name = 'oman'
epsg_local = 3440
#https://epsg.io/
#http://srtm.csi.cgiar.org/srtmdata/
input = '../input/'+project_name+'/srtm_47_08.asc'
input2 = '../input/'+project_name+'/srtm_47_09.asc'
input3 = '../input/'+project_name+'/srtm_48_08.asc'
input4 = '../input/'+project_name+'/srtm_48_09.asc'

xllcorner = 50
yllcorner= 20
cellsize=0.00083333333333333
ncols = 6000
with open(input, "r") as ins:
    i = 0
    for line in ins:
        if i >= 6:
            break;
        print(line)
        param = line.split()
        if param[0] == 'xllcorner':
            xllcorner = float(param[1])
        if param[0] == 'yllcorner':
            yllcorner = float(param[1])
        if param[0] == 'cellsize':
            cellsize = float(param[1])
        if param[0] == 'ncols':
            ncols = float(param[1])
        i += 1
# srtm_x = xllcorner * 0.2 + 37
# srtm_y = yllcorner * (-0.2) + 12


fileName = '../output/'+project_name
fileName += str(step) + 'x' + str(step) + '.topo'

epsg_global = 4326

transformerBack = Transformer.from_crs(epsg_global,epsg_local)
x1,y1 = transformerBack.transform(yllcorner,xllcorner)
x2,y2 = transformerBack.transform(yllcorner+cellsize*ncols,xllcorner+cellsize*ncols)
startXData = min(x1, x2)
endXData = max(x1, x2)
startYData = min(y1,y2)
endYData = max(y1,y2)
print(xllcorner,yllcorner)
print(xllcorner+cellsize*ncols,yllcorner+cellsize*ncols)
print('')
print(x1,y1)
print(x2,y2)

print(startX,startY)
print(endX,endY)




ascii_grid = np.loadtxt(input, skiprows=6)
ascii_grid2 = np.loadtxt(input2, skiprows=6)
ascii_grid3 = np.loadtxt(input3, skiprows=6)
ascii_grid4 = np.loadtxt(input4, skiprows=6)
myfile = open(fileName, 'w')

startLoopX = startX
endLoopX = endX
startLoopY = startY
endLoopY = endY
print (ascii_grid[0][0])
print (ascii_grid[5999][0])
print (ascii_grid[5999][5999])
print (ascii_grid[0][5999])
print('Loop')
print(startLoopX, endLoopX)
print(startLoopY, endLoopY)

def GetZ(la, lo):
    la2 = int(la - ncols)
    lo2 = int(lo - ncols)
    if(la >= ncols and lo >= ncols):
        return ascii_grid4[la2][lo2]
    if(la >= ncols and lo >= 0 and lo < ncols):
        return ascii_grid3[la2][lo]
    if(la >= 0 and la < ncols and lo >= 0 and lo < ncols):
        return ascii_grid[la][lo]
    if(la >= 0 and la < ncols and lo >= ncols):
        return ascii_grid2[la][lo2]
    print('lo=',lo, 'la=',la, 'lo2=',lo2,'la2=',la2)
transformer = Transformer.from_crs(epsg_local, epsg_global)
for x in range(startLoopX, endLoopX,step):
    print(x)
    data = ""
    #for y in range(startLoopY,endLoopY, step):
    for y in range(startLoopY, endLoopY, -step):
        laVal, loVal = transformer.transform(x, y)
        la = int(ncols - 1 - round((laVal - yllcorner) / cellsize));
        lo = int(round((loVal - xllcorner) / cellsize));
        z = GetZ(la,lo)
        if z == NAN:
            z = 0
        data += str(x) + "\t" + str(y) + "\t"+ str(z)+'\n'
    myfile.write(data)
