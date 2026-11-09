# Análise do que os OUTROS grupos postaram (06/11). Uso (no PC, com o arquivo baixado do servidor):
#   python analisar_grupos.py grupos_observados.json
# Mostra: posts e reações por grupo, proporção mulher/homem, os mais reagidos e, o mais importante,
# os TIPOS de produto que eles postam e a gente não busca (nem no Casa nem no Geral), do que mais engaja
# para o que menos. É daí que sai a atualização da lista no meio da semana.
# Não lê o config.txt de verdade: usa um falso (só precisa das listas do bot, não da Shopee).
import json, os, sys, tempfile
from collections import defaultdict
PASTA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA)
import concorrentes

def carregar_bot(bot):
    falso = os.path.join(tempfile.gettempdir(), "config_falso_analise.txt")
    with open(falso, "w", encoding="utf-8") as f:
        f.write("TOKEN=x\nCANAL=@x\n")
    os.environ["BOT_CONFIG"] = falso
    os.environ["BOT_OBSIDIAN"] = ""
    src = open(os.path.join(PASTA, "postar_shopee.py"), encoding="utf-8").read().split("\npreparar_pasta_bot()")[0]
    g = {"__file__": os.path.join(PASTA, "postar_shopee.py"), "__name__": "analise"}
    argv, sys.argv = sys.argv, ["x", bot]
    try:
        exec(src, g)
    finally:
        sys.argv = argv
    return g

def main(caminho):
    dados = json.load(open(caminho, encoding="utf-8"))
    casa, geral = carregar_bot("casa"), carregar_bot("geral")
    nossos_tipos = set()
    for g in (casa, geral):
        nossos_tipos |= {g["tipo_do_produto"](p) for p in g["SIMPLES"] + g["CAROS"]}
        nossos_tipos |= {g["categoria_do_produto"](p) for p in g["SIMPLES"] + g["CAROS"]}
    posts = []
    print("=== GRUPOS ===")
    for jid, gr in dados.items():
        ps = gr.get("posts", [])
        reac = sum(len(p.get("reacoes") or {}) for p in ps)
        print(f"{gr.get('nome') or jid}: {len(ps)} posts, {reac} reações, "
              f"{sum(1 for p in ps if p.get('shopee'))} com link da Shopee")
        posts += [(p, gr.get("nome") or jid) for p in ps]
    if not posts:
        print("Nada guardado ainda.")
        return
    n = lambda p: len(p.get("reacoes") or {})
    pub = defaultdict(lambda: [0, 0])
    for p, _ in posts:
        k = concorrentes.publico(p.get("texto", "")) or "•"
        pub[k][0] += 1
        pub[k][1] += n(p)
    print("\n=== PÚBLICO (posts / reações) ===")
    for k in ("♀", "♂", "•"):
        print(f"{k}: {pub[k][0]} posts ({100 * pub[k][0] / len(posts):.0f}%), {pub[k][1]} reações, "
              f"média {pub[k][1] / max(1, pub[k][0]):.1f} por post")
    print("\n=== 30 MAIS REAGIDOS ===")
    for p, nome in sorted(posts, key=lambda x: -n(x[0]))[:30]:
        print(f"{n(p):4} {concorrentes.publico(p.get('texto', '')) or '•'} {concorrentes.titulo(p.get('texto', ''))[:70]}"
              f" {concorrentes.preco_final(p)} | {nome}")
    # O que eles postam e a gente não busca: agrupa pelo tipo do produto (mesma regra do nosso rodízio)
    faltam = defaultdict(lambda: {"posts": 0, "reacoes": 0, "exemplos": []})
    for p, _ in posts:
        t = concorrentes.titulo(p.get("texto", ""))
        if not t:
            continue
        tipo = geral["tipo_do_produto"](t)
        if tipo in nossos_tipos or geral["categoria_do_produto"](t) in nossos_tipos:
            continue
        f = faltam[tipo]
        f["posts"] += 1
        f["reacoes"] += n(p)
        if len(f["exemplos"]) < 3:
            f["exemplos"].append(t[:60])
    print(f"\n=== O QUE ELES POSTAM E A GENTE NÃO BUSCA ({len(faltam)} tipos) ===")
    for tipo, f in sorted(faltam.items(), key=lambda x: (-x[1]["reacoes"], -x[1]["posts"]))[:60]:
        print(f"{tipo}: {f['posts']} posts, {f['reacoes']} reações | ex.: {' / '.join(f['exemplos'])}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(PASTA, "whatsapp", "grupos_observados.json"))
