# Equipe:
# Guilherme de Menezes Furtado
# Murilo Vinicius Almeida Pinheiro

import memory
import clock
import cpu as cpu
import disk

arqbin = input("Digite o nome do arquivo .bin que deseja ler: ")

disk.read('../Assembly/' + arqbin + '.bin')

clock.start([cpu])

print(memory.read_word(1))
