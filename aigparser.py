import re

class Parser:
    def __init__(self,file):
        self.fin = file
        self.fout = open(self.fin.name.rstrip("aag") + "hll", "w")
        self.M = 0
        self.I = 0
        self.L = 0
        self.O = 0
        self.A = 0
        self.B = 0
        self.C = 0
        self.J = 0
        self.F = 0
        self.dictionary = []
        self.input = []
        self.output = []
        self.ands = []
        self.latch = []
        self.invconstraint = []
        self.badstate = []
        self.fair = []
        self.justice = []
        self.comments = []

    def iterator(self):
        iterator = iter(self.fin)
        return iterator

    def parseHead(self,iterator):
        text = next(iterator)
        reg = re.compile(r"(aag|aig)\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s(\d+)\s(\d+)")
        match = reg.match(text)
        print(text)
        self.M = int(match.group(2))
        self.I = int(match.group(3))
        self.L = int(match.group(4))
        self.O = int(match.group(5))
        self.A = int(match.group(6))
        self.B = int(match.group(7))
        self.C = int(match.group(8))
        self.J = int(match.group(9))
        self.F = int(match.group(10))
        return iterator

    def parseInput(self,iterator):
        reg = re.compile(r"(\d+)")
        for i in range(0,self.I,1):
            text = next(iterator)
            print("input: "+text)
            match = reg.match(text)
            self.input.append(int(match.group(0)))
        return iterator


    def parseLatch(self,iterator):
        reg = re.compile(r"(\d+)\s(\d+)\s(\d+)?")
        for i in range(0, self.L, 1):
            text = next(iterator)
            match = reg.match(text)
            print("latch: " + text)
            try:
                self.latch.append([int(match.group(1)),int(match.group(2)),int(match.group(3))])
            except:
                self.latch.append([int(match.group(1)), int(match.group(2)),0])
        return iterator

    def createDictionary(self):
        self.dictionary = [None]*(2*(self.M)+2)
        self.dictionary[0] = "False"
        self.dictionary[1] = "True"

    def completeDictionary(self):
        for i in range(1, self.M+1, 1):
            if self.dictionary[2*i] is None:
                self.dictionary[2*i] = "a"+str(i)
                self. dictionary[2*i+1] = "~a"+str(i)


    def parseOutput(self, iterator):
        reg = re.compile(r"(\d+)")
        for i in range(0, self.O, 1):
            text = next(iterator)
            print("output: " + text)
            match = reg.match(text)
            self.output.append(int(match.group(0)))
        return iterator

    def parseAnd(self, iterator):
        reg = re.compile(r"(\d+)\s(\d+)\s(\d+)")
        for i in range(0,self.A,1):
            text = next(iterator)
            print("and: " + text)
            match = reg.match(text)
            self.ands.append([int(match.group(1)),int(match.group(2)),int(match.group(3))])
        return iterator

    def parseInvariant(self, iterator):
        reg = re.compile(r"(\d+)")
        for i in range(0, self.C, 1):
            text = next(iterator)
            print("invar: " + text)
            match = reg.match(text)
            self.invconstraint.append(int(match.group(0)))
        return iterator

    def parseBadstate(self, iterator):
        reg = re.compile(r"(\d+)")
        for i in range(0, self.B, 1):
            text = next(iterator)
            print("bad state: " + text)
            match = reg.match(text)
            self.badstate.append(int(match.group(0)))
        return iterator

    def parseFairness(self, iterator):
        for i in range(0, self.F, 1):
            text=next(iterator)
            self.fair.append(text)
        return iterator


    def parseJustice(self,iterator):
        for i in range(0, self.J, 1):
            text=next(iterator)
            self.justice.append(text)
        return iterator


    def parseSymbol(self, symbol):
        #text = next(iterator)
        #print(text)
        reg = re.compile(r"([ilo])(\d+)\s(\w+)")
        match = reg.match(symbol)
        index = int(match.group(2))
        if match.group(1) == "i":
            a = int(self.input[index])
            print(a)
            self.dictionary[a]=match.group(3)
            self.dictionary[a+1]="~"+match.group(3)
        elif match.group(1) == "o":
            self.dictionary[self.output(match.group(2))] = match.group(3)
            self.dictionary[self.output(match.group(2)) + 1] = "~" + match.group(3)
        elif match.group(1) == "l":
            self.dictionary[self.latch(match.group(2))[0]] = match.group(3)
            self.dictionary[self.latch(match.group(2)[0]) + 1] = "~" + match.group(3)


    def parseComments(self,iterator):
        text=next(iterator)
        self.comments.append(text)
        return iterator



    def writeInput(self):
        self.fout.write("input:\n")
        for i in self.input:
            self.fout.write("bool "+self.dictionary[i]+";\n")

    def writeDeclarations(self):
        self.fout.write("declatations:\n")
        for i in self.ands:
            self.fout.write("bool "+self.dictionary[i[0]]+";\n")
        for i in self.latch:
            self.fout.write("bool "+self.dictionary[i[0]]+";\n")


    def writeDefinitions(self):
        self.fout.write("Definitions:\n")
        for i in self.ands:
            self.fout.write(self.dictionary[i[0]]+" := "+self.dictionary[i[1]]+" & "+self.dictionary[i[2]]+";\n")
        for i in self.latch:
            if i[2] == 1:
                self.fout.write(self.dictionary[i[0]]+":= true, "+self.dictionary[i[1]]+";\n")
            elif i[2] == 0:
                self.fout.write(self.dictionary[i[0]] + ":= false, " + self.dictionary[i[1]]+";\n")
            elif i[2] == i[1]:
                self.fout.write(self.dictionary[i[0]] + ":= Nil, " + self.dictionary[i[1]]+";\n")



    def writeOutputs(self):
        self.fout.write("Outputs:\n")
        for i in self.output:
            self.fout.write(self.dictionary[i]+";\n")


    def writeProofObl(self):
        self.fout.write("Proof Obligations:\n")
        for i in self.invconstraint:
            self.fout.write(self.dictionary[i]+";\n")
        for i in self.badstate:
            self.fout.write("~"+self.dictionary[i]+";\n")

    def parseExtra(self, iterator):
        text = next(iterator)
        while text != "c":
            self.parseSymbol(text)
            text = next(iterator)
        for line in fin:
            iterator = parseComments(iterator)

def parse(parser):
    iterator = parser.iterator()
    iterator = parser.parseHead(iterator)
    parser.createDictionary()
    iterator = parser.parseInput(iterator)
    iterator = parser.parseLatch(iterator)
    iterator = parser.parseOutput(iterator)
    iterator = parser.parseBadstate(iterator)
    iterator = parser.parseInvariant(iterator)
    #iterator = parser.parseFairness(iterator)
    #iterator = parser.parseJustice(iterator)
    iterator = parser.parseAnd(iterator)
    parser.parseExtra(iterator)
    parser.completeDictionary()

def write(parser):
    parser.writeInput()
    parser.writeDeclarations()
    parser.writeDefinitions()
    parser.writeOutputs()
    parser.writeProofObl()


def main():
    f = open("test.aag")
    pop = Parser(f)
    parse(pop)
    write(pop)

main()
