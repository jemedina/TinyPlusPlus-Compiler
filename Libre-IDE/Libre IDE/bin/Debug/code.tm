DEFINE:  num1,int,0
DEFINE:  num2,int,1
DEFINE:  num3,int,2
DEFINE:  x,int,3
DEFINE:  t,boolean,4
DEFINE:  f,boolean,5
0: LD  6,0(0)
1: ST  0,0(0)
2: LDC  0,1(0)
3: ST  0,4(5)
4: LDC  0,0(0)
5: ST  0,5(5)
6: IN  0,0,0
7: ST  0,0(5)
8: IN  0,0,0
9: ST  0,1(5)
10: IN  0,0,0
11: ST  0,2(5)
12: LD  0,0(5)
13: ST  0,0(6)
14: LD  0,1(5)
15: LD  1,0(6)
16: MUL  0,1,0
17: ST  0,3(5)
18: LD  0,3(5)
19: ST  0,0(6)
20: LD  0,2(5)
21: LD  1,0(6)
22: SUB  0,1,0
23: JEQ  0,2(7)
24: LDC  0,0(0)
25: LDA  7,1(7)
26: LDC  0,1(0)
28: LD  0,4(5)
29: OUT  0,0,0
27:  JEQ  0,3(7)
31: LD  0,5(5)
32: OUT  0,0,0
30:  LDA  7,2(7)
33: HALT  0,0,0
