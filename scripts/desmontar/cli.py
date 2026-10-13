"""Linha de comando: desmontar novo | validar | conferir | lentes."""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

from . import __version__
from .comum import casa, erros, raiz, slug
from .dossie import INTENCOES, MODOS, PARTES_DO_PROJETO, PROJETO
from .dossie import validar as validar_dossie
from . import fontes as _fontes
from . import lentes as _lentes


def _imprimir(achados, como_json: bool, extra: dict | None = None) -> int:
    if como_json:
        print(json.dumps({"achados": [a.dict() for a in achados], **(extra or {})}, ensure_ascii=False, indent=2))
    else:
        for a in achados:
            print(f"[{a.nivel}] {a.item}: {a.achado}")
        n = len(erros(achados))
        print(f"{n} erro(s), {sum(1 for a in achados if a.nivel == 'aviso')} aviso(s).")
    return 1 if erros(achados) else 0


def cmd_novo(args) -> int:
    hoje = _dt.date.today().isoformat()
    modelo = (raiz() / "templates" / "dossie.md").read_text(encoding="utf-8")
    natureza, _, area = (args.lente or "<natureza>/<area>").partition("/")
    caminho, origem = _lentes.escolher(natureza, area) if args.lente else (None, "")
    versao = ""
    if caminho and origem != "modelo":
        from .comum import frontmatter
        versao = (frontmatter(caminho.read_text(encoding="utf-8")) or {}).get("versao", "")
    lente = f"{args.lente} v{versao} ({origem})" if args.lente and origem != "modelo" else (
        f"{args.lente} v0 (genoma)" if args.lente else "<natureza>/<area> v<N> (<origem>)")
    txt = (modelo.replace("<o que foi desmontado>", args.objeto, 1)
                 .replace("data: <AAAA-MM-DD>", f"data: {hoje}", 1)
                 .replace("modo: <pessoal | publicar | cliente | projeto>", f"modo: {args.modo}", 1)
                 .replace("intencao: <entender | verificar | reproduzir | criar-projeto>", f"intencao: {args.intencao}", 1)
                 .replace("lente: <natureza>/<area> v<N> (<semente | aprendida | genoma | hibrida>)", f"lente: {lente}", 1)
                 .replace("# Desmontagem: <objeto>", f"# Desmontagem: {args.objeto}", 1))
    if args.modo == "projeto" or args.intencao == "criar-projeto":
        txt += f"\n## {PROJETO}\n" + "".join(f"\n### {p}\n<...>\n" for p in PARTES_DO_PROJETO)
    pasta = Path(args.dir).expanduser() if args.dir else casa() / "dossies"
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / f"{hoje}-{slug(args.objeto)}.md"
    if destino.exists():
        print(f"já existe: {destino}")
        return 1
    destino.write_text(txt, encoding="utf-8")
    print(destino)
    return 0


def cmd_validar(args) -> int:
    txt = Path(args.dossie).read_text(encoding="utf-8")
    return _imprimir(validar_dossie(txt, args.modo), args.json)


def cmd_conferir(args) -> int:
    txt = Path(args.dossie).read_text(encoding="utf-8")
    from .comum import frontmatter
    modo = args.modo or (frontmatter(txt) or {}).get("modo") or "pessoal"
    achados, tabela = _fontes.conferir(txt, modo=modo, offline=args.offline)
    if not args.json:
        for linha in tabela:
            print(f"{linha['ref']}: autoridade {linha['autoridade']} · {linha['alvo']}")
    return _imprimir(achados, args.json, {"fontes": tabela})


def cmd_lentes(args) -> int:
    if args.acao == "listar":
        for l in _lentes.listar():
            print(f"{l['id']} v{l['versao']} ({l['origem']})  {l['caminho']}")
        return 0
    if args.acao == "escolher":
        caminho, origem = _lentes.escolher(args.alvo, args.extra)
        print(json.dumps({"lente": f"{args.alvo}/{args.extra}", "origem": origem, "caminho": str(caminho)},
                         ensure_ascii=False))
        return 0
    if args.acao == "mostrar":
        caminho, origem = _lentes.escolher(*args.alvo.split("/", 1))
        print(caminho.read_text(encoding="utf-8"))
        return 0
    if args.acao == "checar":
        txt = Path(args.alvo).read_text(encoding="utf-8")
        return _imprimir(_lentes.checar(txt, links=args.links), args.json)
    if args.acao == "gravar":
        if not args.dossie:
            print("gravar exige --dossie <dossie aprovado>")
            return 1
        achados, destino = _lentes.gravar(Path(args.alvo), Path(args.dossie), links=not args.offline)
        codigo = _imprimir(achados, args.json)
        if destino:
            print(f"gravada: {destino}")
        return codigo
    if args.acao == "historico":
        for r in _lentes.historico(args.alvo):
            print(json.dumps(r, ensure_ascii=False))
        return 0
    if args.acao == "voltar":
        achados, destino = _lentes.voltar(args.alvo, int(args.extra))
        codigo = _imprimir(achados, args.json)
        if destino:
            print(f"lente atual: {destino}")
        return codigo
    return 1


def construir() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="desmontar",
        description="Desmontar v1.0.0 — Engenharia reversa com evidência e lentes por Nei Maciel (@neimaciel)",
        epilog="Desenvolvido por Nei Maciel | X: @neimaciel | Instagram: @neimaciel.ia | https://github.com/neimaciel/desmontar"
    )
    p.add_argument("--version", action="version", version=f"desmontar {__version__} by Nei Maciel (@neimaciel)")
    sub = p.add_subparsers(dest="comando", required=True)

    n = sub.add_parser("novo", help="cria um dossiê a partir de templates/dossie.md")
    n.add_argument("objeto")
    n.add_argument("--modo", choices=MODOS, default="pessoal")
    n.add_argument("--intencao", choices=INTENCOES, default="entender")
    n.add_argument("--lente", help="natureza/area")
    n.add_argument("--dir", help="pasta de destino (padrão: ~/Documents/desmontar/dossies)")
    n.set_defaults(func=cmd_novo)

    v = sub.add_parser("validar", help="confere a estrutura e os rótulos de um dossiê")
    v.add_argument("dossie")
    v.add_argument("--modo", choices=MODOS)
    v.add_argument("--json", action="store_true")
    v.set_defaults(func=cmd_validar)

    c = sub.add_parser("conferir", help="abre as fontes: DOI, retratação, título, links")
    c.add_argument("dossie")
    c.add_argument("--modo", choices=MODOS)
    c.add_argument("--offline", action="store_true")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_conferir)

    l = sub.add_parser("lentes", help="listar | escolher | mostrar | checar | gravar | historico | voltar")
    l.add_argument("acao", choices=["listar", "escolher", "mostrar", "checar", "gravar", "historico", "voltar"])
    l.add_argument("alvo", nargs="?")
    l.add_argument("extra", nargs="?")
    l.add_argument("--dossie")
    l.add_argument("--links", action="store_true")
    l.add_argument("--offline", action="store_true")
    l.add_argument("--json", action="store_true")
    l.set_defaults(func=cmd_lentes)
    return p


def main(argv: list[str] | None = None) -> int:
    args = construir().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
