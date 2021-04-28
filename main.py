import random
class Node:
    def __init__(self, name):
        self.sa0 = 0
        self.name = name
        self.sa1 = 0
        self.testability = 0


gatelist = []  # list of gates
names = []  # list of names
keys = [] # keys to keep track of operations

def readgates():
    with open("c17.fault") as f:
        for line in f:
            # Used to grab specific information by skipping some wires
            #if "->" in line:
            #    continue
            if "test" in line:
                temp = line.split()
                goodoutput = temp[3]
            if "*" not in line:
                continue

            data = line.split()
            #print(data)

            #get object list going
            if data[0] not in names:
                gat = Node(data[0])
                names.append(data[0])
                gatelist.append(gat)

            #calculate the stuck-at-1 and stuck-at-0 gates
            localsa0 = 0
            localsa1 = 0
            if "*" in data[2]:
                if "/0" in data[1]:
                    localsa0 += 1
                elif "/1" in data[1]:
                    localsa1 += 1

                #search for object in list, add to their Stuck-At values
                for index, g in enumerate(gatelist):
                    if g.name == data[0]:
                        g.sa1 += localsa1
                        g.sa0 += localsa0
                        #g.testability = g.sa1 + g.sa0
                        #print(str(g.name) + ": goodoutput is: " + str(goodoutput) + " badoutput is: " + str(data[3]))
                        #print("hd is: " + str(hd(int(goodoutput,2), int(data[3],2))))
                        g.testability = g.sa1*hd(int(goodoutput,2), int(data[3],2)) + g.sa0*hd(int(goodoutput,2), int(data[3],2))
                else: #To keep compiler happy??
                    index = -1
        gatelist.sort(key=lambda x: x.testability, reverse=True)


# Function to calculate hamming distance
# https://www.geeksforgeeks.org/hamming-distance-between-two-integers/
def hd(n1, n2):
    x = n1 ^ n2
    setBits = 0
    while (x > 0):
        setBits += x & 1
        x >>= 1
    return setBits


def addgates(numkeys):
    file = open("c17.bench", "r").readlines()
    ofile = open("c17obf.bench", "w+")
    i=0
    for num in range(numkeys):
        gate = gatelist[i]
        if "->" in gate.name:
            kinput = gate.name.split('->')[0]
            koutput = gate.name.split('->')[1]
            #print(kinput + " -> " + koutput)
            for line in range(len(file)):
                if file[line].split('=')[0].split(' ')[0] == koutput:
                    #print("found -> gate")
                    #print(file[line])
                    keyginsert = "KEYGATE" + str(num)
                    file[line] = file[line].replace(kinput, keyginsert)
                elif "~" in file[line]:
                    #dont wanna mess up new key/keygates
                    break
                if num == numkeys-1:
                    ofile.write(file[line])
        else:
            for line in range(len(file)):
                kinput = gate.name
                if kinput in file[line]:
                    if not file[line].split('=')[0].split(' ')[0] == kinput:
                        #if not file[line].startswith("O") | file[line].startswith("I"):
                            #print(file[line])
                            #print(kinput)
                            # print(file[line])
                        keyginsert = "KEYGATE" + str(num)
                        file[line] = file[line].replace(kinput, keyginsert)
                    #match = kinput + "(?P<character>\,|\))"
                    #regex = re.compile(r"" + match)
                    #file[line] = regex.sub(r"" + "KEYGATE" + str(i) + "\g<character>", file[line])

                    #print(file[line])
                    #keyginsert = "KEYGATE" + str(num)
                    #file[line] = file[line].replace(kinput, keyginsert)
                elif '~' in file[line]:
                    # dont wanna mess up new key/keygates
                    break
                if num == numkeys-1:
                    ofile.write(file[line])
        i+=1
    ofile.close()

    ##add keys
    file = open("c17obf.bench", "a")
    file.write("~\n")
    for i in range(numkeys):
        if "->" in gatelist[i].name:
            gatez = gate.name.split('->')[0]
        else:
            gatez = gatelist[i].name
        file.write("INPUT(KEY" + str(i) + ")\n")
        op = random.choice(["XOR(", "XNOR("])
        keys.append(op)
        file.write("KEYGATE" + str(i) + " = " + str(op) + "KEY" + str(i) + ", " + str(gatez) + ")\n")
    file.close()




if __name__ == "__main__":
    readgates()
    for g in gatelist:
        print(g.name + " testa: " + str(g.testability))

    numkeys=3
    addgates(numkeys)

