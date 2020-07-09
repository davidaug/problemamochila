# problemamochila

# Penalização

Para cada indivíduo com peso acima da capacidade da mochila, foi atribuído um valor de penalidade, para subtrair o valor fitness. Dessa forma, os indivíduos com maior penalidade, seriam descartado ao longo de novas gerações.
 
    array_global_penalidade <- array(tamanho(POPULAÇÃO), 0) #array inicializado com zeros
    para todo indivíduo de POPULAÇÃO faça:
        peso_individuo <- calculo_peso(individuo)
        se peso_individuo > peso_max_mochila então:
        array_global_penalidade[individuo] <- (soma_valor*coef)*(peso_individuo-peso_max_mochila)

Sendo: 
- array_global_penalidade: array acessivel para a função fitness
- peso_individuo: peso do individuo (itens na mochila)
- peso_max_mochila: capacidade máxima da mochila
- soma_valor: soma de todos os itens disponíveis
- coef: coeficiente defindo por testes (no caso, 0.1)

Função fitness:

    fitness <- fitness - array_global_penalidade[individuo]


Para cada indivíduo com peso acima da capacidade da mochila, foi atribuído um valor de penalidade, sendo:

    Penalidade = (Somatório todos os itens * coeficiente) * (peso individuo - capacidade máxima da mochila)

A penalidade é atribuída num array global, que será acessado pelo cálculo de fitness, onde irá subtrair o fitness calculado.

# Reparação

Enquanto o indivíduo é infactível, é procurado o item com menor razão, entre valor e peso e esse item é removido do indivíduo.

    para todo indivíduo de POPULAÇÃO faça:
        enquanto calculo_peso(individuo) > peso:
            ind_item <- busca_menor_valor(item.valor/item.peso).indice
            populacao[ind_item] <- 0
            
Para cada indivíduo infactível:
1. O laço busca o índice do item com a menor razão de valor por peso 
2. O item é removido do indivíduo
3. Se o peso ainda é maior que a capacidade da mochila, o processo é realizado novamente
