import subprocess
import sys
import re
from datetime import datetime  

inputArgs = sys.argv
if len(inputArgs) < 4:
    print('usage python3 ../teste.py <Author> <Periodo> <nome-projeto> <task-filtro1> <task-filtro2>...')
    exit()


author = inputArgs[1]
period = inputArgs[2]
nomeProjeto = inputArgs[3]
resultado_tasks = {}
renomeacoes = []
delecoes = []
filter_tasks = inputArgs[4:]



stdout,stderr = subprocess.Popen(['git', 'log', period, '--name-status', '--author', author], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT).communicate()

result = stdout.decode('utf-8')
commits_data = re.findall('commit (.*)\n?Author: (.*)\nDate:   (.*)\n\n((.*\n)+?)\n(((A|M|R|D).+\n)+)', result)
#incluir-agendamento-incluir-comando.component.ts

class Commit:
    def __init__(self, id, text, task, data, arquivos):
        self.id = id
        self.text = text
        self.task = task
        self.data = data
        self.arquivos = arquivos

class Arquivo:
    def __init__(self, commit_id, operacao, nome, nome_antigo):
        self.commit_id = commit_id
        self.operacao = operacao
        self.nome = nome
        self.nome_antigo = nome_antigo

class Renomeacao:
    def __init__(self, nome_novo, nome_antigo):
        self.nome_novo = nome_novo
        self.nome_antigo = nome_antigo

class ResultadoTask:
    def __init__(self, operacao, nome, commits):
        self.commits = commits
        self.operacao = operacao
        self.nome = nome

class ItemPlanilha:
    def __init__(self, cells, exts, operacao, itens_tasks):
        self.cells = cells
        self.exts = exts
        self.operacao = operacao
        self.itens_tasks = itens_tasks

def make_arquivo(linha, commit_id):
    parts = linha.split('\t')
    operacao = parts[0]
    nome = parts[1] if len(parts) < 3 else parts[2]
    nome_antigo = None if len(parts) < 3 else parts[1]
    return Arquivo(commit_id, operacao, nome, nome_antigo)


def make_commit_from_string(commits_data):
    commit_id = commits_data[0]
    commit_author = commits_data[1]
    commit_date_string = commits_data[2]
    commit_text = commits_data[3].strip()
    task_finds = re.findall('((T|t)ask )(\d+)', commit_text)
    commit_task = commit_text if not task_finds else task_finds[0][2]
    arquivos = list(map(lambda linha: make_arquivo(linha, commit_id), filter(None, commits_data[5].split('\n'))))
    return Commit(commit_id, commit_text, commit_task, datetime.strptime(commit_date_string, '%a %b %d %H:%M:%S %Y %z'), arquivos)




def print_resultado_tasks(resultado):
    for task in filter(lambda task: not len(filter_tasks) or task in filter_tasks, resultado_tasks.keys()):
        print(task, len(resultado[task]))
        resultado[task].sort(key=lambda a: (a.operacao, a.nome))
        for i in resultado[task]:
            print(i.operacao +' '+ i.nome)
        print('')


def print_planilha(resultado_tasks, com_commit=False):
    itens_planilha = [
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação JavaScript', ['.ts', '.js', '.tsx'], 'A', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração JavaScript', ['.ts', '.js', '.tsx'], 'M', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação de tela HTML ou XHTML ou JSP ou XML ou VTL ou XSL ou Swing ou AWT ou XUI ou PHP', ['.html'], 'A', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração de tela HTML ou XHTML ou JSP ou XML ou VTL ou XSL ou Swing ou AWT ou XUI ou PHP', ['.html'], 'M', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação CSS ou SCSS', ['.css', '.scss', 'sass', 'less'], 'A', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração CSS ou SCSS', ['.css', '.scss', 'sass', 'less'], 'M', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação de objetos de Integração e Negócio Java', ['.java'], 'A', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração de Objetos de Integração e Negócio Java', ['.java'], 'M', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação de arquivo chave/valor ou tipo xml', ['.json', '.xml'], 'A', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração de arquivo chave/valor ou tipo xml', ['.json', '.xml'], 'M', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Software de Infraestrutura 	Criação de módulo em Python', ['.py'], 'A', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Software de Infraestrutura 	Alteração de módulo em Python', ['.py'], 'M', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Software de Infraestrutura 	Elaboração e criação de arquivo de definição "Dockerfile"', ['Dockerfile'], 'A', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Software de Infraestrutura 	Alteração de arquivo de definição "Dockerfile"', ['Dockerfile'], 'M', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Implementação de aplicação Cloud	Construção/Alteração de arquivos requirements ou values para deploy no ambiente Cloud', ['values.yaml', 'requirements.yaml'], 'A', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Implementação de aplicação Cloud	Construção/Alteração de arquivos requirements ou values para deploy no ambiente Cloud', ['values.yaml', 'requirements.yaml'], 'M', {})
        
    ]

    for task in filter(lambda task: not len(filter_tasks) or task in filter_tasks, resultado_tasks.keys()):
        resultado_tasks[task].sort(key= lambda a: a.operacao)

        for arquivo in resultado_tasks[task]: 
            config = next(filter(lambda item_plan: item_plan.operacao == arquivo.operacao and any(arquivo.nome.endswith(ext) for ext in item_plan.exts), itens_planilha), None)
            if config:
                if task not in config.itens_tasks:
                    config.itens_tasks[task] = []
                config.itens_tasks[task].append(arquivo)
            else:
                print('Configuração não encontrada para arquivo: ' + arquivo.operacao + ' ' + arquivo.nome)
    print('')
    for item_planilha in itens_planilha:
        soma = 0
        string = ''
        for task in item_planilha.itens_tasks.keys():
            string += 'Task ' + task + '\n'
            if com_commit:
                base_url = 'https://fontes.intranet.bb.com.br'
                string += '\n'.join(list(map(lambda i : (base_url + '/'+nomeProjeto+ '/-/blob/' + i.commits[0].id + '/' + i.nome), item_planilha.itens_tasks[task])))
            else:
                string += '\n'.join(list(map(lambda i : (nomeProjeto+ '/' + i.nome ), item_planilha.itens_tasks[task])))
            string += '\n\n'
            soma += len(item_planilha.itens_tasks[task])
        if soma:

            print('======', item_planilha.cells, soma)
            print(string)
    


commits = list(map(make_commit_from_string, commits_data))
commits.sort(key=lambda r: r.data, reverse=True)


for commit in commits:
    for arquivo in commit.arquivos:
        if not commit.task in resultado_tasks:
            resultado_tasks[commit.task] = []
        if not arquivo.operacao or not arquivo.nome:
            continue

        if arquivo.operacao.startswith('R'):
            renomeacaoAntiga = next(filter(lambda i: i.nome_antigo == arquivo.nome, renomeacoes), None)
            if renomeacaoAntiga:
                arquivo.nome = renomeacaoAntiga.nome_novo

            renomeacoes.append(Renomeacao(arquivo.nome, arquivo.nome_antigo))

            if arquivo.operacao[1:] == '100':
                continue
            arquivo.operacao = 'M'
        else:
            renomeado = next(filter(lambda i: i.nome_antigo == arquivo.nome, renomeacoes), None)
            if renomeado:
                arquivo.nome = renomeado.nome_novo
                
        if arquivo.nome in delecoes:
            continue
        
        if arquivo.operacao == 'D':
            delecoes.append(arquivo.nome)
            continue
        
        arquivoResultadoTasks = next(filter(lambda i: i.nome == arquivo.nome, resultado_tasks[commit.task]), None)
        if arquivoResultadoTasks:
            if arquivoResultadoTasks.operacao != 'A' and arquivo.operacao == 'A':
                arquivoResultadoTasks.operacao = arquivo.operacao
            arquivoResultadoTasks.commits.append(commit)
            continue
        
        resultado_tasks[commit.task].append(ResultadoTask(arquivo.operacao, arquivo.nome, [commit]))





# print('=============================== RESULTADO DAS TASKS ================================ ')
# print('')
# print_resultado_tasks(resultado_tasks)
# 
# print('')
# print('=========================')
# print('=========================')
# print('=========================')
# print('')
# 
# print('============================== RESULTADO============================= ')
# 
# print_planilha(resultado_tasks, com_commit=False)
# print('')
# print('')
# print('')
# print('')
print('============================== RESULTADO PARA PLANILHA ============================= ')
print('')
print_planilha(resultado_tasks, com_commit=True)


#git log 649745097d8135f5b8eb6c1678ab9e2330401391...a30159ec30273f624a5efd4aa027e136e0ed8d54^1 --author=C1317576 --name-status
