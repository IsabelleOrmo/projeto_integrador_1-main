import tabulate
import sys
import oracledb

try:
    conexao = oracledb.connect(
    user="ISA",
    password="isabelle",
    dsn="localhost/XEPDB1")

except Exception as erro:
    print('Erro em conexão', erro)
else:
    print("Conectado", conexao.version)

    # Criar Cursor
cursor = conexao.cursor()

# Criar Cursor
cursor = conexao.cursor()

'''cursor.execute ("""
CREATE TABLE ESTOQUE (
cod_prod INTEGER PRIMARY KEY,
nome VARCHAR2(50),
descricao VARCHAR2(150),
ca FLOAT,
cf FLOAT,
cv FLOAT,
iv FLOAT,
ml Float
 )""")'''


def descriptografia_hills(descricao):
    if descricao is None or not isinstance(descricao, str):
        return ""
    alfabeto = ['Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y']
    matriz_chave = [[42, -63], [-21, 84]]
    indices = [alfabeto.index(letra) for letra in descricao if letra in alfabeto]
    if len(indices) % 2 != 0:
        indices.append(indices[-1])

    num_cols = 2
    matriz_palavra = [indices[i:i + num_cols] for i in range(0, len(indices), num_cols)]
    matriz_criptografada = []

    for vetor in matriz_palavra:
        for linha in matriz_chave:
            produto = sum(linha[i] * vetor[i] for i in range(len(vetor)))
            matriz_criptografada.append(produto)

    for i in range(len(matriz_criptografada)):
        matriz_criptografada[i] = matriz_criptografada[i] % 26
        while matriz_criptografada[i] < 0:
            matriz_criptografada[i] += 26

    descricao_criptografada = ''.join(alfabeto[i] for i in matriz_criptografada)
    return descricao_criptografada


def criptografia_hills(criptografar):
    alfabeto = ['Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y']
    matriz_chave = [[4, 3], [1, 2]]

    indices = [alfabeto.index(letra) for letra in criptografar if letra in alfabeto]
    if len(indices) % 2 != 0:
        indices.append(indices[-1])

    num_cols = 2
    matriz_palavra = [indices[i:i + num_cols] for i in range(0, len(indices), num_cols)]
    matriz_criptografada = []

    for vetor in matriz_palavra:
        for linha in matriz_chave:
            produto = sum(linha[i] * vetor[i] for i in range(len(vetor)))
            matriz_criptografada.append(produto)

    for i in range(len(matriz_criptografada)):
        matriz_criptografada[i] = matriz_criptografada[i] % 26
        while matriz_criptografada[i] < 0:
            matriz_criptografada[i] += 26

    descricao_criptografada = ''.join(alfabeto[i] for i in matriz_criptografada)
    return descricao_criptografada


def calculo(produtos):
    from tabulate import tabulate
    for row in produtos:

        preco_venda = row[3] / (1 - ((row[4] + row[5] + row[6] + row[7]) / (100)))

        # um porcento

        # cálculo receita bruta
        receita_bruta = preco_venda - row[3]

        # cálculo de lucro
        # mc = ((cf + cv + iv + ml) / pv) - 100

        # valor sobre o preço final
        valor_imposto = (row[6] / 100) * preco_venda
        valor_comissao = (row[5] / 100) * preco_venda
        valor_custofixo = (row[4] / 100) * preco_venda

        # cálculo outros custos e rentabilidade
        oc = valor_imposto + valor_comissao + valor_custofixo
        rentabilidade = receita_bruta - oc

        # valores em porcentagem
        pct_pv = ((preco_venda / preco_venda) * 100)
        pct_ca = ((row[3] / preco_venda) * 100)
        pct_rb = ((receita_bruta / preco_venda) * 100)
        pct_custofix = ((valor_custofixo / preco_venda) * 100)
        pct_comissao = ((valor_comissao / preco_venda) * 100)
        pct_imp = ((valor_imposto / preco_venda) * 100)
        pct_oc = ((oc / preco_venda) * 100)
        pct_rent = ((rentabilidade / preco_venda) * 100)

        print("\nId:", row[0])
        print("Nome:", row[1])
        descricao = row[2]
        descricao_descriptografada = descriptografia_hills(descricao)
        print("Descrição:", descricao_descriptografada)
        '''print("Descrição:", row[2]) '''
        # print("\n")
        from tabulate import tabulate  # para importar usamos o terminal e colocamos o camando: pip install tabulate
        data = [['A. Preço de Venda', f'{preco_venda:.2f}', f'{pct_pv:.0f}%'],
                ['B. Custo de Aquisição (Fornecedor)', f'{row[3]:.2f}', f'{pct_ca:.0f}%'],
                ['C. Receita Bruta', f'{receita_bruta:.2f}', f'{pct_rb:.0f}%'],
                ['D. Custo Fixo/Administrativo', f'{valor_custofixo:.2f}', f'{pct_custofix:.0f}%'],
                ['E. Comissão de Vendas', f'{valor_comissao:.2f}', f'{pct_comissao:.0f}%'],
                ['F. Impostos', f'{valor_imposto:.2f}', f'{pct_imp:.0f}%'],
                ['G. Outros Custos (D+E+F)', f'{oc:.2f}', f'{pct_oc:.0f}%'],
                ['H. Rentabilidade (C-G)', f'{rentabilidade:.2f}', f'{pct_rent:.0f}%\n']]
        print(tabulate(data, headers=["Descrição", "Valor", "%"], floatfmt=".2f"))
        if (pct_rent > 0):
            if (pct_rent <= 10):
                print("Lucro Baixo")
            if (pct_rent > 10 and pct_rent <= 20):
                print("Lucro médio")
            if (pct_rent > 20):
                print("Lucro Alto")

        else:
            if (pct_rent == 0):
                print("Equilíbrio")
            else:
                print("Prejuízo")
    return produtos


def mostrar_produtos():
    conexao.commit()
    sql_select_Query = "SELECT * FROM estoque order by cod_prod asc"
    cursor = conexao.cursor()
    cursor.execute(sql_select_Query)
    produtos = cursor.fetchall()
    calculo(produtos)
    menu()


def cadastrar_produto():
    print('\nEntrada de Dados')
    validacao = 0
    while True:
        cod_prod = int(input('Código do produto: '))
        # validacao
        validacao = "SELECT * FROM estoque WHERE cod_prod={0}".format(cod_prod)
        cursor.execute(validacao)
        resultado = cursor.fetchall()
        if resultado:
            print("Este produto já foi cadastrado.")

        else:
            break

    nome = input('Nome do produto: ')
    descricao = input('Descrição do produto: ')
    criptografar = descricao.upper()
    descricao_criptografada = criptografia_hills(criptografar)
    ca = float(input('Custo do produto: '))
    cf = float(input('Custo fixo: '))
    cv = float(input('Comissão de vendas: '))
    iv = float(input('Impostos: '))
    ml = float(input('Rentabilidade: '))

    comando = f"""INSERT INTO ESTOQUE( cod_prod,nome,descricao,ca,cf,cv,iv,ml)
    VALUES
        ( {cod_prod}, '{nome}', '{descricao_criptografada}',{ca},{cf}, {cv},{iv},{ml})"""

    cursor.execute(comando)
    conexao.commit()
    print('Produto Cadastrado!')
    print("\n")
    '''from tabulate import tabulate #para importar usamos o terminal e colocamos o camando: pip install tabulate
    data = [[ 'A. Preço de Venda', f'{pv:.2f}', f'{pct_pv:.0f}%'],
    ['B. Custo de Aquisição (Fornecedor)',  f'{ca:.2f}', f'{pct_ca:.0f}%'],
    ['C. Receita Bruta', f'{rb:.2f}', f'{pct_rb:.0f}%'],
    ['D. Custo Fixo/Administrativo', f'{valor_custofixo:.2f}', f'{pct_custofix:.0f}%'],
    ['E. Comissão de Vendas', f'{valor_comissao:.2f}', f'{pct_comissao:.0f}%'],
    ['F. Impostos', f'{valor_imposto:.2f}', f'{pct_imp:.0f}%'],
    ['G. Outros Custos (D+E+F)', f'{oc:.2f}', f'{pct_oc:.0f}%'],
    ['H. Rentabilidade (C-G)', f'{ml:.2f}', f'{pct_rent:.0f}%\n']]
    print (tabulate(data, headers=["Descrição", "Valor", "%"], floatfmt=".2f"))

    if pct_rent > 20:
        print("Lucro Alto!!")
    elif pct_rent > 10 and pct_rent <= 20:
        print("Lucro médio!")
    elif pct_rent > 0 and pct_rent <=10:
        print("Lucro baixo...")
    elif pct_rent == 0:
        print("Equilíbro.")
    else: 
        print("Prejuízo....")'''
    menu()


def deletar_produto():
    while True:
        id_prod = int(input("Digite o código do produto: "))
        conexao.commit()
        cursor = conexao.cursor()
        validacao = "SELECT * FROM estoque WHERE cod_prod={0}".format(id_prod)
        cursor.execute(validacao)
        resultado = cursor.fetchall()
        if resultado:
            sql_select_Query = "SELECT * FROM estoque WHERE cod_prod={0}".format(id_prod)
            cursor = conexao.cursor()
            cursor.execute(sql_select_Query)
            produtos = cursor.fetchall()
            calculo(produtos)

            confirmar = int(input("\nConfirme o id do produto para sua exclusão: "))
            if (confirmar == id_prod):
                apagar_query = "delete FROM estoque WHERE cod_prod={0}".format(confirmar)
                cursor = conexao.cursor()
                cursor.execute(apagar_query)
                conexao.commit()
                print("Produto excluído")
                menu()
            else:
                print("Operação cancelada")
                menu()

        else:
            print("Produto não encontrado.")


def alterar_produto():
    print("ALTERAR PRODUTO \n")
    while True:
        id_prod = int(input("Digite o código do produto: "))
        conexao.commit()
        cursor = conexao.cursor()
        validacao = "SELECT * FROM estoque WHERE cod_prod={0}".format(id_prod)
        cursor.execute(validacao)
        resultado = cursor.fetchall()
        if resultado:
            while True:
                print("\n MENU")
                print("1. MOSTRAR")
                print("2. ALTERAR")
                print("3. SAIR")
                opcao = int(input("Selecione o que deseja fazer:"))
                if (opcao == 1):
                    sql_select_Query = "SELECT * FROM estoque WHERE cod_prod={0}".format(id_prod)
                    cursor.execute(sql_select_Query)
                    produtos = cursor.fetchall()
                    calculo(produtos)
                elif (opcao == 2):
                    while True:
                        print("\nO que deseja alterar?\n")
                        print("1. NOME")
                        print("2. DESCRIÇÃO")
                        print("3. CUSTO DO PRODUTO")
                        print("4. CUSTO FIXO")
                        print("5. IMPOSTO")
                        print("6. RENTABILIDADE")
                        print("7. SAIR")
                        alteracao = int(input("\nDigite a opção: "))
                        if (alteracao == 1):
                            nome = input("Insira o novo nome: ")
                            sql_alterar_query = "UPDATE estoque SET nome = :1 WHERE cod_prod = :2"
                            cursor.execute(sql_alterar_query, (nome, id_prod))
                            conexao.commit()
                            print("\nProduto alterado com sucesso!")
                        elif (alteracao == 2):
                            descricao = input("Insira a nova descrição: ")
                            if not descricao.strip():
                                print("A descrição não pode estar vazia!")
                                continue
                            criptografar = descricao.upper()
                            descricao_criptografada = criptografia_hills(criptografar)
                            sql_alterar_query = "UPDATE estoque SET descricao = :1 WHERE cod_prod = :2"
                            cursor.execute(sql_alterar_query, (descricao_criptografada, id_prod))
                            conexao.commit()
                            print("\nProduto alterado com sucesso!")
                        elif (alteracao == 3):
                            ca = int(input("Insira o novo custo do produto: "))
                            sql_alterar_query = "UPDATE estoque SET ca = :1 WHERE cod_prod = :2"
                            cursor.execute(sql_alterar_query, (ca, id_prod))
                            conexao.commit()
                            print("\nProduto alterado com sucesso!")
                        elif (alteracao == 4):
                            cf = int(input("Insira o novo custo fixo: "))
                            sql_alterar_query = "UPDATE estoque SET cf = :1 WHERE cod_prod = :2"
                            cursor.execute(sql_alterar_query, (cf, id_prod))
                            conexao.commit()
                            print("\nProduto alterado com sucesso!")
                        elif (alteracao == 5):
                            iv = int(input("Insira o novo valor de imposto: "))
                            sql_alterar_query = "UPDATE estoque SET iv = :1 WHERE cod_prod = :2"
                            cursor.execute(sql_alterar_query, (iv, id_prod))
                            conexao.commit()
                            print("\nProduto alterado com sucesso!")
                        elif (alteracao == 6):
                            ml = int(input("Insira o nova rentabilidade: "))
                            sql_alterar_query = "UPDATE estoque SET ml = :1 WHERE cod_prod = :2"
                            cursor.execute(sql_alterar_query, (ml, id_prod))
                            conexao.commit()
                            print("\nProduto alterado com sucesso!")
                        elif (alteracao == 7):
                            break
                        else:
                            print("Essa opção não existe")
                elif (opcao == 3):
                    menu()
                else:
                    print("Essa opção não existe")

        else:
            print("Produto não encontrado. \nDeseja voltar ao menu principal?")
            while True:
                voltar = int(input("Digite 1 para SIM ou digite 2 para NÃO \n"))
                if (voltar == 1):
                    menu()
                elif (voltar == 2):
                    break
                else:
                    "Opção inválida"


def menu():
    print("\n-----MENU-----\n")
    print("DIGITE 1 PARA CADASTRAR UM PRODUTO")
    print("DIGITE 2 PARA VER SEUS PRODUTOS CADASTRADOS")
    print("DIGITE 3 PARA DELETAR PRODUTO")
    print("DIGITE 4 PARA ALTERAR UM PRODUTO")
    print("DIGITE 5 PARA SAIR")
    numero_digitado = int(input(" "))
    if (numero_digitado == 1):
        cadastrar_produto()
    if (numero_digitado == 2):
        mostrar_produtos()
    if (numero_digitado == 3):
        deletar_produto()
    if (numero_digitado == 4):
        alterar_produto()
    if (numero_digitado == 5):
        sys.exit()
    else:
        print("Essa opção não existe")
        menu()


menu()