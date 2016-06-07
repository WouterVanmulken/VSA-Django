from tpb import TPB
import os
# from tpb import CATEGORIES, ORDERS


startlink = raw_input("what is start of the link ?\n")
endlink =   raw_input("\nwhat is the end of the link ?\n")

# startlink = 'Scorpion.S02E'
# endlink = '.HDTV.x264-LOL[ettv]'


print("\nprocessing...");


magnetList = [];

for x in range(1, 20):
    t = TPB('https://thepiratebay.se') # create a TPB object with default domain

    s = startlink
    if(x<10): s += "0"
    s += str(x) + endlink

    search = t.search(s)

    if(search.items()>0):
        for t in search:
            print(t.title);
            magnetList.append(t.magnet_link)


print("done looping");
wannaDoThis = raw_input("Do you wish to download all of those ?");
if('y' in wannaDoThis):
    for y in range(0, len(magnetList)):
        os.startfile(magnetList[y]);
