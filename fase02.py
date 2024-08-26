import tabulate
import sys
import oracledb

try:
 conexao = oracledb.connect(
 user="ISA",
 password="isabelle",
 dsn="localhost/XEPDB1")
except Exception as erro:
 print ('Erro em conexão', erro)
else:
 print ("Conectado", conexao.version)

 # Criar Cursor
 cursor= conexao.cursor()

# Cria a tabela estoque
'''cursor.execute ("""
CREATE TABLE ESTOQUE (
cod_prod INTEGER PRIMARY KEY,
nome VARCHAR2(50),
descrição VARCHAR2(150),
preço_venda FLOAT,
preço_venda_pct DECIMAL(5,2),
custo_prod FLOAT,
custo_prod_pct DECIMAL(5,2),
receita_bruta FLOAT,
receita_bruta_pct DECIMAL(5,2),
custo_fixo FLOAT,
custo_fixo_pct DECIMAL(5,2),
comissão_de_venda FLOAT,
comissão_de_venda_pct DECIMAL(5,2),
impostos FLOAT,
impostos_pct DECIMAL(5,2),
outros_custos FLOAT,
outros_custos_pct DECIMAL(5,2),
rentabilidade FLOAT,
rentabilidade_pct DECIMAL(5,2)
 )""")'''
 

def mostrar_produtos():
    from tabulate import tabulate

    sql_select_Query = "SELECT * FROM estoque"
    cursor = conexao.cursor()
    cursor.execute(sql_select_Query)
    produtos = cursor.fetchall()

    for row in produtos:
        print("\nId:", row[0])
        print("Nome:", row[1])
        print("Descrição:", row[2])   
        #print("\n")
        data = [
            ["A. Preço de Venda:", f'{row[3]:.2f}', f'{row[4]:.0f}%'],
            ['B. Custo de Aquisição (Fornecedor)', f'{row[5]:.2f}', f'{row[6]:.0f}%'],
            ['C. Receita Bruta', f'{row[7]:.2f}', f'{row[8]:.0f}%'],
            ['D. Custo Fixo/Administrativo', f'{row[9]:.2f}', f'{row[10]:.0f}%'],
            ['E. Comissão de Vendas', f'{row[11]:.2f}', f'{row[12]:.0f}%'],
            ['F. Impostos', f'{row[13]:.2f}', f'{row[14]:.0f}%'],
            ['G. Outros Custos (D+E+F)', f'{row[15]:.2f}', f'{row[16]:.0f}%'],
            ['H. Rentabilidade (C-G)', f'{row[17]:.2f}', f'{row[18]:.0f}%\n']]
        print(tabulate(data, headers=["Descrição", "Valor", "%"], floatfmt=".2f"))
        if (row[17] > 0):
            if (row[17] <= 10):
                print("Lucro Baixo")
            if (row[17] > 10 and row[17] <= 20):
                print("Lucro médio")
            if (row[17] > 20):
                print("Lucro Alto")

        else:
            if (row[17] == 0):
                print("Equilíbrio")
            else:
                print("Prejuízo")
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
    ca = float(input('Custo do produto: '))
    cf = float(input('Custo fixo: '))
    cv = float(input('Comissão de vendas: '))
    iv = float(input('Impostos: '))
    ml = float(input('Rentabilidade: '))



    # cálculo preço de venda
    pv = ca / (1 - ((cf + cv + iv + ml) / (100)))

    # um porcento

    # cálculo receita bruta
    rb = pv - ca

    # cálculo de lucro
    mc = ((cf + cv + iv + ml) / pv) - 100

    # valor sobre o preço final
    valor_imposto = (iv / 100) * pv
    valor_comissao = (cv / 100) * pv
    valor_custofixo = (cf / 100) * pv

    # cálculo outros custos e rentabilidade
    oc = valor_imposto + valor_comissao + valor_custofixo
    rentabilidade = rb - oc


    #valores em porcentagem
    pct_pv=((pv / pv) * 100)
    pct_ca=((ca / pv) * 100)
    pct_rb=((rb / pv) * 100)
    pct_custofix=((valor_custofixo / pv) * 100)
    pct_comissao=((valor_comissao / pv) * 100)
    pct_imp=((valor_imposto / pv) * 100)
    pct_oc=((oc / pv) * 100)
    pct_rent=((rentabilidade / pv) * 100)


    # data = dados que vão aparecer na tabela, hearders = cabeçario


    comando = f"""INSERT INTO ESTOQUE( cod_prod,nome,descrição,preço_venda,preço_venda_pct,custo_prod,custo_prod_pct,receita_bruta,receita_bruta_pct,custo_fixo,custo_fixo_pct,comissão_de_venda,comissão_de_venda_pct,impostos,impostos_pct,outros_custos,outros_custos_pct, rentabilidade,rentabilidade_pct)
    VALUES
        ( {cod_prod}, '{nome}', '{descricao}',{pv},{pct_pv}, {ca},{pct_ca},{rb},{pct_rb} ,{valor_custofixo},{pct_custofix}, {valor_comissao},{pct_comissao}, {valor_imposto},{pct_imp},{oc},{pct_oc}, {rentabilidade},{pct_rent})"""

    cursor.execute(comando)
    conexao.commit() 
    print('Produto Cadastrado!')
    print("\n")
    from tabulate import tabulate #para importar usamos o terminal e colocamos o camando: pip install tabulate
    data = [[ 'A. Preço de Venda', f'{pv:.2f}', f'{pct_pv:.0f}%'],
    ['B. Custo de Aquisição (Fornecedor)',  f'{ca:.2f}', f'{pct_ca:.0f}%'],
    ['C. Receita Bruta', f'{rb:.2f}', f'{pct_rb:.0f}%'],
    ['D. Custo Fixo/Administrativo', f'{valor_custofixo:.2f}', f'{pct_custofix:.0f}%'],
    ['E. Comissão de Vendas', f'{valor_comissao:.2f}', f'{pct_comissao:.0f}%'],
    ['F. Impostos', f'{valor_imposto:.2f}', f'{pct_imp:.0f}%'],
    ['G. Outros Custos (D+E+F)', f'{oc:.2f}', f'{pct_oc:.0f}%'],
    ['H. Rentabilidade (C-G)', f'{rentabilidade:.2f}', f'{pct_rent:.0f}%\n']]
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
        print("Prejuízo....")
    menu()

def menu():

    print("\n-----MENU-----\n")
    print("DIGITE 1 PARA CADASTRAR UM PRODUTO")
    print("DIGITE 2 PARA VER SEUS PRODUTOS CADASTRADOS")
    print("DIGITE 3 PARA SAIR")
    numero_digitado=int(input(" "))
    if(numero_digitado==1):
        cadastrar_produto()
    if(numero_digitado==2):
        mostrar_produtos()
    if(numero_digitado==3):
        sys.exit()
    else:
        print("Essa opção não existe")
        menu()

menu()
