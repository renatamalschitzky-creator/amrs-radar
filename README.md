# AMRS · Radar de Mercado

Portal de notícias automático com atualização diária via GitHub Actions.

## Estrutura
```
amrs-radar/
├── index.html              → portal visual
├── fetch_news.py           → script de coleta de notícias
├── data/
│   └── news.json           → notícias coletadas (gerado automaticamente)
└── .github/workflows/
    └── update.yml          → agendamento diário 07:00 BRT
```

## Como publicar (uma vez só)

1. Crie um repositório no GitHub (pode ser privado)
2. Suba estes arquivos para o repositório
3. Vá em **Settings → Pages → Source → GitHub Actions**
4. Aguarde o primeiro deploy

O portal ficará disponível em:
`https://SEU_USUARIO.github.io/amrs-radar/`

## Como testar localmente

```bash
pip install feedparser
python fetch_news.py
# abra o index.html no navegador
```

## Personalizar fontes RSS

Edite o arquivo `fetch_news.py` — cada seção tem:
- `keywords`: palavras que filtram as notícias relevantes
- `sources`: feeds RSS das fontes de notícia

## Atualização manual

No GitHub, vá em **Actions → Atualizar Radar AMRS → Run workflow**.

---
*A Minha Rede Social · AMRS*
