\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  0 C4 + 0 C5
Subject To
 R0: - 1.2 C0 + 0.5 C1 - 1.2 C2 + 0.5 C3 + C6 = 2
 R1: - 9.2 C0 + 3.1 C1 - 9.2 C2 + 3.1 C3 + C7 = 1.2
 R2: 0.45 C8 - 3.5 C9 + C10 = 0.9
 R3: C0 = 0
 R4: C1 = 0.38
Bounds
General Constraints
 GC0: C8 = MAX ( C6 , 0 )
 GC1: C9 = MAX ( C7 , 0 )
End
