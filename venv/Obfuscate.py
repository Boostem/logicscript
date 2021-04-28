
class Node:
    def __init__(self, name):
        self.name = name
        self.sa0 = 0
        self.sa1 = 0



gates = [] #list of gates
names = [] #list of names
def main():
    with open("c17.fault") as f:
        for line in f:
            if "->" in line:
                continue
            data = line.split()

            if "gat" in data[0]:
                name = data[0]
                if name not in gates:
                    n = Node(name)
                    gates.append(n)
                else:
                    break

if __name__ == "__main__":
    main()