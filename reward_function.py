def reward_function(parametros):
    # primeiro extrai-se os dados oferecidos pelo ambiente que serão utilizados para a modelagem da função de recompensa
    distanciaCentro = parametros['distance_from_center'] # distancia que o carrinho está do centro da pista (metros)
    larguraPista = parametros['track_width'] # largura da pista (metros)
    velocidade = parametros['speed'] # velocidade atual do carrinho (metros por segundo)
    rodasNaPista = parametros['all_wheels_on_track'] # diz se todas as rodas estão na pista (booleana)
    anguloDirecao = abs(parametros['steering_angle']) # angulo de direção do carrinho (graus) 

    
    # recompensa base, que será ajustada conforme as regras criadas
    recompensa = 1.0
    
    # essa regra avalia o quão centralizado o carrinho está na pista. 
    # 1. primeiro calcula-se a 'proporcaoDistanciaDoCentro', que é a distância do carro ao centro # dividida pela metade da largura da pista. assim temos essa distância 'normalizada', independentemente da largura da pista
    # 2. se a proporção for maior que 0.6, significa que o carro está se afastando do centro, então a recompensa é diminuida, proporcionalmente.
    # 3. se o carro estiver próximo ao centro, ou seja, proporcaoDistanciaDoCentro < 0.6, aumenta-se a recompensa para incentivar que ele permaneça nessa posição
    proporcaoDistanciaDoCentro = distanciaCentro / (larguraPista / 2)
    if proporcaoDistanciaDoCentro > 0.6:  
        recompensa *= (0.8 - proporcaoDistanciaDoCentro)  
    else:
        recompensa *= 1.5  

    # se alguma roda estiver fora da pista, penaliza. isso incentiva o agente a se manter dentro dos limites da pista
    if not rodasNaPista:
        recompensa *= 0.4  

    # incentiva o carrinho a manter uma alta velocidade mas mas com a condição de o ângulo de direção se manter dentro de um limite controlável.
    # 1. se a velocidade for maior que 2.5m/s e o angulo de direção for menor que 20º, dobra-se a recompensa.
    # 2. se a velocidade for ainda maior, > 3.5m/s, e o angulo de direção for ainda menor, < 15º, triplica-se a recompensa, pois essa é uma condição ideal, em que o carrinho está veloz mas com a direção controlada.
    # 3. se a velocidade for menor do que 2.5 ou o angulo de direção for maior do que 20º, a recompensa é diminuída, pois ou o carrinho estará lento demais ou com um ângulo mais descontrolado.
    if velocidade > 2.5 and anguloDirecao < 20:  
        recompensa *= 2.0  
    elif velocidade > 3.5 and anguloDirecao < 15:
        recompensa *= 3.0  
    else:
        recompensa *= 0.7  

    return float(recompensa)
