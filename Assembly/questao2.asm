goto main
wb 0
r ww 1000
m ww 1
n ww 0
main rcv y, m
     inc
     rcv x, r
     sub x, m
     mov x, n
jz x, fdois
loop jz x, final
     inc
     mov y, r
     sqr r
     rcv w, r
     prim y 
     jz x, pulo
     rcv x, n
     sub x, m
     mov x, n
pulo inc
rcv x, n
goto loop
final mov y, r
rcv x, r
sub x, m
mov x, r
     halt
fdois mov y, r
halt