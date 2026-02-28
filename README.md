# cpu-simulator

A software simulation of a 16-bit RISC-style CPU written in Python.  
This project models instruction decoding, control signals, ALU operations, memory access, and optional pipelining.

---

#

- 16-bit fixed-width instruction format
- R-type, I-type, and memory instructions
- Sign-extended immediates
- Register file simulation
- Instruction and data memory
- Control signal generation
- Optional 5-stage pipeline simulation
- CPI calculation (pipelined vs non-pipelined) (piplined not addded yet)

---

## Instruction Set Architecture

| Opcode | Instruction | Type |
|--------|------------|------|
| 0001   | ADD        | R    |
| 0010   | SUB        | R    |
| 0011   | LOAD       | I    |
| 0100   | STORE      | I    |
| 0101   | JMP        | J    |
| 0110   | BEQ        | I    |
| 0111   | ADDI       | I    |
| 1111   | HALT       | -    |

---

## 🏗 Architecture Overview

The CPU is composed of:

- **Program Counter (PC)**
- **Instruction Memory**
- **Register File (8 registers)**
- **ALU**
- **Control Unit**
- **Data Memory**

Execution follows:

1. Fetch
2. Decode
3. Execute
4. Memory
5. Write-back

---
Example output

<img width="264" height="143" alt="image" src="https://github.com/user-attachments/assets/31cb4f60-791d-4c71-af04-020cbdb8be27" />

---

## To be added
Piplining to compare with non-piplined CPI
Better output to visualize each instruction
