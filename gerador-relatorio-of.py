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
resultadoTasks = {}
renomeacoes = []
delecoes = []
filterTasks = inputArgs[4:]



stdout,stderr = subprocess.Popen(['git', 'log', period, '--name-status', '--author', author], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT).communicate()

result = stdout.decode('utf-8')
commits_data = re.findall('commit (.*\n)?Author: (.*)\nDate:   (.*)\n\n((.*\n)+?)\n(((A|M|R|D).+\n)+)', result)
#incluir-agendamento-incluir-comando.component.ts

class Commit:
    def __init__(self, task, data, arquivos):
        self.task = task
        self.data = data
        self.arquivos = arquivos

class Arquivo:
    def __init__(self, operacao, nome, nomeAntigo):
        self.operacao = operacao
        self.nome = nome
        self.nomeAntigo = nomeAntigo

class Renomeacao:
    def __init__(self, nomeNovo, nomeAntigo):
        self.nomeNovo = nomeNovo
        self.nomeAntigo = nomeAntigo

class ResultadoTask:
    def __init__(self, operacao, nome):
        self.operacao = operacao
        self.nome = nome

class ItemPlanilha:
    def __init__(self, cells, exts, operacao, itensTasks):
        self.cells = cells
        self.exts = exts
        self.operacao = operacao
        self.itensTasks = itensTasks

def makeArquivo(linha):
    parts = linha.split('\t')
    operacao = parts[0]
    nome = parts[1] if len(parts) < 3 else parts[2]
    nomeAntigo = None if len(parts) < 3 else parts[1]
    return Arquivo(operacao, nome, nomeAntigo)
def makeCommitFromString(commits_data):
    commit_id = commits_data[0]
    commit_author = commits_data[1]
    commit_date_string = commits_data[2]
    commit_text = commits_data[3].strip()
    task_finds = re.findall('((T|t)ask )(\d+)', commit_text)
    commit_task = commit_text if not task_finds else task_finds[0][2]
    arquivos = list(map(makeArquivo, filter(None, commits_data[5].split('\n'))))
    return Commit(commit_task, datetime.strptime(commit_date_string, '%a %b %d %H:%M:%S %Y %z'), arquivos)




def printResultadoTasks(resultado):
    for task in filter(lambda task: not len(filterTasks) or task in filterTasks, resultadoTasks.keys()):
        print(task, len(resultado[task]))
        resultado[task].sort(key=lambda a: (a.operacao, a.nome))
        for i in resultado[task]:
            print(i.operacao +' '+ i.nome)
        print('')


def printPlanilha(resultadoTasks):
    itensPlanilha = [
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

    resultadoTasks
    for task in filter(lambda task: not len(filterTasks) or task in filterTasks, resultadoTasks.keys()):
        resultadoTasks[task].sort(key= lambda a: a.operacao)

        for arquivo in resultadoTasks[task]: 
            config = next(filter(lambda itemPlan: itemPlan.operacao == arquivo.operacao and any(arquivo.nome.endswith(ext) for ext in itemPlan.exts), itensPlanilha), None)
            if config:
                if task not in config.itensTasks:
                    config.itensTasks[task] = []
                config.itensTasks[task].append(arquivo.nome)
            else:
                print('Configuração não encontrada para arquivo: ' + arquivo.operacao + ' ' + arquivo.nome)

    for itemPlanilha in itensPlanilha:
        sum = 0
        string = ''
        for task in itemPlanilha.itensTasks.keys():
            string += 'Task ' + task + '\n'
            string += '\n'.join(list(map(lambda i : nomeProjeto+'/'+i, itemPlanilha.itensTasks[task])))
            string += '\n\n'
            sum += len(itemPlanilha.itensTasks[task])
        if sum:

            print('======', itemPlanilha.cells, sum)
            print(string)
    


commits = list(map(makeCommitFromString, commits_data))
commits.sort(key=lambda r: r.data, reverse=True)


for commit in commits:
    for arquivo in commit.arquivos:
        if not commit.task in resultadoTasks:
            resultadoTasks[commit.task] = []
        if not arquivo.operacao or not arquivo.nome:
            continue

        if arquivo.operacao.startswith('R'):
            renomeacaoAntiga = next(filter(lambda i: i.nomeAntigo == arquivo.nome, renomeacoes), None)
            if renomeacaoAntiga:
                arquivo.nome = renomeacaoAntiga.nomeNovo

            renomeacoes.append(Renomeacao(arquivo.nome, arquivo.nomeAntigo))

            if arquivo.operacao[1:] == '100':
                continue
            arquivo.operacao = 'M'
        else:
            renomeado = next(filter(lambda i: i.nomeAntigo == arquivo.nome, renomeacoes), None)
            if renomeado:
                arquivo.nome = renomeado.nomeNovo
                
        if arquivo.nome in delecoes:
            continue
        
        if arquivo.operacao == 'D':
            delecoes.append(arquivo.nome)
            continue
        
        arquivoResultadoTasks = next(filter(lambda i: i.nome == arquivo.nome, resultadoTasks[commit.task]), None)
        if arquivoResultadoTasks:
            if arquivoResultadoTasks.operacao != 'A' and arquivo.operacao == 'A':
                arquivoResultadoTasks.operacao = arquivo.operacao
            continue
        
        resultadoTasks[commit.task].append(ResultadoTask(arquivo.operacao, arquivo.nome))


print('=============================== RESULTADO DAS TASKS ================================ ')
print('')
printResultadoTasks(resultadoTasks)

print('')
print('=========================')
print('=========================')
print('=========================')
print('')

print('============================== RESULTADO PARA PLANILHA ============================= ')
print('')
printPlanilha(resultadoTasks)


#git log 649745097d8135f5b8eb6c1678ab9e2330401391...a30159ec30273f624a5efd4aa027e136e0ed8d54^1 --author=C1317576 --name-status