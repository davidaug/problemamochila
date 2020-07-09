import numpy as np
import copy
from itertools import combinations, product
import time
import csv


status_ag_print = True


def ag_print(string):
    if status_ag_print:
        print(string)


class AlgoritmoGenetico:

    tam_pop = 0
    prob_mut = 0.0
    prob_cross = 0.0
    best_fitness = []
    best_pop = []

    tipo_funcao = 'reparacao'

    coef_penalidade = 0.1

    pais = []

    fitness_atual = np.array([])

    melhor_fitness_geral = 0
    individuo_melhor_fitness_geral = []
    melhor_mochila_geral = ''

    populacao = None
    cap_mochila = 120

    penalidade = []

    objetos_mochila = np.array(
        [np.array([3, 8, 12, 2, 8, 4, 4, 5, 1, 1, 8, 6, 4, 3, 3, 5, 7, 3, 5, 7, 4, 3, 7, 2, 3, 5, 4, 3, 7, 19, 20, 21, 11, 24, 13, 17, 18, 6, 15, 25, 12, 19]),
        np.array([1, 3, 1, 8, 9, 3, 2, 8, 5, 1, 1, 6, 3, 2, 5, 2, 3, 8, 9, 3, 2, 4, 5, 4, 3, 1, 3, 2, 14, 32, 20, 19, 15, 37, 18, 13, 19, 10, 15, 40, 17, 39])]
    ) #itens da mochila

    controle_exec = 0

    def __init__(self, prob_mut, prob_cross, tam_pop, funcao, max_exec=500):
        self.tam_pop = tam_pop
        self.prob_mut = prob_mut
        self.prob_cross = prob_cross
        if funcao == 'reparacao':
            self.fn = self.funcao_reparacao
        else:
            self.fn = self.funcao_penalidade
            self.tipo_funcao = 'penalidade'


        self.max_exec = max_exec
        self.penalidade = np.zeros(tam_pop)
        self.max_peso = self.objetos_mochila[0].sum()
        self.max_valor = self.objetos_mochila[1].sum()

        ag_print(f'Pm: {self.prob_mut} | Pc: {self.prob_cross} | Tam. População: {self.tam_pop} | Fn: {funcao}')
        ag_print(f'Max Exec: {self.max_exec}')

    def inicializar_populacao(self):
        for i in range(0, self.tam_pop):
            pop = np.array(np.random.randint(0, 2, size=len(self.objetos_mochila[0])))
            if self.populacao is None:
                self.populacao = np.array(pop)
            else:
                self.populacao = np.vstack((self.populacao, pop))

    def calcular_peso(self, arr):
        return arr.dot(self.objetos_mochila[0]).sum()

    def calcular_beneficio(self, arr): # Calcula o valor da mochila
        return arr.dot(self.objetos_mochila[1]).sum()

    def calcular_fitness(self):
        melhor_fitness = 0
        individuo = None
        self.fitness_atual = np.array([])
        for pop in range(0, len(self.populacao)):
            fitness = self.calcular_beneficio(self.populacao[pop])
            if self.tipo_funcao == 'penalidade':
                fitness = fitness - self.penalidade[pop]
            self.fitness_atual = np.append(self.fitness_atual, fitness)
            if self.calcular_peso(self.populacao[pop]) < self.cap_mochila and fitness > melhor_fitness:
                melhor_fitness = fitness
                individuo = copy.deepcopy(self.populacao[pop])

        if melhor_fitness > self.melhor_fitness_geral:
            self.melhor_fitness_geral = melhor_fitness
            self.individuo_melhor_fitness_geral = individuo

        self.best_fitness.append(melhor_fitness)
        self.best_pop.append(individuo)

    def selecao_roleta(self):
        self.pais = []
        while len(self.pais) < 2:
            soma_fitness = self.fitness_atual.sum()
            psi = np.array([])
            for i in range(0, len(self.populacao)):
                psi = np.append(psi, (self.fitness_atual[i]/soma_fitness))

            indv = np.random.randint(0, len(self.populacao)) #sorteia individuo inicial
            r = np.random.random() #garante ao menos 2 pais
            soma = psi[indv]
            self.pais.append(self.populacao[indv])
            while r > soma:
                indv += 1
                if indv > len(psi)-1:
                    indv = 0

                self.pais.append(self.populacao[indv])
                soma += psi[indv]


    def reproducao(self):
        combinacoes = tuple(combinations(np.arange(len(self.pais)), 2))
        for combinacao in combinacoes:
            r = np.random.random()
            if r < self.prob_cross:
                ponto_cross = np.random.randint(0, len(self.pais[0]))
                filho_1 = np.append(self.pais[combinacao[0]][:ponto_cross], self.pais[combinacao[1]][ponto_cross:])
                filho_2 = np.append(self.pais[combinacao[1]][:ponto_cross], self.pais[combinacao[0]][ponto_cross:])
                self.populacao = np.vstack((self.populacao, filho_1))
                self.populacao = np.vstack((self.populacao, filho_2))

    def mutacao(self):
        for pop in range(0, len(self.populacao)):
            for idx in range(0, len(self.populacao[pop])):
                mut = np.random.random()
                if mut < self.prob_mut:
                    self.populacao[pop][idx] = int(not self.populacao[pop][idx])

    def selecionar_nova_populacao(self):
        temp = self.fitness_atual
        nova_populacao = []
        novo_fitness_atual = []
        while len(nova_populacao) < self.tam_pop:
            idx_maior_fitness = temp.argmax()
            nova_populacao.append(self.populacao[idx_maior_fitness])
            novo_fitness_atual.append(self.fitness_atual[idx_maior_fitness])
            temp[idx_maior_fitness] = 0

        self.populacao = np.array(nova_populacao)
        self.fitness_atual = np.array(novo_fitness_atual)

    def funcao_reparacao(self):
        for pop in range(0, len(self.populacao)):
            while self.calcular_peso(self.populacao[pop]) > self.cap_mochila:
                array_valor_peso = np.array([])
                for idx in range(0, len(self.populacao[pop])):
                    item = self.populacao[pop][idx]
                    array_valor_peso = np.append(array_valor_peso,
                                                 item*(self.objetos_mochila[1][idx] / self.objetos_mochila[0][idx]))

                    if item == 0:
                        array_valor_peso[idx] = np.nan

                menor_valor_peso = np.nanargmin(array_valor_peso)
                self.populacao[pop][menor_valor_peso] = 0


    def funcao_penalidade(self):
        self.penalidade = np.zeros(len(self.populacao))
        for pop in range(0, len(self.populacao)):
            peso_populacao = self.calcular_peso(self.populacao[pop])
            if peso_populacao > self.cap_mochila:
                self.penalidade[pop] = (self.max_valor*self.coef_penalidade) * (peso_populacao-self.cap_mochila)

    def executar(self):
        self.inicializar_populacao()
        self.calcular_fitness()

        self.controle_exec = 0
        ag_print("Inicio Loop")

        while self.controle_exec < self.max_exec:
            self.selecao_roleta()
            self.reproducao()
            self.mutacao()
            self.fn()
            self.calcular_fitness()
            self.selecionar_nova_populacao()
            self.controle_exec += 1

        ag_print("Final Loop")

        ag_print(f"Melhor Fitness: {self.melhor_fitness_geral}")
        #print(self.best_fitness)
        final = f"{str(np.sum(self.individuo_melhor_fitness_geral))}, "
        final += f"{str(self.calcular_peso(self.individuo_melhor_fitness_geral))}, "
        final += f"{str(self.calcular_beneficio(self.individuo_melhor_fitness_geral))}, "
        final += f"{str([i for i in self.individuo_melhor_fitness_geral])}"
        final = final.replace("[", "")
        final = final.replace("]", "")

        self.melhor_mochila_geral = final

        ag_print(final)
        #ag_print(f"Melhores Fitness: {self.best_fitness[1:]}")
        #ag_print(f"Melhores Individuos: {self.best_pop[1:]}")




if __name__ == '__main__':
    REPARACAO = 'reparacao'
    PENALIDADE = 'penalidade'

    funcoes = [REPARACAO, PENALIDADE]
    conf_poss_mut = [0.06, 0.07, 0.08]
    conf_poss_cross = [0.6, 0.7, 0.8]
    conf_tam_pop = [4, 5, 6]

    configs = [conf_poss_mut, conf_poss_cross, conf_tam_pop]
    lista_configs = list(product(*configs))
    list_execucao = []

    funcao = REPARACAO
    for configuracao in lista_configs:
        for num_exec in range(1,11):
            ag_print("Inicializando...")
            dict_resultado = dict()
            poss_mut = configuracao[0]
            poss_cross = configuracao[1]
            pop_inicial = configuracao[2]
            start = time.time()
            ag = AlgoritmoGenetico(poss_mut, poss_cross, pop_inicial, funcao, max_exec=500)
            ag.executar()
            end = time.time()
            print(end-start)

            dict_resultado['config'] = str(configuracao)
            dict_resultado['numero_execucao'] = num_exec
            dict_resultado['melhor_mochila'] = ag.melhor_mochila_geral
            dict_resultado['lista_melhor_fitness'] = ag.best_fitness[1:]
            dict_resultado['melhor_fitness'] = ag.melhor_fitness_geral
            list_execucao.append(dict_resultado)
            keys = list_execucao[0].keys()

    with open(f'result_csv_{np.random.randint(1000,9000)}.csv', 'w') as output:
        dwriter = csv.DictWriter(output, keys)
        dwriter.writeheader()
        dwriter.writerows(list_execucao)

