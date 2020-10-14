import tabela_info

f = open("texto.txt", "r")
lines = f.readlines()
l_linha = 0
l_coluna = 0

erros = {
    0: 'Símbolo não pode ser reconhecido.',
    2: 'Necessário um dígito para continuar.',
    4: 'Necessário um sinal seguido de dígito ou somente um dígito após o "E" para continuar.',
    5: 'Necessário um dígito após o sinal.',
    7: 'Erro de aspas no literal.',
    10: 'Necessário que se digite "}".'
}

numeros = ['0','1','2','3','4','5','6','7','8','9']
letras = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
            'q','r','s','t','u','v','x','y','w','z','A','B','C','D','E',
            'F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T',
            'U','V','X','W','Y','Z']

def def_proximo(estado_atual, simbolo):

    if estado_atual == 7 and (not simbolo == '\n') and (not simbolo == '"'):
        return tabela_info.tabela_transicoes[estado_atual][tabela_info.dicionario["C"]]
    elif estado_atual == 10 and (not simbolo == '}') and (not simbolo == '\n'):
        return tabela_info.tabela_transicoes[estado_atual][tabela_info.dicionario["C"]]
    elif (estado_atual == 1 or estado_atual == 3) and simbolo == "E":
        return tabela_info.tabela_transicoes[estado_atual][tabela_info.dicionario["E"]]
    elif simbolo in numeros:
        return tabela_info.tabela_transicoes[estado_atual][tabela_info.dicionario["D"]]
    elif simbolo in letras:
        return tabela_info.tabela_transicoes[estado_atual][tabela_info.dicionario["L"]]
    elif simbolo not in tabela_info.dicionario.keys():
        return tabela_info.tabela_transicoes[estado_atual][tabela_info.dicionario["ERRO"]]
    else:
        return tabela_info.tabela_transicoes[estado_atual][tabela_info.dicionario[simbolo]]


def def_token(lexema, estado):


    token = tabela_info.tipo_tokens[estado]
    objeto_tabela = {"lexema": lexema, "token": token, "Tipo":"-"}

    if token == "id":
        if lexema not in tabela_info.tabela_simbolos.keys():
            tabela_info.tabela_simbolos[lexema] = objeto_tabela
        else:
            objeto_tabela = tabela_info.tabela_simbolos[lexema]

    return objeto_tabela


def def_error(estado_atual, l_linha, l_coluna):


    print("\nErro (" +str(l_linha+1) + "," +str(l_coluna) +"): " + erros[estado_atual])

    return False


def lexema():

    global l_linha
    global l_coluna

    lex = ""
    linha = lines[l_linha]

    estado_atual = 0
    estado_proximo = 0

    while True:

        simbolo = linha[l_coluna]
        estado_proximo = def_proximo(estado_atual, simbolo)


        if estado_proximo == -1:
            if estado_atual in tabela_info.estados_final:
              return def_token(lex, estado_atual)
            else:
                if(simbolo!= '\n'):
                    print(linha[l_coluna])
                    l_coluna = l_coluna + 1
                    return def_error(estado_atual, l_linha, l_coluna - 1)

            return def_error(estado_atual, l_linha, l_coluna)
        elif estado_proximo == 0:
            lex = ""
            if simbolo == '\n':
                l_linha = l_linha + 1
                try:
                    linha = lines[l_linha]
                except:
                    estado_atual = 22
                    return def_token(lex, estado_atual)
                l_coluna = 0
            else:
                l_coluna = l_coluna + 1
        else:
            lex = lex + simbolo
            l_coluna = l_coluna + 1
            estado_atual = estado_proximo


def inicio():

    global l_coluna
    aux = 1

    while (aux == 1):

        token = lexema()
        if token == False:
            print("\n")
        elif token != False:
            print(token)
            if token['token'] == "EOF":
                break


    print("\nTabela de Simbolos:")
    for i in tabela_info.tabela_simbolos:
        print(str(i) + " : " + str(tabela_info.tabela_simbolos[i]))


inicio()


