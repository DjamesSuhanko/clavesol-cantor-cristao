"""Adiciona o banner somente à entrada e às cópias idênticas dessa página."""
from pathlib import Path
import re
import shutil
from carousel import banner, images


def add_carousel(root, out, base):
    entry = out / 'index.html'
    original = entry.read_text(encoding='utf-8')
    if 'class="collection-carousel"' in original:
        raise ValueError('A entrada já contém um carrossel; integração duplicada.')
    marker = re.search(r'<[a-z]+\b[^>]*class=["\'][^"\']*\blist-search\b[^"\']*["\'][^>]*>', original)
    if not marker:
        marker = re.search(r'<div\b[^>]*id=["\']hymn-search-controls["\'][^>]*>', original)
    if marker:
        position = marker.start()
    else:
        main = re.search(r'<main\b[^>]*>', original)
        if not main:
            raise ValueError('Página inicial sem <main> para inserir o carrossel.')
        position = main.end()
    html = original[:position] + banner(root, base) + original[position:]
    # Os hinários também publicam a entrada em /partituras/hinos/<coleção>/.
    aliases = [p for p in out.rglob('index.html') if p.read_text(encoding='utf-8') == original]
    for path in aliases:
        path.write_text(html, encoding='utf-8')
    (out / 'carrossel').mkdir(exist_ok=True)
    for name in images(root):
        shutil.copyfile(root / 'carrossel' / name, out / 'carrossel' / name)
    (out / 'assets').mkdir(exist_ok=True)
    for name in ('carrossel.css', 'carrossel.mjs'):
        shutil.copyfile(root / 'assets' / name, out / 'assets' / name)
