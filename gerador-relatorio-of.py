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


def replacer(match):
    return match.group(2)+'$'+(match.group(5) or match.group(3))+'\n' + ('\n' if  match.group(1) else '')

stdout,stderr = subprocess.Popen(['git', 'log', period, '--name-status', '--author', author], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT).communicate()

result = stdout.decode('utf-8')
data = re.sub(r'commit.*\n(.*\n)?Author.*\nDate:\s\s\s(.*)\n\n\s\s\s\s((Task )?(\d+)|.*).*\n\n', replacer, result)
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
def makeCommitFromString(commitString):
    commitLinhas = commitString.splitlines()
    taskData = commitLinhas[0].split('$')
    arquivos = list(map(makeArquivo, commitLinhas[1:]))
    return Commit(taskData[1], datetime.strptime(taskData[0], '%a %b %d %H:%M:%S %Y %z'), arquivos)




def printResultadoTasks(resultado):
    for task in filter(lambda task: not len(filterTasks) or task in filterTasks, resultadoTasks.keys()):
        print(task, len(resultado[task]))
        resultado[task].sort(key=lambda a: (a.operacao, a.nome))
        for i in resultado[task]:
            print(i.operacao +' '+ i.nome)
        print('')


def printPlanilha(resultadoTasks):
    itensPlanilha = [
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação JavaScript', ['.ts', '.js'], 'A', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração JavaScript', ['.ts', '.js'], 'M', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação de tela HTML ou XHTML ou JSP ou XML ou VTL ou XSL ou Swing ou AWT ou XUI ou PHP', ['.html'], 'A', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração de tela HTML ou XHTML ou JSP ou XML ou VTL ou XSL ou Swing ou AWT ou XUI ou PHP', ['.html'], 'M', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação CSS ou SCSS', ['.css', '.scss', 'sass', 'less'], 'A', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração CSS ou SCSS', ['.css', '.scss', 'sass', 'less'], 'M', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação de objetos de Integração e Negócio Java', ['.java'], 'A', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração de Objetos de Integração e Negócio Java', ['.java'], 'M', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação de arquivo chave/valor ou tipo xml', ['.json', '.xml'], 'A', {}),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração de arquivo chave/valor ou tipo xml', ['.json', '.xml'], 'M', {}),
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
    


commits = list(map(makeCommitFromString, data.split('\n\n')))
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
