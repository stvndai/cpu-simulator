
opcodes = {
    0b0001 : "ADD",
    0b0010 : "SUB",
    0b0011 : "LOAD",
    0b0100 : "STORE",
    0b0101 : "JMP",
    0b0110 : "BEQ",
    0b0111 : "ADDI",
    0b1111 : "HALT"
    
}
    
class Cpu:
    def __init__(self):
        self.pc = 0
        
        file = open("instructionMemory.txt" ,"r") # instruction memory will just be a file.
        self.instructionMemory = [0]*1024
        self.dataMemory = [0] * 1024
        with open('instructionMemory.txt', 'r') as file:
            self.instructionMemory = [int(line, base=2) for line in file]

        
        self.currInstruction = None
        self.decoded = None
        self.aluOutput = None
        self.memOuput = None
        self.writeBackOuput = None

        self.registers = [0]*8 
        
        self.cycles = 0
        self.instructions_executed = 0
        self.running = True
        
    def fetch(self):
        """this fetech the next instruction from the instruction instruction memory"""
        if self.pc < len(self.instructionMemory):
            self.currInstruction = self.instructionMemory[self.pc]
        else:
            self.running = False
            return 1111000000000000
            
        print(self.currInstruction)
        self.pc += 1
        self.cycles += 1
        return self.currInstruction
        

    def decode(self, instruction):
        instr = instruction
        opcode = (instr >> 12) & 0xF
        
        self.decoded = {
            "opcode": opcode,
            "rd": (instr >> 9) & 0x7,
            "rs1": (instr >> 6) & 0x7,
            "rs2": (instr >> 3) & 0x7,
            "imm": instr & 0x3F,
        }
        
        opcode = self.decoded["opcode"]
        rd = self.decoded["rd"]
        rs1 = self.decoded["rs1"]
        rs2 = self.decoded["rs2"]
        imm = self.decoded["imm"]
        
        if imm & 0x20:
            imm -= 0x40
            
        control = {
            "opcode" : opcode,
            "rd" : rd,
            "rs1" : rs1,
            "rs2" : rs2,
            "imm" : imm,
            "regWrite" : False,
            "memRead" : False,
            "memWrite" : False,
            "branch" : False,
            "jump" : False,
            "aluSrcImm" : False,
            "aluOp" : None
        }
        
        if opcode == 0b0001: #ADD
            control["regWrite"] = True
            control["aluOp"] = "ADD"
        
        elif opcode == 0b0010: #SUB
            control["regWrite"] = True
            control["aluOp"] = "SUB"
        
        elif opcode == 0b0011: # LOAD
            control["regWrite"] = True
            control["memRead"] = True
            control["aluSrcImm"] = True
            control["aluOp"] = "ADD"
        
        elif opcode == 0b0100: # STORE
            control["memWrite"] = True
            control["aluSrcImm"] = True
            control["aluOp"] = "ADD"
        
        elif opcode == 0b0101: # JMP
            control["jump"] = True    
        
        elif opcode == 0b0110: # BEQ
            control["branch"] = True
            control["aluOp"] = "SUB"
        
        elif opcode == 0b0111: #ADDI
            control["regWrite"] = True
            control["aluSrcImm"] = True
            control ["aluOp"] = "ADD"
        
        elif opcode == 0b1111:  # HALT
            control["halt"] = True
        
        self.cycles += 1
        return control
            
    def execute(self, control):
        
        rs1 = self.registers[control["rs1"]]
        rs2 = self.registers[control["rs2"]]
        imm = control["imm"]
        
        operand2 = imm if control["aluSrcImm"] else rs2
        
        result = None

        if control["aluOp"] == "ADD":
            result = rs1 + operand2
        
        elif control["aluOp"] == "SUB":
            result = rs1 - operand2
        
        if control["branch"] and result == 0:
            self.pc = control["imm"]
        
        if control["jump"]:
            self.pc = self.currInstruction & 0xFFF
        
        self.cycles += 1
        return result    

            
    def memory(self, control, aluResult):
        if control["memRead"]:
            return self.dataMemory[aluResult]
        
        if control["memWrite"]:
            self.dataMemory[aluResult] = self.registers[control["rs2"]]
            
        self.cycles += 1
        return aluResult
        
    def writeBack(self, control, regVal):
        if control["regWrite"] == True:
            self.registers[control["rd"]] = regVal
            
        self.cycles += 1

    def cycle(self):
        instruction = self.fetch()
        control = self.decode(instruction)
        if control.get("halt"):
            self.running = False
            return
        
        aluResult = self.execute(control)
        memResult = self.memory(control, aluResult)
        self.writeBack(control, memResult)
        
        self.instructions_executed += 1
        
    def run(self):
        while self.running:
            self.cycle()

        print("Program finished.")
        print("Cycles:", self.cycles)
        print("Instructions:", self.instructions_executed)
        print("CPI:", self.cycles / self.instructions_executed)
        
    
cpu = Cpu()
cpu.run()