# Adicionar hinos após a conversão

Os XML originais permanecem em `/home/djames/Documents/ClaveSol/CantorCristao/`. A conversão para as páginas SVG e o mapa de tempo será preparada em uma próxima etapa. Colocar apenas um XML na pasta não publica um player completo. Não há exportação de PDF nesta estrutura.

Cada hino preparado ocupará duas pastas correspondentes:

```text
partituras/hinos/cantor-cristao/hino-001.md
assets/music/hinos/cantor-cristao/hino-001/
    score.musicxml
    score-1.svg
    score-2.svg       (se houver outras páginas)
    timing.json
    score.mscz       (opcional)
```

Exemplo de Markdown (modelo, ainda não publicado):

```markdown
Title: Hino 1 — Título do hino
Author: Nome do autor
Instrument: Quatro vozes
Lesson: 1
Playback: generated
Cursor: true
Draft: false

Texto opcional sobre o hino.
```

`Lesson` define o número usado na ordenação e busca. As páginas SVG devem ser consecutivas, começando em 1. O `timing.json` deve corresponder ao MusicXML e às páginas SVG. O build valida o catálogo, exige reprodução gerada com cursor e produz `sequence.json` automaticamente na pasta `dist`.

Use `Draft: true` enquanto um hino ainda não estiver pronto. Não faça commit de `dist`. Valide o build e os links antes do push. O player atual contém o tratamento existente de fermatas e repetições; a compatibilidade dos XML deste acervo será aferida durante a conversão, não está garantida por esta estrutura.
