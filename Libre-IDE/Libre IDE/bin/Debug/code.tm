DEFINE:  x,int,0
DEFINE:  y,int,1
0: LD  6,0(0)
1: ST  0,0(0)
2: IN  0,0,0
3: ST  0,0(5)
4: LD  0,0(5)
5: OUT  0,0,0
6: LDC  0,*(0)
7: OUTLN  0,0,0
8: LDC  0,4(0)
9: ST  0,1(5)
10: LD  0,1(5)
11: ST  0,0(6)
12: LDC  0,0(0)
13: LD  1,0(6)
14: SUB  0,1,0
15: JNE  0,2(7)
16: LDC  0,0(0)
17: LDA  7,1(7)
18: LDC  0,1(0)
20: LD  0,1(5)
21: ST  0,0(6)
22: LDC  0,2(0)
23: LD  1,0(6)
24: SUB  0,1,0
25: JEQ  0,2(7)
26: LDC  0,0(0)
27: LDA  7,1(7)
28: LDC  0,1(0)
29:  JEQ  0,2(7)
31:  LDA  7,0(7)
32: LD  0,1(5)
33: OUT  0,0,0
34: LDC  0,*(0)
35: OUTLN  0,0,0
36: LD  0,0(5)
37: OUT  0,0,0
38: LDC  0,*(0)
39: OUTLN  0,0,0
40: LD  0,1(5)
41: ST  0,0(6)
42: LDC  0,1(0)
43: LD  1,0(6)
44: SUB  0,1,0
45: ST  0,1(5)
19:  JEQ  0,27(7)
30:  LDA  7,16(7)
46:  LDA  7,-37(7)
47: LD  0,0(5)
48: ST  0,0(6)
49: LDC  0,1(0)
50: LD  1,0(6)
51: SUB  0,1,0
52: ST  0,0(5)
53: LD  0,0(5)
54: ST  0,0(6)
55: LDC  0,0(0)
56: LD  1,0(6)
57: SUB  0,1,0
58: JEQ  0,2(7)
59: LDC  0,0(0)
60: LDA  7,1(7)
61: LDC  0,1(0)
62:  JEQ  0,-55(7)
63: HALT  0,0,0
