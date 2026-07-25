# Como contribuir

Obrigado por considerar contribuir! Aqui estão as diretrizes.

## Fluxo de trabalho

1. Faça um **fork** do repositório
2. Crie uma branch descritiva: `git checkout -b feat/nome-da-feature` ou `fix/descricao-do-bug`
3. Faça suas alterações com commits claros (veja convenção abaixo)
4. Garanta que **todos os testes passam**: `pytest -v`
5. Abra um **Pull Request** descrevendo o que foi feito e por quê

## Convenção de commits

Use o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adiciona filtro de gastos por valor máximo
fix: corrige erro ao excluir categoria com gastos vinculados
test: adiciona testes para o resumo mensal
docs: atualiza exemplos de curl no README
refactor: extrai validação de UUID para helper
```

## Rodando os testes

```bash
# Suíte completa (usa SQLite em memória, sem Postgres necessário)
pytest -v

# Com relatório de cobertura
pytest --cov=app --cov-report=term-missing
```

Novos recursos **devem vir acompanhados de testes**.

## Adicionando uma nova rota

Siga a separação em camadas do projeto:

1. Se necessário, crie ou ajuste o **model** em `app/models/`
2. Gere uma **migration**: `alembic revision --autogenerate -m "descrição"`
3. Crie ou ajuste o **schema Pydantic** em `app/schemas/`
4. Adicione a regra de negócio no **serviço** em `app/services/`
5. Se precisar de nova query, adicione no **repositório** em `app/repositories/`
6. Registre o endpoint na **rota** em `app/api/v1/routes/`
7. Escreva os **testes** em `tests/`

## Reportando bugs

Abra uma issue descrevendo: o comportamento esperado, o comportamento atual e como reproduzir o problema.
