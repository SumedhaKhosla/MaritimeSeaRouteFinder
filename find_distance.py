####################################################################################
# Description: Script for finding distance between two ports in the sea            #
# ##################################################################################


# making necessary imports
import warnings
warnings.filterwarnings("ignore")
from scgraph.geographs.marnet import marnet_geograph


# Function for finding shortest distance between 2 seaports given their long and lat
def find_shortest_seaport_distance(srcLng:float, srcLat:float,dstLng:float, dstLat:float):
    output = marnet_geograph.get_shortest_path(
    origin_node={"latitude": srcLat,"longitude": srcLng}, 
    destination_node={"latitude": dstLat,"longitude": dstLng},
    output_units='km')

    return output   


if __name__ == "__main__":
    out = find_shortest_seaport_distance(srcLng=121.47, srcLat=31.23, dstLng=-81.09, dstLat=32.08)
    print(out)
