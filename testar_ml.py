# Teste do Mercado Livre: entra na Central de Afiliados com a sessão (ml_cookies.txt, ao lado do config.txt),
# busca e mostra 5 produtos. Não mostra cookie nem código de segurança. A lógica fica em mercadolivre.py.
# Uso:  python testar_ml.py                      busca "perfume masculino"
#       python testar_ml.py "perfume feminino"   outra busca
#       python testar_ml.py "perfume" --link     também gera o link de afiliado do 1º produto
import sys

from mercadolivre import SessaoCaiu, SessaoML

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    termo = args[0] if args else "perfume masculino"
    try:
        ml = SessaoML()
    except SessaoCaiu as e:
        sys.exit(f"O Mercado Livre não aceitou a sessão ({e}). Exporte os cookies de novo para ml_cookies.txt.")
    print("Sessão do Mercado Livre OK (Central de Afiliados abriu).")
    produtos = ml.buscar(termo)
    print(f"Busca '{termo}': {len(produtos)} produtos. Os 5 primeiros:")
    for p in produtos[:5]:
        de = f"de R$ {p['preco_antes']} " if p["preco_antes"] else ""
        print(f"  - {p['nome'][:70]} | {de}por R$ {p['preco']} {p['desconto']} | nota {p['nota']} | "
              f"{p['vendidos']}+ vendidos | comissão {p['comissao']}%")
    if "--link" in sys.argv and produtos:
        print("Link de afiliado do 1º:", ml.gerar_link(produtos[0]) or "a geração falhou")
