
import pandas as pd
from mayavi import mlab
import plotly.express as px

#can render as many points as you have ram
def plot_block_positions_3D(positions): 
    #Function takes list of (x,y,z) tuples and grapsh them in 3d space.
    xl = [];  yl = [];  zl = []
    for index, tup in enumerate(positions):
        try:
            xl.append(tup[0]);  yl.append(tup[1]);  zl.append(tup[2])
        except:
            pass

    #Bottom to top color gradient 
    s = yl
    mlab.points3d(xl, yl, zl, s, colormap = "RdYlBu", scale_factor = 1.0, scale_mode='none', opacity = 1,  mask_points = None, mode = "point")  
    mlab.show()


def make_data_frame(data):  
    df = pd.DataFrame(data, columns=['x', 'y', 'z'])
    return df

#good for smaller ammouts of data (<500k blocks)
def plot_data_frame_3D(df):
    fig = px.scatter_3d(df, x = 'x', y = 'z', z = 'y' , title ='test', color = 'y', opacity=1.0)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.show()


def read_file():
    tups = []
    with open('out\out.csv') as csv_file:
        for line in csv_file:
            try:
                s = list(line.split(','))
                tup = (int(s[0]), int(s[1]), int(s[2]))
                tups.append(tup)
            except:
                pass
    return tups
            

print("Plot 1 is good for plotting smaller ammounts of data. 2 can go up to millions of points")
mode = input("Plot type: 1 / 2\n")

dat = read_file()

if mode == '1':
    df = make_data_frame(dat)
    print(df)
    plot_data_frame_3D(df)

else:
    plot_block_positions_3D(dat)