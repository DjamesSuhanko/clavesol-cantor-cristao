# Conversão em segundo plano

O script `scripts/converter_cantor_cristao.py` lê os XML originais sem alterá-los, abre uma cópia no MuseScore e usa o importador validado do Clave Sol para gerar MusicXML, SVGs, MuseScore e cursor. Sem PDFs. O áudio é sintetizado pelo player.

Destino exclusivo: `partituras/hinos/cantor-cristao/` e `assets/music/hinos/cantor-cristao/`, no repositório independente. Não transpõe nem mistura arquivos nos hinários Bb, Eb e C.

Estado e logs: `/home/djames/Documents/ClaveSol/lab/cantor-cristao-conversao/`. O `status.json` registra sucessos, falhas e conclusão; `logs/` contém um arquivo por hino e `build.log` a validação final.

Para retomar, execute o mesmo script com o Python do ambiente do blog. Ele ignora sucessos cujos originais e arquivos produzidos não mudaram; falhas são tentadas novamente. Há um bloqueio contra duas execuções simultâneas. Cada hino tem limite de 15 minutos. Hinos incompatíveis são registrados e o lote continua. Não há commit nem push automático.

```bash
/home/djames/Documents/ClaveSol/site/clavesol/.venv/bin/python -u scripts/converter_cantor_cristao.py
```

Ao final, o build inclui os hinos prontos na listagem e na busca. Títulos genéricos do XML, como “Title”, aparecem como “Hino N” e podem ser preenchidos posteriormente no Markdown.

Versões com letras são preservadas: `cc060a-4vozes.xml` gera `hino-060a` (Hino 60A), e `cc060b-4vozes.xml` gera `hino-060b` (Hino 60B). Cada versão tem arquivos, logs e controle de retomada independentes. Arquivos sem letra mantêm o nome anterior, como `hino-326`. Colisões reais de identificadores interrompem o lote e informam os nomes envolvidos.
