#**************************************************************************
#Trabalho Computacional – Introdução à Programação - 2024/2
#Grupo:
# Rodrigo Monteiro Junior
# Gabriel Lozer
#**************************************************************************

# NOTA: foi preferido o uso do inglês para
# evitar acentos no código, e também por preferencia pessoal

# importando para o uso da função "sqrt"
import math

# importando pra usar o sys.stdin.read(), mencionado no documento
import sys

# facilitando a checagem de erros com valores padrao
EMPTY = -223
EMPTY_Vector2 = -224
EMPTY_Pokemon = -225

# inicializadores dos nossos objetos

# um ponto no espaço, simplesmente uma coordenada x,y com
# um indice também para indicar o lugar dela na ordem
# passada nos inputs.
def Point(x, y, idx):
    p = [x,y,idx]
    return p

# Vetor de 2 dimensões, utilizado para guardar um vetor entre dois pontos,
# também serve como uma maneira conveniente de calcular distância.
def Vector2(A, B):
    v = [A, B, EMPTY]
    return v

# os nossos queridos pokemons
def Pokemon(a, d, hp, name):
    p = [a,d,hp,0,name] # atk, def, score, name
    return p

# "Getters" para cada campo de um ponto
# tornam a escrita mais conveniente e o código mais legível,
# abstraindo a lista que existe por trás de nossos objetos.
def PointGetID(p): return p[2]
def PointGetX(p): return p[0]
def PointGetY(p): return p[1]

# fórmula para o cálculo da distância, dada por
# a² = b² + c²
# onde b e c são as distancias no x e no y
def PointDist(p,p2):
    # |B-A| ( modulo of vector p2-p )
    distX = PointGetX(p2) - PointGetX(p)
    distY = PointGetY(p2) - PointGetY(p)
    return math.sqrt(\
            distX*distX + distY*distY)

# "GetNeighbour" ou, vizinho, busca o ponto mais próximo de p
# em um dado espaço, que é um conjunto de pontos.
def PointGetNeigh(p, space):

    # inicia com um valor padrão
    closest = EMPTY_Vector2

    # itera pelos pontos no espaço
    for p2 in space:

        # cria um vetor iniciando em p e indo até p2
        path = Vector2(p, p2)

        # se estivermos no valor padrão, então esse novo ponto
        # se torna o mais próximo, caso contrário,
        # calculamos a distância entre os pontos e checamos se
        # é menor do que a mais próxima atual.
        if closest == EMPTY_Vector2 or \
                Vector2GetDist(path) < Vector2GetDist(closest):
            closest = path

    return closest


# funções de utilidade para vetores
def Vector2GetA(v): return v[0]
def Vector2GetB(v): return v[1]

# essa função calcula o módulo do vetor (distancia entre os pontos B e A)
# apenas uma vez, e salva ela.
def Vector2GetDist(v):
    if v[2] == EMPTY:
        v[2] = PointDist(Vector2GetA(v), Vector2GetB(v))
    return v[2]


# getters para atk, def, hp, vitórias e nome
def PokemonGetATK(p): return p[0]
def PokemonGetDEF(p): return p[1]
def PokemonGetHP(p): return p[2]
def PokemonGetWIN(p): return p[3]
def PokemonGetNAME(p): return p[4]

# adiciona uma vitória para o pokemon
def PokemonAddWIN(p): p[3] += 1

# calcula o dano líquido do pokemon p contra o pokemon p2
def PokemonGetEATK(p, p2):
    return PokemonGetATK(p) - PokemonGetDEF(p2)

# faz dois pokemons batalharem
def PokemonBattle(p, p2):
    # primeiro, calculamos o dano líquido dos dois pokemon
    atk_p = PokemonGetEATK(p, p2)
    atk_p2 = PokemonGetEATK(p2, p)

    # em seguida, salvamos a vida de cada um
    hp_p = PokemonGetHP(p)
    hp_p2 = PokemonGetHP(p2)

    # se o dano líquido de p e p2 for menor ou igual a 0,
    # então nenhum dos pokemon pontua, pois isso significa
    # que nenhum dano efetivo ocorrerá.
    if atk_p <= 0 and atk_p2 <= 0: return

    # caso a vida dos dois não seja igual, então precisamos
    # incluí-la no cálculo
    if hp_p != hp_p2:
        # calculamos, então, os TTK (Turns To Kill),
        # a quantidade de turnos necessários para a vitória
        # para cada pokemon:
        ttk_p = hp_p2/atk_p
        ttk_p2 = hp_p/atk_p2

        # o pokemon com o menor TTK vence, pois leva o adversário
        # à 0 antes
        if ttk_p2 < ttk_p:
            PokemonAddWIN(p2)
            return

        PokemonAddWIN(p)
        return

    # caso o HP seja igual, o pokemon com maior dano líquido vence.
    if atk_p2 > atk_p:
        PokemonAddWIN(p2)
        return

    # em caso de empate, o primeiro pokemon também acumula uma vitória
    PokemonAddWIN(p)

# "parsing"

# lê um ponto do input, separando em X, Y
def parsePoint(point_idx):
    coords = input().split()
    x = int(coords[0])
    y = int(coords[1])
    return Point(x, y, point_idx)

# lê todo o conjunto de pontos do espaço do input,
# um por um, e salva na lista space.
# A quantidade lida é dada por n.
def parsePoints():
    space = []

    n = int(input())

    for i in range(n):
        space.append(parsePoint(i))

    return space

# lê um pokemon a partir de um vetor de conteúdo do input
# que nada mais é do que o stdin separado pelos espaços
def parseSinglePokemon(content):
    name = content.pop(0)
    hp   = int(content.pop(0))
    atk  = int(content.pop(0))
    dfs  = int(content.pop(0))
    return Pokemon(atk, dfs, hp, name)

def parsePokemon():
    pokemon = []

    # separando o stdin em espaços
    content = sys.stdin.read().split()

    # enquanto ainda houver 4 ou mais campos
    # para leitura, leia um pokemon,
    # pois um pokemon necessita de 4 campos (HP, ATK, DEF, NOME)
    while len(content) >= 4:
        pokemon.append(parseSinglePokemon(content))

    return pokemon


# calcula o caminho mais curto no espaço
def shortestPath(space):
    # a string do caminho inicia com o ponto inicial
    path = "0"

    start = space[0] # uma cópia do ponto inicial, para cálculo de distância da volta
    point = space[0] # ponto atual, modificado a cada iteração
    total = 0 # distância total

    while len(space) > 1:
        path += " " # adiciona um espaço à string do caminho

        space.remove(point) # remove o ponto atual do espaço

        # procura o ponto mais próximo ao atual, excluindo ele mesmo
        # e os pontos anteriores
        neigh = PointGetNeigh(point, space)

        # recebe o destino do vetor, isto é, o ponto que encontramos
        point = Vector2GetB(neigh)

        # calcula a distância percorrida entre os pontos.
        total += Vector2GetDist(neigh)

        # adiciona o indice do ponto à string do caminho
        path += str(PointGetID(point))

    # calcula a distância da volta
    total += PointDist(start, point)
    # adiciona o ponto inicial no caminho
    path += " 0"

    print("Caminho:", path)
    print(f"Distancia: {total:.6f}")


def findWinner(pokemon):
    # inicia no vazio
    melhor = EMPTY_Pokemon

    # itera pelos pokemon, removendo as batalhas repetidas
    for i in range(len(pokemon)):

        # remove o pokemon atual
        p = pokemon.pop(0)

        # itera pelos possíveis oponentes e batalha com cada um
        for p2 in pokemon:
            PokemonBattle(p, p2)

        # se melhor for vazio ou o número de vitórias do
        # pokemon atual for maior que o número do atual
        # campeão, temos um novo campeão
        if melhor == EMPTY_Pokemon or \
                PokemonGetWIN(p) > PokemonGetWIN(melhor):
            melhor = p

    # printa o nome e as vitórias do campeão
    print("Campeao:",PokemonGetNAME(melhor))
    print("Numero de vitorias:",PokemonGetWIN(melhor))


def main():
    # faz o parsing do input
    space = parsePoints()
    pokemon = parsePokemon()

    # calcula o caminho mais próximo e o pokemon campeão
    shortestPath(space)
    findWinner(pokemon)

main()

