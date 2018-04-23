from PIL import Image
from scipy import interpolate
import numpy as np

fsize = open("/code/odm_orthophoto/odm_orthophoto_log.txt",'r')

while True:
    line =fsize.readline()
    if not line:
        break
    if ":" in line:
        linearr = line.split(':', 2)
        if "resolution, " in linearr[0]:
            size = linearr[1].split('x',2)
            width  = int(size[0])
            height = int(size[1])
            break
    else :
        continue

if width==0 or height==0:
    print("Error: Invalid size!!\n")

img = Image.new('RGB', (width,height),"black")
f = open("/code/my_out/copy.ply",'r')
fp = open("/code/my_out/copy.ply",'r')
#img.show()

pixels = img.load()
head = 1

max_x= -100000
min_x= 100000
max_y= -100000  
min_y=  100000

while True:
    line = f.readline()
    if not line:
        break          # no line to read
    if head ==0 :               # not header
        linearr = line.split(' ',2)
        x = float(linearr[0])
        y = float(linearr[1])
        #print(x,y)
        if x > max_x :
            max_x = x
        if x<min_x :
            min_x = x
        if y>max_y:
            max_y = y
        if y<min_y:
            min_y = y

    elif line == "end_header\n":    #end of the header
            head = 0
    else : 
        continue
#print (max_x,min_x,max_y,min_y)
#print (img.size[0],img.size[1])
#print (pixels[0,0])


act_width = max_x-min_x
act_height = max_y-min_y
head = 1
points = []
grid_x, grid_y = np.mgrid[0:width, 0:height]
#grid_y = np.mgrid[0:height]

grid_r = []
grid_g = []
grid_b = []


#print (grid_r)
while True:
    line = fp.readline()
    if not line: break          # no line to read
    if head ==0 :               # not header
        linearr = line.split(' ',5)
        x = float(linearr[0])
        y = float(linearr[1])
        r = int(linearr[3])
        g = int(linearr[4])
        b = int(linearr[5])
          
        pixel_x = int((width-1)*(x-min_x)/act_width)
        pixel_y = int((height-1)*(y-min_y)/act_height)
        
        #pixels[pixel_x , pixel_y] = (r,g,b)
        #print(pixel_x,pixel_y)
        #grid_x.append(pixel_x)
        #grid_y.append(pixel_y)
        points.append([pixel_x,pixel_y])

        grid_r.append(r)
        grid_g.append(g)
        grid_b.append(b)


    elif line == "end_header\n":    #end of the header
            head = 0
    else : 
        continue

#print (points,len(grid_x), len(grid_r))

rf = interpolate.griddata(points,grid_r,(grid_x,grid_y),method='cubic')
#rf = interpolate.interp2d(grid_x,grid_y,grid_r,kind='cubic')
print("red end")

gf = interpolate.griddata(points,grid_g,(grid_x,grid_y),method=    'cubic')
#gf = interpolate.interp2d(grid_x,grid_y,grid_g,kind='cubic')
print("green end")

bf = interpolate.griddata(points,grid_b,(grid_x,grid_y),method='cubic')
#bf = interpolate.interp2d(grid_x,grid_y,grid_b,kind='cubic')
print("blue end")

for i in range(height):
    for j in range(width):
        pixels[j,height-i-1] = (int(rf[j][i]) , int(gf[j][i]), int(bf[j][i]))

img.save("/code/my_out/dem_mesh.png")
f.close()
fp.close()
