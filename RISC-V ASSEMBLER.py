dic_format={"add":"R","sub":"R","sll":"R","slt":"R","sltu":"R","xor":"R","srl":"R","sra":"R","or":"R","and":"R",
           "lw":"I","addi":"I","slti":"I","sltiu":"I","xori":"I","ori":"I","andi":"I","slli":"I","srli":"I","srai":"I","lb":"I","lh":"I","lbu":"I","lhu":"I","jalr":"I","sw":"S","sb":"S","sh":"S","AUIPC":"U","lui":"U","beq":"SB","bnq":"SB","blt":"SB","bge":"SB","bltu":"SB","bgeu":"SB","jal":"UJ"}
op=''
RestOfInst=[]
type_of_format=''
RestOfInst=''
regsters_nums=[]
Imm=''
VV={}
Imm_line=''
outputArray=[]
inputName=input("Please Enter input file name to read")
outputName= input("Please Enter output file name to create and write data in")



def decimalToBinary(i,Bits):  # a method used to convert decimal numbers to binary to a chosen number of bytes
    S=bin(i)
    L=S[2:].zfill(Bits)
    return L

def CatchingLabels(fileName):
    count=0
    for L in FileData:
        count += 1

        if (':' in L):
            Line = L.replace(':', ' ')  # to clear the semi column of the label
            Splited = Line.split()  # spliting the line into a list
            Label = Splited[0]  # catching the label
            VV[Label] = count  # storing the label with its address in a dictionary for later use

    count = 0  # reset the value of the counter for later use

def ReplacingBows(List):       # a method used to clear Bows form the instructions
    temp= [x.replace('(', ' ') for x in List]
    X= [x.replace(')', '') for x in temp]
    return X

def ReplacingStackPointer(RestOfInst):   # a method specified for replacing the stack pointer
    temp= [x.replace('(sp)', ' 2') for x in RestOfInst]

    temp2=[x.replace('sp', ' 2') for x in temp]

    return temp2


def RemoveComments(comment):   # a method used to delete comments if any occurred
    for x in comment:

        if '#' in x:   # if '#' detected ( # used in the simulator RARS to comment lines )
            start=x
            index= comment.index(start)
            R=comment[0:index]
            #remove = comment[index:]
            #R = [x for x in comment if x not in remove]   # i tried to use list comprehension but it will
                                                           #  cause a problem if any part of the instruction
                                                           # occued in the comment and it will delete both
            return R


def UJ_type():  # method used to handle the the JALR instruction
    dic_op={'UJ':'1101111'}
    rd = regsters_nums[0]
    Imm = regsters_nums[1]
    value = ((VV.get(Imm)) * 4 - Imm_line * 4)

    if value < 0:
        value = str(value).replace('-', '')
        value = decimalToBinary(int(value),20)
        value = list(value)
        value[0] = '1'
        value = ''.join(value)
        value=decimalToBinary(int(value),20)

        outputArray.append(value[0]+ value[10:]+ value[9]+ value[1:9]+ decimalToBinary(int(rd), 5)+
              dic_op.get(type_of_format))

    else:
        value = decimalToBinary(int(value),20)

        outputArray.append(value[0] + value[10:20] + value[9] + value[1:9] + decimalToBinary(int(rd), 5)+
              dic_op.get(type_of_format))


def SB_type():
    dic_op={"SB":"1100011"}
    dic_func3={"beq":"000","bne":"001","blt":"100","bge":"101","bltu":"110","bgeu":"111"}

    rs1 = regsters_nums[0]
    rs2=regsters_nums[1]
    Imm= regsters_nums[2]
    value=((VV.get(Imm))*4 -Imm_line*4 )   # to determine the value of the branch

    if value<0:   # if the value of the branch is negative (mostly a loop)
        value= str(value).replace('-','')
        Value=int(value)
        Value=decimalToBinary(Value,12)
        Value=list(Value)
        Value[0]='1'
        Value=''.join(Value)

        outputArray.append(Value[1]+Value[2:7]+decimalToBinary(int(rs2),5)+decimalToBinary(int(rs1),5)+dic_func3.get(op)+
                           Value[7:11]+Value[0]+dic_op.get(type_of_format))
    else:

        value = decimalToBinary(value, 12)

        outputArray.append(value[0]+ value[2:8]+ decimalToBinary(int(rs2), 5)+ decimalToBinary(int(rs1), 5)+ dic_func3.get(op)+
              value[8:12]+ value[1]+ dic_op.get(type_of_format))


def I_type():
    dic_op={"lw":"0000011","addi":"0010011","lb":"0000011","lh":"0000011","slti":"0010011","sltiu":"0010011","xori":"0010011","ori":"0010011","andi":"0010011","slli":"0010011","srli":"0010011","srai":"0010011","lbu":"0000011","lhu":"0000011","jalr":"1100111"}
    dic_fun3={"lw":"010","addi":"000","lb":"000","lh":"001","slti":"010","sltiu":"011","xori":"100","ori":"110","andi":"111","slli":"001","srli":"101","srai":"101","lbu":"100","lhu":"101","jalr":"000"}
    dic_left7bits= {"slli":"0000000","srli":"0000000","srai":"0100000"}

    if (op in dic_left7bits):  # to determine if it is a shift instruction
        rd = regsters_nums[0]
        rs1 = regsters_nums[1]
        shamt = regsters_nums[2]
        outputArray.append(dic_left7bits.get(op)+decimalToBinary(int(shamt),5)+
                           decimalToBinary(int(rs1),5)+dic_fun3.get(op)+decimalToBinary(int(rd),5)+dic_op.get(op))


    elif(dic_op.get(op) == '0000011' ):  # for load instruction

        inst=ReplacingBows(regsters_nums)  # replacing the bows to deal with raw numbers
        rd=inst[0]
        address=inst[-1].split()  # splitting the immediate from the register
        rs1=address[1]
        Immediate=address[0]
        outputArray.append(decimalToBinary(int(Immediate),12)+
                           decimalToBinary(int(rs1), 5)+ dic_fun3.get(op)+ decimalToBinary(int(rd), 5)+ dic_op.get(op))

    elif(dic_op.get(op)=='1100111'):   # for jump and link registers

        inst = ReplacingBows(regsters_nums)  # replacing the bows to deal with raw numbers
        rd = inst[0]
        address = inst[-1].split()  # splitting the immediate from the register
        rs1 = address[1]
        Immediate = address[0]
        outputArray.append(
            decimalToBinary(int(Immediate), 12) + decimalToBinary(int(rs1), 5) + dic_fun3.get(op) + decimalToBinary(
                int(rd), 5) + dic_op.get(op))

    else:
        rd = regsters_nums[0]
        rs1 = regsters_nums[1]
        Immediate = regsters_nums[2]
        if int(Immediate)<0:       #if the number is negitve change the most significant bit to 1
            Immediate = str(Immediate).replace('-', '')
            Immediate = decimalToBinary(int(Immediate),12)
            Immediate = list(Immediate)
            Immediate[0] = '1'
            Immediate = ''.join(Immediate)
        else:
         Immediate = decimalToBinary(int(Immediate), 12)
        outputArray.append(Immediate+ decimalToBinary(int(rs1), 5)+
                           dic_fun3.get(op)+ decimalToBinary(int(rd), 5)+ dic_op.get(op))


def U_type():   # a method specified for the U-type instructions

    dic_op={"lui":"0110111","AUIPC":"0010111"}
    rd = regsters_nums[0]
    Imm= regsters_nums[1]
    outputArray.append(decimalToBinary(int(Imm),20)+decimalToBinary(int(rd),5)+dic_op.get(op))


def S_type():   # a method specified for the store instruction
    dic_op={"S":"0100011"}
    dic_func3={"sw":"010","sb":"000","sh":"001"}

    Inst = ReplacingBows(regsters_nums)  # clearing the bows by the method mentioned earlier
    Address=Inst[-1].split()   # Splitting rs1 form the offset
    rs2=Inst[0]
    rs1=Address[1]
    Imm=Address[0]
    Imm_Int = decimalToBinary(int(Imm),12)  # converting dicimal value to binary the splitting it into
    Imm_5=Imm_Int[7:]                         # two variables
    Imm_7=Imm_Int[0:7]

    outputArray.append(Imm_7+decimalToBinary(int(rs2),5)+
                       decimalToBinary(int(rs1),5)+dic_func3.get(op)+Imm_5+dic_op.get(type_of_format))


def R_type():  # a method specified for the Arithmetic instructions
    dic_op = {"R":"0110011"}
    dic_fun3 = {"add": "000","sub":"000","sll":"001","slt":"010","sltu":"011","xor":"100","srl":"101","sra":"101","or":"110","and":"111"}
    dic_fun7 = {"add": "0000000","sub":"0100000","sll":"0000000","slt":"0000000","sltu":"0000000","xor":"0000000","srl":"0000000","sra":"0100000","or":"0000000","and":"0000000"}
    rd= regsters_nums[0]
    rs1=regsters_nums[1]
    rs2= regsters_nums[2]
    outputArray.append(dic_fun7.get(op)+decimalToBinary(int(rs2),5)+decimalToBinary(int(rs1),5)+dic_fun3.get(op)+decimalToBinary((int(rd)),5)+dic_op.get(type_of_format))



print("Reading file "+ inputName)     # enter the name of the file that containg the assembly code


f=open(inputName,'r')     #opening the file and storing the data then closing it
FileData=f.read().splitlines()
print(FileData)
f.close()
count=0


CatchingLabels(FileData)  # catching the labels in the asssmebly code if in and storing
                           # them in a dictionary with the lined they in

for ln in FileData:
      count+=1
      NoComma = ln.replace(',', ' ')

      if ':' in NoComma:   # removing labels if any and store opcode and the rest of the instruction
            NoComma=NoComma.replace(':',' ')
            Splited_line= NoComma.split()
            Splited_line.pop(0)
            op = Splited_line[0]
            RestOfInst = Splited_line[1:]


      else:   # if no labels occurred
           Splited_line=NoComma.split()
           op=Splited_line[0]
           RestOfInst=Splited_line[1:]


      if(op in dic_format):   # get the typre of the format from the opcode
         type_of_format=dic_format.get(op)
      else:
        print("this type of operation doesn't exist in line check  " + str(count))
        exit()

      if ('sp' or '(sp)' in RestOfInst): # replca stack pointer by its register value (2)

        RestOfInst=ReplacingStackPointer(RestOfInst)

      for x in RestOfInst:
         if ('#' in x):  #check for comments and remove if any

            RestOfInst=RemoveComments(RestOfInst)

      for x in RestOfInst:
        regsters_nums = []  # fleching the registers numbers of the previous instruction

        for i in RestOfInst:
            regsters_nums.append(i.replace('x',''))  # clearing the 'x' from the registers
                                                       #so we can deal with raw numbers

          # a method specified for each format
        if(type_of_format=='R'):
           R_type()
        elif (type_of_format=='I'):
           I_type()
        elif(type_of_format=="S"):
           S_type()
        elif(type_of_format=="U"):
           U_type()
        elif(type_of_format=="SB"):
           Imm_line=count    # storing the value of the branch instruction to calculate the jump
           SB_type()
        elif(type_of_format=="UJ"):
           Imm_line=count    # storing the value of the branch instruction to calculate the jump
           UJ_type()



        break

print("Writing results in file "+ outputName)   #outpiting the result into a file by a chosen name from the user
outputfile = open(outputName,"w+")
for i in range(len(outputArray)):
    outputfile.write(outputArray[i] + "\n")
outputfile.close()
print("Done reading and writing files successfully...")







