# arguments
# the layer number from where the anchors should be fully printed
layerNo = 14

file = open("./GcodeFiles/CFFFP_Two Thread Box Walls.gcode", "r")
lines = file.readlines()


# FIND TOOL CHANGE AND COMMNET THEM
# find all the lines that have T1
t1Idx = [i for i, e in enumerate(lines) if e == "T1\n"]
print("T1 pos: ", t1Idx)
# comment 2 more lines above it
for idx in t1Idx:
    lines[idx-2] = ";" + lines[idx-2]
    lines[idx-1] = ";" + lines[idx-1]
    lines[idx] = ";" + lines[idx]

# find all the lines that have T0, comment all except the first one
t0Idx = [i for i, e in enumerate(lines) if e == "T0\n"]
t0Idx.pop(0)  # remove first T0
print("T0 pos: ", t0Idx)
# comment 2 more lines above it
for idx in t0Idx:
    lines[idx-2] = ";" + lines[idx-2]
    lines[idx-1] = ";" + lines[idx-1]
    lines[idx] = ";" + lines[idx]

# find index of ;LAYER + No
layerLineNo = [i for i, e in enumerate(
    lines) if ";LAYER:" + str(layerNo) in e][0]
print("Line no. of the layer: ", layerLineNo)


# we should find after which tool change we should start adding the gcode for anchors
idxStartPrint = -1
# if layer is inside the tool change => then we will start adding the gcode when the tool change is over
for i in range(len(t0Idx)):
    if t1Idx[i] < layerLineNo and layerLineNo < t0Idx[i]:
        # print("In tool change: ", t1Idx[i], " ", t0Idx[i])
        idxStartPrint = i

# if it is outside the tool change
if idxStartPrint == -1:
    for i in range(len(t0Idx)-1):
        if t0Idx[i] < layerLineNo and layerLineNo < t1Idx[i + 1]:
            # print("Between tools: ", t0Idx[i], " ", t1Idx[i + 1])
            idxStartPrint = i + 1

print("Line where Anchors code should be added: ", t0Idx[idxStartPrint])

linesW = 0  # no of lines lready added
for idx in range(idxStartPrint+1, len(t1Idx)):
    # get evrything between the tool change
    toolChangeList = [lines[i] for i in range(t1Idx[idx] + 1, t0Idx[idx] + 1)]
    # remove it from t1Idx[idx] + 1 and t0Idx[idx]
    del lines[t1Idx[idx] + 1:t0Idx[idx] + 1]
    # add it after lines[t0Idx[idxStartPrint]]
    lines = lines[:t0Idx[idxStartPrint] + 1 + linesW] + \
        toolChangeList + lines[t0Idx[idxStartPrint] + 1 + linesW:]
    linesW += t0Idx[idx] - t1Idx[idx]

# comment all lines that have T1:
# M104 T1 S150 ; M104 T1 S200 ; M104 T1 S0 ; M109 T1 S150
t1IdxTemp = [i for i, e in enumerate(
    lines) if e == "M104 T1 S150\n" or e == "M104 T1 S200\n" or e == "M104 T1 S0\n" or e == "M109 T1 S150\n"]

for i in t1IdxTemp:
    lines[i] = ";" + lines[i]

# write to another file
output = open("./GcodeFiles/Modified.gcode", "w")
output.writelines(lines)
output.close()
