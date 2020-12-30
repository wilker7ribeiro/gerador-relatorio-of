# Gerador Relatorio de atividades

Este projeto tem por objetivo auxiliar na geração de relatorio de atividades, ele retorna os arquivos criados e modificados através dos commits fornecidos como parametros.

# Usage

```
python3 gerador-relatorio-of.py <Author> <Período> <Projeto> <TaskFiltro1> <TaskFiltro2> ...<TaskFiltroN>
```

Author - Autor dos commits

Período - Periodo de análise (ex: 649745097d8135f5b8eb6c1678ab9e2330401391...8db5d657f4d1e3856c54c7558dda81c78a3e082f^1)

Projeto - Nome do projeto

TaskFiltros - Quais tasks vão ser analisadas

# Example
```
python3 gerador-relatorio-of.py C9999999 HEAD...8db5d657f4d1e3856c54c7558dda81c78a3e082f^1 big-projeto-estatico
```
```
python3 gerador-relatorio-of.py C9999999 649745097d8135f5b8eb6c1678ab9e2330401391...8db5d657f4d1e3856c54c7558dda81c78a3e082f^1 big-projeto-estatico 1923423 1242312
```