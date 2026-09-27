"""Gera as imagens de prévia (1200x630): og.png, a partir da página inicial, e og-octante-N.png, a partir dos cartões."""
import asyncio
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from paginas import cartao_og  # noqa: E402
from teste import cartao_og_teste  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

PASTA = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/outputs/cubo-politico').resolve()
GL = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']


async def main():
    async with async_playwright() as p:
        nav = await p.chromium.launch(args=GL)
        ctx = await nav.new_context(viewport={'width': 1200, 'height': 630}, reduced_motion='reduce')
        pg = await ctx.new_page()
        await pg.goto((PASTA / 'index.html').as_uri())
        await pg.wait_for_timeout(2500)
        await pg.screenshot(path=str(PASTA / 'og.png'))
        for n in range(1, 9):
            tmp = PASTA / f'_og{n}.html'
            tmp.write_text(cartao_og(n), encoding='utf-8')
            await pg.goto(tmp.as_uri())
            await pg.evaluate('document.fonts.ready')
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(PASTA / f'og-octante-{n}.png'))
            tmp.unlink()
        tmp = PASTA / '_ogt.html'
        tmp.write_text(cartao_og_teste(), encoding='utf-8')
        await pg.goto(tmp.as_uri())
        await pg.evaluate('document.fonts.ready')
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=str(PASTA / 'og-teste.png'))
        tmp.unlink()
        await nav.close()
    for f in sorted(PASTA.glob('og*.png')):
        print(f.name, f.stat().st_size // 1024, 'KB')

asyncio.run(main())
