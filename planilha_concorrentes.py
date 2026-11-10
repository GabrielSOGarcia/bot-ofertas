# /planilha no painel (10/11, Gabriel): o que cada grupo concorrente mais posta e o que mais engaja, separado
# por nicho. Formato pedido: título PERFUME, subtítulo com cada grupo (grupo A, grupo B...), e os produtos que
# mais saem; depois CASA, depois GERAL. Vem do que o chip guardou (whatsapp/grupos_observados.json, pelo
# programa do WhatsApp). Encaminhamentos o WhatsApp não mostra para quem é membro: conta reação, quantas vezes
# o grupo repetiu o produto e em quantos grupos diferentes ele apareceu.
# Gera um .xlsx sem precisar de biblioteca (abre no Google Planilhas, LibreOffice ou no celular).
import io
import re
import time
import zipfile
from collections import defaultdict
from xml.sax.saxutils import escape

import concorrentes

NICHOS = [("PERFUME", ["perfume", "parfum", "fragranc"]),
          ("CASA", ["casa", "lar", "chef", "cozinha", "home", "decor", "sho"]),
          ("GERAL", [])]                       # o resto (tecnologia, promoções gerais...)
POR_GRUPO = 10                                  # produtos por grupo
_VAZIAS = {"de", "da", "do", "com", "para", "e", "o", "a", "em", "kit", "ml", "un", "cm", "original", "novo"}


def nicho_do_grupo(nome):
    n = concorrentes.normalizar(nome)
    for nicho, chaves in NICHOS:
        if any(c in n for c in chaves):
            return nicho
    return "GERAL"


# Linhas de propaganda que alguns grupos põem antes do nome (10/11: "A oferta pode acabar a qualquer momento",
# "Quer entrar em algum dos outros grupos oficiais", "Loja Oficial X no ML", "Válido no site todo")
_PROPAGANDA = re.compile(r"oferta pode acabar|grupos? oficia|entrar em algum|loja oficial|valido|v[aá]lido|"
                         r"cupom|frete|mercado livre|shopee|compre aqui|link|parcel|pix|^por\b|^de\b", re.I)


def titulo_produto(texto):
    linhas = [l for l in str(texto).splitlines() if not _PROPAGANDA.search(concorrentes.normalizar(l))]
    return concorrentes.titulo("\n".join(linhas))


def chave(titulo):
    # O mesmo produto escrito um pouco diferente: as 4 primeiras palavras que importam
    palavras = [p for p in re.findall(r"[a-z0-9]+", concorrentes.normalizar(titulo)) if p not in _VAZIAS]
    return " ".join(palavras[:4])


def ranking(grupos):
    # {nicho: [(nome do grupo, total de posts, [linhas])]}; linha = (produto, vezes, reações, grupos, preço)
    em_quantos = defaultdict(set)
    por_grupo = {}
    for jid, g in grupos.items():
        nome = g.get("nome") or jid
        prods = {}
        for p in g.get("posts") or []:
            t = titulo_produto(p.get("texto") or "")
            k = chave(t)
            if len(k.split()) < 2:
                continue
            a = prods.setdefault(k, {"titulo": t, "vezes": 0, "reacoes": 0, "preco": ""})
            a["vezes"] += 1
            a["reacoes"] += int(p.get("reacoes") or 0)
            a["preco"] = concorrentes.preco_final(p) or a["preco"]
            em_quantos[k].add(nome)
        por_grupo[nome] = (len(g.get("posts") or []), prods)
    saida = defaultdict(list)
    for nome, (total, prods) in por_grupo.items():
        def pontos(item):
            k, a = item
            return a["reacoes"] * 3 + (len(em_quantos[k]) - 1) * 2 + a["vezes"]
        top = sorted(prods.items(), key=pontos, reverse=True)[:POR_GRUPO]
        linhas = [(a["titulo"], a["vezes"], a["reacoes"], len(em_quantos[k]), a["preco"]) for k, a in top]
        saida[nicho_do_grupo(nome)].append((nome, total, linhas))
    for lista in saida.values():
        lista.sort(key=lambda x: -x[1])
    return saida


# ---------- .xlsx mínimo (uma aba, negrito nos títulos) ----------
_ESTILOS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<fonts count="4"><font><sz val="11"/><name val="Calibri"/></font>'
            '<font><b/><sz val="16"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>'
            '<font><b/><sz val="12"/><name val="Calibri"/></font>'
            '<font><b/><sz val="10"/><color rgb="FF555555"/><name val="Calibri"/></font></fonts>'
            '<fills count="4"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>'
            '<fill><patternFill patternType="solid"><fgColor rgb="FF1F2937"/></patternFill></fill>'
            '<fill><patternFill patternType="solid"><fgColor rgb="FFF3E9D8"/></patternFill></fill></fills>'
            '<borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs>'
            '<cellXfs count="4"><xf/>'
            '<xf fontId="1" fillId="2" applyFont="1" applyFill="1"/>'
            '<xf fontId="2" fillId="3" applyFont="1" applyFill="1"/>'
            '<xf fontId="3" applyFont="1"/></cellXfs></styleSheet>')


def _xlsx(linhas):
    # linhas: [(estilo, [valores])]; estilo 0 normal, 1 título, 2 subtítulo, 3 cabeçalho
    def col(i):
        return "ABCDEFGH"[i]
    xml = []
    for n, (estilo, valores) in enumerate(linhas, 1):
        cels = []
        for i, v in enumerate(valores):
            ref = f"{col(i)}{n}"
            s = f' s="{estilo}"' if estilo else ""
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                cels.append(f'<c r="{ref}"{s}><v>{v}</v></c>')
            else:
                cels.append(f'<c r="{ref}"{s} t="inlineStr"><is><t xml:space="preserve">{escape(str(v))}</t></is></c>')
        xml.append(f'<row r="{n}">{"".join(cels)}</row>')
    folha = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
             '<cols><col min="1" max="1" width="62" customWidth="1"/><col min="2" max="4" width="12" customWidth="1"/>'
             '<col min="5" max="5" width="14" customWidth="1"/></cols>'
             f'<sheetData>{"".join(xml)}</sheetData></worksheet>')
    arq = io.BytesIO()
    with zipfile.ZipFile(arq, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                   '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                   '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                   '</Types>')
        z.writestr("_rels/.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
                   '</Relationships>')
        z.writestr("xl/workbook.xml",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                   'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                   '<sheets><sheet name="Concorrentes" sheetId="1" r:id="rId1"/></sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
                   '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                   '</Relationships>')
        z.writestr("xl/styles.xml", _ESTILOS)
        z.writestr("xl/worksheets/sheet1.xml", folha)
    return arq.getvalue()


def montar(grupos, dias):
    # Devolve (bytes do .xlsx, resumo em texto para a mensagem do painel)
    rank = ranking(grupos)
    linhas = [(3, [f"O que os grupos concorrentes mais postam (últimos {dias} dias) - "
                   f"gerado em {time.strftime('%d/%m %H:%M')}"]),
              (3, ["Pontos: reação vale 3, cada grupo a mais que postou o mesmo produto vale 2, cada repetição "
                   "no grupo vale 1. (Encaminhamentos o WhatsApp não mostra para membros.)"]), (0, [])]
    resumo = []
    for nicho, _ in NICHOS:
        if not rank.get(nicho):
            continue
        linhas.append((1, [nicho, "", "", "", ""]))
        for nome, total, prods in rank[nicho]:
            linhas.append((2, [f"{nome} ({total} posts)", "", "", "", ""]))
            linhas.append((3, ["Produto", "Vezes", "Reações", "Em grupos", "Preço"]))
            for t, vezes, reac, em, preco in prods:
                linhas.append((0, [t, vezes, reac, em, preco]))
            linhas.append((0, []))
            if prods:
                resumo.append(f"{nicho} | {nome}: {prods[0][0][:50]}")
    return _xlsx(linhas), resumo
