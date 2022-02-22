1. get x1, x2, y1, y2
2. get coordinate system


go to https://epsg.io/
3. enter coordinate system and press search
4. get epsg
5. press transform coordinate
6. input x1, y1 to input coordinates
7. press transform
8. press show position on a map on the right panel


go to http://srtm.csi.cgiar.org/srtmdata/
9. tile size 5x5, format esri ascii
10. select 4 tiles on the map in your area and press search
11. make sure that is your area
12. press download srtm for all the 4 tiles
13. make folder with project name
14. unzip the dowloaded srtm and put it to input/project name

pythonProjectProj1
15. set startX = x1, endX = x2, startY = y1, endY = y2
16. epsg_local = epsg from https://epsg.io/
17. set project name
18. run