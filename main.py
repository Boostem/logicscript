
class Node:
    def __init__(self, name):
        self.name = name
        self.sa0 = 0
        self.sa1 = 0
        self.testability = 0

gatelist = []  # list of gates
names = []  # list of names


def gates():
    with open("c17.fault") as f:
        for line in f:
            # skip the wires, they are redundant and skip tests
            #if "->" in line:
            #    continue
            if "test" in line:
                continue
            if "*" not in line:
                continue

            data = line.split()
            print(data)

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
            else: #To keep compiler happy
                index = -1


# Function to calculate hamming distance
# https://www.geeksforgeeks.org/hamming-distance-between-two-integers/
def hd(n1, n2):
    x = n1 ^ n2
    setBits = 0
    while (x > 0):
        setBits += x & 1
        x >>= 1
    return setBits


if __name__ == "__main__":
    gates()
    for g in gatelist:
        print((g.name) + " test is: " + str(g.sa0 + g.sa1))

    #print(hd(0b0101, 0b1010))

'''import re
import numpy as np


class Node:
    def __init__(self, name, sa0, sa1):
        self.name = name
        self.sa0 = sa0
        self.sa1 = sa1
        self.testability = self.sa0 + self.sa1
nodes.sort(key=lambda node: node.testability, reverse=True)

class LogicObf:
    def __init__(self, netlist_filename, output_filename, num_keys):
        self.netlist_filename = netlist_filename
        self.output_filename = output_filename
        self.output_file = open(self.output_filename, "r")
        self.netlist_file = open(self.netlist_filename, "r")
        self.nodes = list()
        self.num_keys = num_keys

    def run(self):
        self.create_nodes()
        self.sort_nodes()
        self.add_key_gates()

    def create_nodes(self):
        for line in self.output_file:
            if line == '\n':
                break
            name = line.rstrip()
            next(self.output_file)
            next(self.output_file)
            sa0 = int(next(self.output_file).split("T(sa0): ")[1].rstrip())
            sa1 = int(next(self.output_file).split("T(sa1): ")[1].rstrip())
            self.nodes.append(Node(name, sa0, sa1))

    def sort_nodes(self):
        nodes = self.nodes
        nodes.sort(key=lambda node: node.testability, reverse=True)
        self.nodes = nodes

    def get_nodes(self):
        return self.nodes

    def add_key_gates(self):
        file = self.netlist_file.readlines()
        for i in range(self.num_keys):
            file.append('INPUT(key' + str(i) + ')')
            node = self.nodes[i]
            if '_' in node.name:
                keygate_input = node.name.split('_')[0]
                keygate_output = node.name.split('_')[1].split('[')[1].split(']')[0]
                keygate_type = np.random.choice(['XOR', 'XNOR'])
                file.append('keygate' + str(i) + ' = ' + keygate_type + '(key' + str(i) + ', ' + keygate_input + ')')
                # modify the line to take keygate as input
                for line in range(len(file)):
                    if file[line].split('=')[0].split(' ')[0] == keygate_output:
                        match = keygate_input + "(?P<character>\,|\))"
                        regex = re.compile(r"" + match)
                        file[line] = regex.sub(r"" + "keygate" + str(i) + "\g<character>", file[line])
                        break
            else:
                keygate_type = np.random.choice(['XOR', 'XNOR'])
                keygate_input = node.name.split(':')[0]
                for line in range(len(file)):
                    match = keygate_input + "(?P<character>\,|\))"
                    regex = re.compile(r"" + match)
                    file[line] = regex.sub(r"" + "keygate" + str(i) + "\g<character>", file[line])
                file.append('keygate' + str(i) + ' = ' + keygate_type + '(key' + str(i) + ', ' + keygate_input + ')')
        with open(self.netlist_filename.split('.')[0] + "_obf.bench", 'w') as f:
            for line in file:
                f.write("%s\n" % line.upper())


def main():
    logic_obf = LogicObf("c1196.bench", "c1196_SCOAP_Output.txt", 30)
    logic_obf.run()
    nodes = logic_obf.get_nodes()


if __name__ == "__main__":
    main()'''

'''class Node:
    def __init__(self, name):
        self.name = name
        self.sa0 = 0
        self.sa1 = 0

tests = []
nodes = []
nodenames = [] #list of names for checking
def main():
    left = 0b1111
    right= 0b1011
    new = left ^ right
    count=0
    while(new):
        print(count)
        count = count + (new & 1)
        new>>=1
    print(count)
    with open("c17.fault") as f:
        for line in f:
            if "->" in line:
                continue
            data = line.split()
            #print(data)
            if data[0] == "test":
                print("")
                #print("test: " + data[1] + " with output: " + data[3])

            if "gat" in data[0]:
                name = data[0]
                if name not in nodenames:
                    n = Node(name)
                else:
                    break
                if "*" in data[2]:
                    if "/0" in data[1]:
                        n.sa0 += 1
                        #print(name + " is stuck at 0 with output " + data[3])
                    elif "/1" in data[1]:
                        n.sa1 += 1
                        #print(name + " is stuck at 1 with output " + data[3])
                nodes.append(n)



   for no in nodes:
        print(no.name)
        print(no.sa0)
        print(no.sa1)



if __name__ == "__main__":
    main()'''
