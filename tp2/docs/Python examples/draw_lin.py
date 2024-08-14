import matplotlib.pyplot as plt
#======================
#draw points and lines
#======================

x0, y0 = 6,2 # just a dot

# line 1
# x1 are the x coordinates of the points for the first line, y1 are the y coordinates for the same points
x1, y1 = [-1, 12], [1, 4] 

# line 2
# x2 are the x coordinates of the points for the second line, y2 are the y coordinates for the same points
x2, y2 = [1, 10], [3, 2]

#the elements in x1 and y1 must be in sequence.
plt.plot(x0,y0, x1, y1, x2, y2, marker = 'o')

plt.show()
