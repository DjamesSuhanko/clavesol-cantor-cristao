# Clave Sol — Cantor Cristão

Estrutura independente do hinário, com identidade visual Clave Sol, busca por número/título e player com andamento em BPM e cursor sincronizado. **Ainda não há hinos convertidos ou publicados.** Nenhum XML original foi copiado ou alterado nesta etapa.

## GitHub Pages

1. No repositório, abra **Settings → Pages**.
2. Em **Source**, selecione **GitHub Actions**. Deixe **Custom domain** vazio.
3. Em **Actions → Publicar Cantor Cristão → Run workflow**, escolha `main` e execute.
4. O endereço será https://djamessuhanko.github.io/clavesol-cantor-cristao/.

O commit inicial usa `[skip ci]` para permitir configurar o Pages antes da primeira execução. Os próximos pushes em `main` publicam automaticamente.

## Prévia local

Requer Python 3.12+ e Node.js 22+ para os testes do player e da busca.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
BASE_PATH= .venv/bin/python build.py
BASE_PATH= .venv/bin/python scripts/check_links.py
python3 -m http.server 8000 --directory dist
```

Sem `BASE_PATH`, o build usa `/clavesol-cantor-cristao`. A busca ignora acentos e zeros iniciais, combina palavras e compara números completos (buscar 10 não mostra 110). Funciona localmente no navegador, sem serviço externo.

## Receber os hinos preparados

Consulte [docs/ADICIONAR-HINOS.md](docs/ADICIONAR-HINOS.md). O catálogo é gerado a partir dos Markdown e a busca incorpora automaticamente cada hino publicado. Os arquivos de `assets/music.*`, `music_pages.py` e módulos de MusicXML foram copiados do blog; a busca fica isolada em `catalog_home.py` e `assets/hymn-search.*`.

A estrutura não inclui conversor novo nem executa conversão. Os XML de origem continuam em `/home/djames/Documents/ClaveSol/CantorCristao/`. O script de sincronização dos quatro repositórios existentes ainda não inclui este repositório.
