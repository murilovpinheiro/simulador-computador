# Equipe:
# Guilherme de Menezes Furtado
# Murilo Vinicius Almeida Pinheiro

import sys

fsrc = open(str(sys.argv[1]), 'r')
#abrindo o arqivo

lines = []
#lines é basicamente as linhas tratadas
lines_bin = []
#lines_bin são as linhas codificadas
#(VALOR DA INSTRUÇÃO, [VETOR com os OPERANDOS]) //os operandos são salvos em char, com 32 bits
# para WW = (0000,0000,0000,0000) -> word
names = []
#(NOME, BYTES até o NOME (equivale ao endereço onde está o valor na memória))

instructions = ['add', 'sub', 'goto', 'mov', 'jz', 'halt', 'wb', 'ww', 'min', 'div', 'z', 'u', 'sqr', 'and', 'prim', 'rcv', 'inc', 'dec']
instruction_set = {'add' : 0x02, 
                   'sub' : 0x0D, 
                   'goto': 0x09, 
                   'mov' : 0x06, 
                   'jz'  : 0x0B,
                   'min' : 0x19,
                   'div' : 0x23,
                   'sqr' : 0x40,
                   'and' : 0x51,
                   'prim': 0x56,
                   'rcv' : 0x67,
                   'z'   : 0x34,
                   'u'   : 0x35,
                   'inc' : 0x75,
                   'dec' : 0x79, 
                   'halt': 0xFF}
#instructions são as instruções, ou melhor o nome delas
#o instruction set tem a instrução e o número da MI equivalente

def is_instruction(str):
  #checa se uma String está nas lista de instruções aceitas
   global instructions
   inst = False
   for i in instructions:
      if i == str:
         inst = True
         break
   return inst
   
def is_name(str):
  #checa se uma String é um nome, nome são os nomes q nós atribuimos no assembly
  #atribuimos nomes para as linhas, por exemplo, na hora de pular e em loops
   global names
   name = False
   for n in names:
      if n[0] == str:
         name = True
         break
   return name
   
def encode_2ops(inst, ops): #add, jz, sub, min, div, and, z, u
  #essa função é para instruções com "dois parametros" por exemplo Add x, b
  #nesse caso o parametro 1 é x e o 2 é b
   line_bin = []
  #line_bin aparamente é a saída dessa função
   if len(ops) > 1:
     #se há mais de duas opções
      if ops[0] == 'x':
        #checa o primeiro parametro se é um parametro válido
         if is_name(ops[1]):
           #checa se o segundo parametro está nos nomes dados aos espaços de
           #memória anteriormente
            line_bin.append(instruction_set[inst])
            line_bin.append(ops[1])

           #se for tudo certo ele adiciona o valor equivalente a instrução digitada
           #e coloca logo em seguida o parametro 2

   return line_bin

def encode_goto(ops):
  #muito parecida com a de cima, mas é especifica pro goto e devolve pro goto
   line_bin = []
   if len(ops) > 0:
      if is_name(ops[0]):
         line_bin.append(instruction_set['goto'])
         line_bin.append(ops[0])

   return line_bin
def encode_inc():
   line_bin = []
   line_bin.append(instruction_set['inc'])
   return line_bin

def encode_mov(ops):
  #nesse caso o parametro 1 é x e o 2 é b
   line_bin = []
  #line_bin aparamente é a saída dessa função
   if len(ops) > 1:
     #se há mais de duas opções
      if ops[0] == 'x':
         if is_name(ops[1]):
          line_bin.append(instruction_set['mov'])
          line_bin.append(ops[1])
      if ops[0] == 'mdr':
         if is_name(ops[1]):
          line_bin.append(instruction_set['mov'] + 17)
          line_bin.append(ops[1])
      if ops[0] == 'y':
         if is_name(ops[1]):
          line_bin.append(instruction_set['mov'] + 112)
          line_bin.append(ops[1])
           #AS SOMAS FEITAS NESSES IFS SÃO PARA CORRESPONDER A MI EQUIVALENTE AO MOV Y E A MOV MDR
           #ALGUMAS OUTRAS FUNÇÕES FAZEM O MESMO
           
   return line_bin
def encode_dec(ops):
  #nesse caso o parametro 1 é x e o 2 é b
   line_bin = []
  #line_bin aparamente é a saída dessa função
   if len(ops) > 1:
     #se há mais de duas opções
      if ops[0] == 'mem':
         if is_name(ops[1]):
          line_bin.append(instruction_set['dec'] + 1)
          line_bin.append(ops[1])
      if ops[0] == 'y':
         if is_name(ops[1]):
          line_bin.append(instruction_set['dec'])
          line_bin.append(ops[1])
   return line_bin
def encode_prim(ops):
  #nesse caso o parametro 1 é x e o 2 é b
   line_bin = []
   line_bin.append(instruction_set['prim'])
   return line_bin

def encode_sqr(ops):
   line_bin = []
   if len(ops) > 0:
      if is_name(ops[0]):
         line_bin.append(instruction_set['sqr'])
         line_bin.append(ops[0])
   return line_bin

def encode_rcv(ops):
  #nesse caso o parametro 1 é x e o 2 é b
   line_bin = []
  #line_bin aparamente é a saída dessa função
   if len(ops) > 1:
     #se há mais de duas opções
      if ops[0] == 'x':
         if is_name(ops[1]):
          line_bin.append(instruction_set['rcv'])
          line_bin.append(ops[1])
      if ops[0] == 'w':
         if is_name(ops[1]):
          line_bin.append(instruction_set['rcv'] + 3)
          line_bin.append(ops[1])
      if ops[0] == 'pc':
         if is_name(ops[1]):
          line_bin.append(instruction_set['rcv'] + 6)
          line_bin.append(ops[1])
      if ops[0] == 'y':
         if is_name(ops[1]):
          line_bin.append(instruction_set['rcv'] + 11)
          line_bin.append(ops[1])

   return line_bin
def encode_z():
   line_bin = []
   line_bin.append(instruction_set['z'])
   return line_bin
  
def encode_u():
   line_bin = []
   line_bin.append(instruction_set['u'])
   return line_bin
def encode_halt():
   line_bin = []
   line_bin.append(instruction_set['halt'])
   return line_bin
   
def encode_wb(ops):
  #encode para o wb, escreve no byte, utilizada no começo pra zerar o byte 0, só escreve números de 1 byte, ou seja menores que 256
   line_bin = []
   if len(ops) > 0:
      if ops[0].isnumeric():
         if int(ops[0]) < 256:
            line_bin.append(int(ops[0]))
   return line_bin   

def encode_ww(ops):
  #write_word na memória
   line_bin = []
   if len(ops) > 0:
     #checa se tem um parametro valido
      if ops[0].isnumeric():
         val = int(ops[0])
     #checa se é número e depois se é um número de 32bits
         if val < pow(2,32):
           #divide o valor em 4 bytes e depois retorna o resultado
            line_bin.append(val & 0xFF)
            line_bin.append((val & 0xFF00) >> 8)
            line_bin.append((val & 0xFF0000) >> 16)
            line_bin.append((val & 0xFF000000) >> 24)
   return line_bin
      
def encode_instruction(inst, ops):
  #checa uma instrução e envia o equivalente pra função que codifica os específicos
   if inst == 'add' or inst == 'sub' or inst == 'min' or inst == 'jz' or inst == 'and' or inst == 'div':
      return encode_2ops(inst, ops)
   elif inst == 'goto':
      return encode_goto(ops)
   elif inst == 'mov':
      return encode_mov(ops)
   elif inst == 'prim':
      return encode_prim(ops)
   elif inst == 'sqr':
      return encode_sqr(ops)
   elif inst == 'rcv':
      return encode_rcv(ops)
   elif inst == 'halt':
      return encode_halt()
   elif inst == 'wb':
      return encode_wb(ops)
   elif inst == 'inc':
      return encode_inc()
   elif inst == 'dec':
      return encode_dec(ops)
   elif inst == 'ww':
      return encode_ww(ops)
   elif inst == 'z':
      return encode_z()
   elif inst == 'u':
      return encode_u()
   else:
      return []
   
   
def line_to_bin_step1(line):
   line_bin = []
   if is_instruction(line[0]):
     #se a primeira parte da instrução for uma instrução
      line_bin = encode_instruction(line[0], line[1:])
      #se for ele pega, coloca em line[0] a string da instrução
      #esse 1: basicamente pega 1 e tudo depois dele e faz uma sublista
      #ou seja line[1:] ele tá pegando todas as OPS
   else:
     #basicamente faz o mesmo acima mas pulaa primeira STRING da linha

      line_bin = encode_instruction(line[1], line[2:])
    #acredito q esse if else é pra pular os NOMES das LINHAS
   return line_bin
   
def lines_to_bin_step1():
   global lines
   for line in lines:
      line_bin = line_to_bin_step1(line)
      if line_bin == []:
         print("Erro de sintaxe na linha ", lines.index(line))
         return False
      lines_bin.append(line_bin)
    #basicamente roda todas as linhas e faz o line_bin pra todos
    #se line_bin for vazio quer dizer que não encontrou uma inst equivalente então erro
   return True

def find_names():
  #captura os nomes das linhas
   global lines
   for k in range(0, len(lines)):
      is_label = True
      for i in instructions:
        #se a primeira string da linha for uma instrução, quer dizer q não é um nome então não adiciona em nomes
          if lines[k][0] == i:
             is_label = False
             break
      if is_label:
        #se for um nome, ele adiciona na lista de nomes, o nome e o número da linha
         names.append((lines[k][0], k))
         
def count_bytes(line_number):
   line = 0
   byte = 1
   while line < line_number:
     #byte += tamamnho de todas as lines_bin até uma linha x-1, lines_bin são basicamente
     #(número da microinstrução, [PARAMETROS]) #se não me engano os parametros ainda são letras e não números
      byte += len(lines_bin[line])
     #byte += tamanho em bytes, de linha I codificada
      line += 1
   return byte
  #byte = números de bytes até a linha x-1
  #essa função foi a unica q eu não entendi muito bem

def get_name_byte(str):
   for name in names:
     #para todos os nomes
      if name[0] == str:
        #se nome == a str, retorna o byte onde está o nome? ou o nome em bytes?
         return name[1]
         
def resolve_names():
   for i in range(0, len(names)):
     #para cada nome
     #names[i][1] antes do count_bytes é igual a linha onde está names[i]
      names[i] = (names[i][0], count_bytes(names[i][1]))
     #names[i][1] dps do count_bytes é igual ao espaço da memória equivalente ao nome em bytes
   for line in lines_bin:
     #para cada linha codificada
      for i in range(0, len(line)):
        #roda toda a linha
         if is_name(line[i]):
           #se um valor da linha for um nome
            if line[i-1] == instruction_set['add'] or line[i-1] == instruction_set['sub'] or line[i-1] == instruction_set['mov'] or line[i-1] ==instruction_set['min'] or line[i-1] == instruction_set['div'] or line[i-1] == instruction_set['sqr'] or line[i-1] == instruction_set['prim'] or line[i-1] == instruction_set['and'] or line[i-1] == instruction_set['rcv'] or line[i-1] == instruction_set['dec'] or line[i-1] == instruction_set['rcv']+3 or line[i-1] == instruction_set['rcv']+6 or line[i-1] == instruction_set['rcv']+11 or line[i-1] == instruction_set['mov']+17 or line[i-1] == instruction_set['mov']+112:
              #se o valor antes do nome for uma instrução de dois operandos, fiz de cada um das instruções que recebem espaços de memorias
               
               line[i] = get_name_byte(line[i])//4
              #vai capturar o valor o tamanho em word
            else:
              #se não for captura o valor em bytes
               line[i] = get_name_byte(line[i])

for line in fsrc:
  #por cada linha no .asm
   tokens = line.replace('\n','').replace(',','').lower().split(" ")
  #retira os \n e as virgulas, coloca tudo em minusculo e separar por espaços
   i = 0
   while i < len(tokens):
      if tokens[i] == '':
        #todos espaços vazio são retirados da lista
         tokens.pop(i)
         i -= 1
      i += 1
   if len(tokens) > 0:
     #quando a linha é tratada a gente adiciona ela na lista de linhas
      lines.append(tokens)
   
find_names()
#encontra os nomes dentro das linhas
if lines_to_bin_step1():
  #se não houver erros de sintaxe
   resolve_names()
  #transforma os nomes que são em parametros em tamanhos em byte, que localizam o endereço onde estão os parametros e requisição de uma instrução
   byte_arr = [0]
   for line in lines_bin:
     #para todas as linhas codificadas
      for byte in line:
      #para todos os byte na linha
         byte_arr.append(byte)
        #adiciona o byte no array de bytes
   fdst = open(str(sys.argv[2]), 'wb')
   fdst.write(bytearray(byte_arr))
  #escreve os write_bytes equivalentes
   fdst.close()

fsrc.close()

#lembrando WW escrevem em ordem crescente, ou seja, o WW escreve na word 1 dps na 2 e assim vai...

#quando utilizamos o goto main no começo, este é escrito no BYTE 0, utilizamos um WB 0 depois pra sobrescrever esse goto e não utilizarmos o BYTE 0 para nada 