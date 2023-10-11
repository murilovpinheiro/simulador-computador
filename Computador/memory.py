# Equipe:
# Guilherme de Menezes Furtado
# Murilo Vinicius Almeida Pinheiro

#Apesar do python representar números negativos em binário com sinal, ele utiliza o sistema complemento de 2, então a subtração da ALU funciona.
#É conveniente utilizar representação hexadecimal para ajudar na visualização.
#Ao deslocar um número binário B à direita N vezes (divisão por potência N de 2), é possível obter o resto desta divisão ao realizar B & bin(N).
from array import array

#Memória de 1 MB de longs, ou seja, de 262144 palavras de 32 bits (todas zeradas)
memory = array("L", [0]) * (1024*1024//4) 

#Lê a palavra da memória no endereço recebido
def read_word(end):

  #Usa só os 18 primeiros dígitos em binário (essa é a quantidade de dígitos de endereçamento)
  end = end & 0b111111111111111111
  return memory[end]

#Escreve na palavra da memória do endereço recebido
def write_word(end, val):
  
  end = end & 0b111111111111111111

  #Usa só os 32 primeiros dígitos do valor (cada palavra de memória armazena 32 bits)
  val = val & 0xFFFFFFFF
  memory[end] = val

#Cada palavra de memória possui 4 bytes, ou seja, para obter o byte n, basta fazer n//4 para obter a palavra e n%4 para obter o número do byte na palavra
def read_byte(end):

  #Há 1MB na memória, ou seja, 1048576 bytes. São então necessários 20 bits de endereçamento.
  end = end & 0b11111111111111111111

  #Divide por 4 para achar o endereço da palavra
  end_word = end >> 2
  val_word = memory[end_word]

  #Pega o resto da divisão para obter o endereço do byte na palavra
  end_byte = end & 0b11

  #Desloca para a direita até remover os bits depois do byte a ser retornado
  val_byte = val_word >> (end_byte << 3)

  #Isola os bits do byte a ser retornado
  val_byte = val_byte & 0xFF
  
  return val_byte

def write_byte(end, val):

  val = val & 0xFF
  end = end & 0b11111111111111111111
  end_word = end >> 2
  val_word = memory[end_word]

  end_byte = end & 0b11

  #Cria máscara e a usa para zerar os bits do byte onde se quer escrever
  mask = ~(0xFF << (end_byte << 3))
  val_word = val_word & mask

  #Desloca o valor a ser inserido para a posição do byte e o insere
  val = val << (end_byte << 3)
  val_word = val_word | val
  memory[end_word] = val_word