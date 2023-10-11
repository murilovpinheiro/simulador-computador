goto inicio
wb 0

e ww 2204
a ww 400
b ww 100
c ww 3
d ww 0

inicio rcv x, e
mov x, d
rcv x, a
div x, d
rcv x, e
jz x, bis

rcv x, b
div x, d
rcv x, e
jz x, nbis

rcv x, c
and x, d
jz x, bis

nbis z
mov x, e
halt

bis u
mov x, e
halt