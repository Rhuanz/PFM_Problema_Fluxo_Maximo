"""
* Programa: Modelagem PFM
* Autor(es): Rhuan Gabriel, Ana Paula Kendall
* Data de Criação: 26/04/2021
* Última alteração: 03/05/2021
* Descrição Geral: Modelagem genérica e solução para Problemas de Fluxo Máximo, programa apresentado como parte
da primeira nota de disciplina Pesquisa Operacional.
"""

import pulp
from pulp import LpProblem
from pulp import LpVariable
from pulp import LpConstraint
from pulp import LpElement
from pulp import LpSolverDefault
from pulp import LpMinimize
from pulp import LpMaximize
from pulp import LpStatus
from pulp import value
from pulp import lpSum

print("Olá!\n"
      "Para resolver seu problema de fluxo maximo\n"
      "escreva os dados num arquivo .txt no fomato especificado a seguir:")

print("n #numero de vertices (vertices numerados de 1 a n )\n"
      "m #numero de arcos (arcos numerados de 1 a m)\n"
      "s #indice da origem\n"
      "t #indice do escoadouro\n"
      "i j c1 #dados do arco 1\n"
      ". . .\n"
      "i j cm #dados do arco m\n")

print("\nVerifique se o arquivo esta no diretorio 'Instancias' e digite o nome do arquivo\n")

#organizando nome do arquivo
arq = input("Digite o nome do arquivo: ")
arq = arq+".txt"

#lendo os dados do arquivo
ref_arquivo = open("Instancias/"+arq, "r")

nrede = []

for line in ref_arquivo:
    nrede.append(line)

ref_arquivo.close()

#removendo as quebras de linha
rede = []

for i in nrede:
    if i != "\n":
        rede.append(i)

for i in range(0, len(rede)):
    rede[i] = rede[i].rstrip("\n")

#distribuindo valores recebidos
vertices = int(rede[0])
arcos = int(rede[1])
origem = int(rede[2])
fim = int(rede[3])

#definindo o tipo do problema
prob = LpProblem("PFM", LpMaximize)

#preenchendo variáveis do programa
x = [[[]for i in range(vertices)] for j in range(vertices)] 

for i in range(vertices):
    for j in range(vertices):
        x[i][j] = 0

for i in range (4, len(rede)):
    varia = rede[i].split()
    x[int(varia[0])-1][int(varia[1])-1] = int(varia[2]) 

#definindo as variáveis da modelagm
for i in range(vertices):
    for j in range(vertices):
        if x[i][j] != 0:
            nome = f"X{i}{j}"
            x[i][j] = LpVariable(nome, 0, x[i][j])

#escolhendo qual lado maximizar da rede e definindo função objetivo
somai = 0
somaf = 0

for i in range(vertices):
    somai = somai + x[origem-1][i]
    somaf = somaf + x[i][fim-1]

if somai == somaf or somai < somaf:
    prob += lpSum(x[origem-1][i] for i in range(vertices))

else:
    prob += lpSum(x[i][fim-1] for i in range(vertices))

#definindo condições
for i in range (vertices):
    if i != origem-1 and i != fim-1:
        prob += lpSum(x[i][j] for j in range(vertices)) ==  lpSum(x[j][i] for j in range(vertices))

prob += lpSum(x[origem-1][i] for i in range (vertices)) >= 0
prob += lpSum(x[i][fim-1] for i in range (vertices)) >= 0


#ativando e exibindo a solução
status = prob.solve()
print(LpStatus[status])

if somai == somaf or somai < somaf:
    somai = 0
    for i in range(vertices):
        somai += value(x[origem-1][i])
    print(f"Solucao: {somai}")
else:
    somaf = 0
    for i in range(vertices):
        somaf += value(x[i][fim-1])
    print(f"Solucao: {somaf}")
    
for i in range(0, vertices):
    for j in range(0, vertices):
        if value(x[i][j]) != 0:
            print(f"Arco{i+1},{j+1} = {value(x[i][j])}")
    
