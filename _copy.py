import os
import json
#from db import MongoDb


for i in range(1292, 2780):
    print(i)
    s = str(i)
    os.system("sudo cp /Volumes/HARIDHAANAM/bitcoin/blocks/blk0"+s+".dat ~/Documents/bitcoin/blocks/blk0"+s+".dat ")
