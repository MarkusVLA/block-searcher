
from functools import partial
import anvil
import pandas as pd
import plotly.express as px
from mayavi import mlab
import numpy as np
import csv
import os
from numba import jit
import multiprocessing as mp



PATH = os.path.dirname(os.path.abspath(__file__))


def write_csv(blocklist, region_id):
    df = make_data_frame(blocklist)
    os.makedirs('out', exist_ok=True)
    df.to_csv('out\out.csv', mode='a', header=False, index=False)


def make_data_frame(data):  
    df = pd.DataFrame(data, columns=['x', 'y', 'z'])
    return df


def user_data():
    print("1.12.2 block ids: https://www.digminecraft.com/lists/item_id_list_pc_1_12.php")
    block_id = int(input("Block id to search: "))
    return block_id


def get_chuk(xc, zc, region_id, path):
    region_name = '\\r.{}.{}.mca'.format(region_id[0], region_id[1])                                 
    region = anvil.Region.from_file(path + region_name)         

    #Error handling for chunk not existing.
    try:
        chunk = anvil.Chunk.from_region(region, xc, zc)
        return chunk

    except:
        print("Failed to load chunk {}.".format((xc, zc)))
        return False
 

#faster block itereation this way
@jit(nopython = True)
def index_to_coord(i):
    return ((i) % 16 , i // (16 * 16) , (i // 16) % 16)


def get_blocks_with_id(chunk, id):
    blocks = []
    k = 0
    for block in chunk.stream_chunk(index = 0, section=None):
        if block.id == id:
            blocks.append(index_to_coord(k))
        k += 1
    return blocks
        

def split_region_name(name):
    comp = list(name.split("."))
    x = int(comp[1]);  z = int(comp[2])
    return (x , z)


@jit(nopython = True)
def to_real_coordinates(tuple, cx, cz):
    return ((tuple[0] + cx * 16) , (tuple[1]) , (tuple[2] + cz * 16 ))


def get_block_coordinates_by_id(block_id, region, size, world_directory):
    coordinates = []
    print("\nReading region {}...".format(region))
    reg_x = region[0]
    reg_z = region[1]
    for xc in range(size):
        if reg_x < 0:
            xc = (abs(xc) + 1) * (-1)
        for zc in range(size):
            if reg_z < 0:
                zc = (abs(zc) + 1) * (-1)
            chunk = get_chuk(xc, zc, region, world_directory)

            #Error reading chunk. In case chunk doesn't exist.
            if chunk == False:
                pass

            else:
                cx = chunk.x
                cz = chunk.z
                chunk_blocks = get_blocks_with_id(chunk, block_id)
                for index, tuple in enumerate(chunk_blocks):
                        coordinates.append(to_real_coordinates(tuple, cx, cz))

    return coordinates




def main(id, world_directory, region_id):
    coords = get_block_coordinates_by_id(id, region_id, 32, world_directory)
    print("\nExporting to csv")
    write_csv(coords, region_id)


def initialize_csv():
    form = []
    df = make_data_frame(form)
    os.makedirs('out', exist_ok=True)
    df.to_csv('out\out.csv', mode='w', index_label = False)



regions = []

if __name__ == "__main__":

    id = user_data() 
    world_directory = input("Full path to region files:")

    initialize_csv()
    print("\nDone initalizing output.")
    print("Found {} files in {}".format(len(os.listdir(world_directory)), world_directory))

    for region_file in os.listdir(world_directory):
        region_id = split_region_name(region_file)
        regions.append(region_id)

    #Create a process pool to devide tasks among cpu threads.
    print("Creating process pool.")
    p = mp.Pool()
    p.map(partial(main, id, world_directory ), regions)

    p.close()
    print("Starting search.")
    p.join()
    
        

        

