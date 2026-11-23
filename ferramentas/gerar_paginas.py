"""Gera as páginas por tema do app (Pretos Velhos, Exu, Pombogira, Erês) e o sitemap.xml.

Uso: python ferramentas/gerar_paginas.py   (lê dados/videos.json; escreve <tema>/index.html e sitemap.xml)
Roda sozinho no GitHub depois de atualizar a lista de vídeos, então as páginas acompanham o canal.
Para criar um tema novo, acrescente um item em TEMAS.
"""
import html
import json
import re
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITE = "https://reformaoculta.github.io/"
CANAL = "https://www.youtube.com/channel/UCXF-4pobMGoKSlgOB3P28Zw"
SAUDE = re.compile(r"c[aâ]ncer|\bcura\b|doen[cç]a|covid", re.I)

TEMAS = [
    {
        "slug": "pretos-velhos",
        "nome": "Pretos Velhos",
        "titulo": "Pretos Velhos na Umbanda: ensinamentos, ervas e benzimentos",
        "descricao": "Quem são os Pretos Velhos na Umbanda, como trabalham e os ensinamentos de Pai Joaquim de Angola sobre ervas, benzimentos, simpatias e fé. Vídeos gratuitos da Rádio Reforma Interna.",
        "busca": r"pret[oa]s? velh|pai joaquim|pai benedito|vov[oó] |\bvo (maria|cambinda|catarina)",
        "saudacao": "Adorei as Almas!",
        "texto": [
            "Os <strong>Pretos Velhos</strong> são uma das linhas mais amadas da Umbanda. São espíritos que se apresentam como anciãos e anciãs, muitas vezes ligados à memória dos africanos escravizados no Brasil, e que trazem para o terreiro a sabedoria de quem viveu muito e aprendeu com a dor sem perder a fé.",
            "Na gira, costumam trabalhar sentados no banquinho, com cachimbo, terço e muita paciência. Aconselham, benzem, ensinam o uso das ervas e ajudam cada pessoa a enxergar o próprio caminho com humildade, perdão e caridade.",
            "Aqui na Rádio Reforma Interna, <strong>Pai Joaquim de Angola</strong> é a voz mais conhecida do canal: os ensinamentos dele sobre ervas, benzimentos e simpatias já passaram de um milhão de visualizações.",
        ],
        "perguntas": [
            ("Quem são os Pretos Velhos?", "São espíritos de luz que se manifestam na Umbanda com a aparência de pessoas idosas, trazendo sabedoria, humildade e acolhimento. Trabalham com conselhos, benzimentos e ervas."),
            ("Qual a saudação aos Pretos Velhos?", "A saudação mais conhecida é \"Adorei as Almas!\". Em muitas casas, o dia 13 de maio é dedicado a eles."),
            ("O que os Pretos Velhos ensinam?", "Paciência, perdão, fé e caridade. Também ensinam o uso das ervas, os banhos e os benzimentos para equilibrar o corpo e o espírito."),
        ],
    },
    {
        "slug": "exu",
        "nome": "Exu",
        "titulo": "Exu na Umbanda: quem é, o que faz e seus ensinamentos",
        "descricao": "Exu na Umbanda sem preconceito: guardião, mensageiro e protetor dos caminhos. Ensinamentos de Exu Caveira, Exu Ventania, Tranca Rua e mais, em vídeos gratuitos da Rádio Reforma Interna.",
        "busca": r"\bexus?\b|tranca ?rua|ze pelintra|destranca|guardi[oa]",
        "saudacao": "Laroyê, Exu! Exu é Mojubá!",
        "texto": [
            "<strong>Exu</strong> é o guardião, o mensageiro e o executor da lei na Umbanda. Ele protege a casa, a gira e cada pessoa, abre e fecha caminhos e ajuda a colocar ordem onde existe desequilíbrio.",
            "Por muito tempo Exu foi confundido com o diabo, e esse preconceito ainda existe. Na Umbanda, Exu trabalha para o bem e para a evolução: cobra responsabilidade, mostra as consequências das nossas escolhas e nos tira da zona de conforto.",
            "No canal, você encontra os ensinamentos de várias falanges, como <strong>Exu Caveira</strong>, <strong>Exu Ventania</strong> e <strong>Tranca Rua das Almas</strong>, sempre com respeito e fundamento.",
        ],
        "perguntas": [
            ("Exu é o diabo?", "Não. Na Umbanda, Exu é um guardião que trabalha pela lei e pela evolução espiritual. A associação com o diabo veio do preconceito contra as religiões de matriz africana."),
            ("Qual a saudação a Exu?", "\"Laroyê, Exu!\" e \"Exu é Mojubá!\" são as saudações mais usadas."),
            ("O que Exu faz na Umbanda?", "Protege o terreiro e as pessoas, abre e fecha caminhos, leva e traz mensagens e ajuda a desmanchar demandas e energias negativas."),
        ],
    },
    {
        "slug": "pombogira",
        "nome": "Pombogira",
        "titulo": "Pombogira na Umbanda: quem é, como trabalha e seus ensinamentos",
        "descricao": "Pombogira na Umbanda com respeito e fundamento: amor-próprio, força feminina e cura emocional. Ensinamentos de Maria Quitéria, Maria Mulambo, Sete Rosas e mais em vídeos gratuitos.",
        "busca": r"pomb[ao] ?gira|maria (padilha|mulambo|quiteria|navalha)|sete (rosas|saias)|rosa caveira",
        "saudacao": "Laroyê, Pombogira!",
        "texto": [
            "<strong>Pombogira</strong> é a força feminina da linha de Exu. Ela trabalha com as emoções, os desejos, o amor-próprio e a coragem de ser quem se é, ajudando a curar feridas afetivas e a romper relações e padrões que fazem mal.",
            "Assim como Exu, Pombogira sofre muito preconceito e é reduzida a estereótipos. Na Umbanda, ela é uma guardiã sábia e firme, que fala de frente, sem rodeios, e ensina a não aceitar a opressão.",
            "No canal, falam com você <strong>Maria Quitéria</strong>, <strong>Maria Mulambo</strong>, <strong>Pombogira Sete Rosas</strong> e outras, com ensinamentos sobre a vida, a magia das flores e o autoconhecimento.",
        ],
        "perguntas": [
            ("Quem é Pombogira?", "É a guardiã feminina da linha da esquerda na Umbanda. Trabalha com as emoções, o amor-próprio e a proteção, sempre dentro da lei espiritual."),
            ("Qual a saudação a Pombogira?", "A saudação mais usada é \"Laroyê, Pombogira!\"."),
            ("Pombogira faz amarração?", "Na Umbanda séria, não. Pombogira respeita o livre-arbítrio e ajuda a pessoa a se fortalecer, e não a prender a vontade de outra pessoa."),
        ],
    },
    {
        "slug": "eres",
        "nome": "Erês",
        "titulo": "Erês na Umbanda: as crianças, a alegria e a pureza",
        "descricao": "Quem são os Erês na Umbanda, a linha das crianças, Cosme e Damião, e os ensinamentos do Erê Luizinho e do Erê Joãozinho em vídeos gratuitos da Rádio Reforma Interna.",
        "busca": r"\beres?\b|erezinh|ibej|cosme|crianc",
        "saudacao": "Oni Beijada!",
        "texto": [
            "Os <strong>Erês</strong> são os espíritos que se apresentam como crianças na Umbanda. Trazem alegria, leveza e pureza para a gira, e com brincadeiras e doces conseguem desmanchar energias pesadas que muitas vezes os adultos nem percebem.",
            "Essa linha é ligada a <strong>Cosme e Damião</strong> e aos Ibejis, e costuma ser celebrada em setembro. Por trás da brincadeira, os Erês trabalham sério: limpam, curam e lembram a gente de olhar a vida com mais simplicidade.",
            "No canal, o <strong>Erê Luizinho</strong> e o <strong>Erê Joãozinho</strong> falam sobre alegria, consciência e o trabalho das crianças na espiritualidade.",
        ],
        "perguntas": [
            ("Quem são os Erês?", "São espíritos que se manifestam como crianças na Umbanda, trazendo alegria, pureza e limpeza espiritual."),
            ("Qual a saudação aos Erês?", "A saudação mais conhecida é \"Oni Beijada!\"."),
            ("Quando se comemora os Erês?", "Em muitas casas, em setembro, perto do dia de Cosme e Damião (27 de setembro), com festa, doces e muita alegria."),
        ],
    },
]


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def e(t):
    return html.escape(t, quote=True)


def views(v):
    if v >= 1_000_000:
        return f"{v / 1e6:.1f}".replace(".", ",") + " mi"
    if v >= 1000:
        return f"{round(v / 1000)} mil"
    return str(v)


def duracao(s):
    if not s:
        return ""
    h, m = s // 3600, (s % 3600) // 60
    return f"{h}h{m:02d}" if h else f"{m} min"


def cartao(v):
    info = " • ".join(x for x in (duracao(v.get("d", 0)), f"{views(v['v'])} visualizações" if v["v"] else "") if x)
    return (f'<div class="cartao video" data-id="{v["id"]}" tabindex="0" role="button" aria-label="Assistir: {e(v["t"])}">'
            f'<div class="capa"><img loading="lazy" src="https://i.ytimg.com/vi/{v["id"]}/mqdefault.jpg" alt="">'
            f'<span class="play" aria-hidden="true"></span></div>'
            f'<div class="corpo"><h3>{e(v["t"])}</h3><p class="info">{info}</p>'
            f'<a class="no-youtube" href="https://www.youtube.com/watch?v={v["id"]}" target="_blank" rel="noopener">Ver no YouTube</a>'
            f'</div></div>')


def pagina(tema, videos, todos):
    url = SITE + tema["slug"] + "/"
    busca = re.compile(tema["busca"])
    lista = [v for v in videos if busca.search(sem_acento(v["t"]))]
    top = sorted((v for v in lista if not SAUDE.search(v["t"])), key=lambda v: -v["v"])[:18]
    ids_top = {v["id"] for v in top}
    recentes = [v for v in sorted(lista, key=lambda v: v["o"]) if v["id"] not in ids_top][:6]
    total = len(lista)
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}} for p, r in tema["perguntas"]]}
    colecao = {"@context": "https://schema.org", "@type": "CollectionPage", "name": tema["titulo"], "url": url,
               "inLanguage": "pt-BR", "description": tema["descricao"],
               "isPartOf": {"@type": "WebSite", "name": "Rádio Reforma Interna", "url": SITE},
               "mainEntity": {"@type": "ItemList", "itemListElement": [
                   {"@type": "ListItem", "position": i + 1, "url": f"https://www.youtube.com/watch?v={v['id']}", "name": v["t"]}
                   for i, v in enumerate(top)]}}
    outros = "".join(f'<a href="../{t["slug"]}/">{e(t["nome"])}</a>' for t in todos if t is not tema)
    perguntas = "".join(f"<details><summary>{e(p)}</summary><p>{e(r)}</p></details>" for p, r in tema["perguntas"])
    texto = "".join(f"<p>{p}</p>" for p in tema["texto"])
    sec_recentes = (f'<section class="bloco"><h2 class="titulo-bloco">Mais recentes</h2><div class="grade">'
                    f'{"".join(cartao(v) for v in recentes)}</div></section>') if recentes else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(tema["titulo"])} | Rádio Reforma Interna</title>
<meta name="description" content="{e(tema["descricao"])}">
<meta name="theme-color" content="#FE6704">
<link rel="canonical" href="{url}">
<link rel="manifest" href="../manifest.webmanifest">
<link rel="icon" href="../icones/icone-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="../icones/icone-180.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(tema["titulo"])}">
<meta property="og:description" content="{e(tema["descricao"])}">
<meta property="og:image" content="{SITE}icones/icone-512.png">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="pt_BR">
<link rel="stylesheet" href="../estilo.css">
<script type="application/ld+json">{json.dumps(colecao, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>
</head>
<body>
<header class="topo">
  <a href="../" class="voltar" aria-label="Voltar ao app"><img src="../icones/icone-192.png" alt="" class="logo" width="44" height="44"></a>
  <div class="marca"><strong>Rádio Reforma Interna</strong><span>Umbanda • espiritualidade • magia</span></div>
  <a class="botao-inscrever" href="{CANAL}?sub_confirmation=1" target="_blank" rel="noopener">Inscrever-se</a>
</header>
<main class="tema-pagina">
  <nav class="trilha"><a href="../">Início</a> › {e(tema["nome"])}</nav>
  <h1 class="titulo-tema">{e(tema["titulo"])}</h1>
  <p class="saudacao">{e(tema["saudacao"])}</p>
  <section class="texto-tema">{texto}</section>

  <section class="bloco">
    <h2 class="titulo-bloco">Os mais assistidos sobre {e(tema["nome"])}</h2>
    <p class="sub">{total} vídeos sobre {e(tema["nome"])} no canal. Toque para assistir aqui mesmo.</p>
    <div class="grade">{"".join(cartao(v) for v in top)}</div>
  </section>
  {sec_recentes}

  <section class="bloco perguntas">
    <h2 class="titulo-bloco">Perguntas frequentes</h2>
    {perguntas}
    <p class="sub">Cada casa de Umbanda tem seus fundamentos. Aqui está a visão da Rádio Reforma Interna.</p>
  </section>

  <section class="bloco">
    <h2 class="titulo-bloco">Outros temas</h2>
    <div class="outros-temas">{outros}</div>
  </section>

  <section class="bloco chamada">
    <p>Quer um vídeo novo por dia e aviso quando sair vídeo no canal?</p>
    <a class="botao" href="../">Abrir o app da Rádio Reforma Interna</a>
  </section>
</main>
<footer class="rodape">Rádio Reforma Interna • conteúdo do canal no YouTube</footer>
<script>
document.querySelectorAll(".video").forEach(function (c) {{
  function tocar(ev) {{
    if (ev.target.closest("a")) return;
    var capa = c.querySelector(".capa"); if (!capa || capa.dataset.tocando) return;
    capa.dataset.tocando = 1;
    capa.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + c.dataset.id +
      '?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen title="Vídeo"></iframe>';
  }}
  c.addEventListener("click", tocar);
  c.addEventListener("keydown", function (ev) {{ if (ev.key === "Enter") tocar(ev); }});
}});
</script>
</body>
</html>
"""


def main():
    d = json.loads((RAIZ / "dados" / "videos.json").read_text(encoding="utf-8"))
    for t in TEMAS:
        pasta = RAIZ / t["slug"]
        pasta.mkdir(exist_ok=True)
        (pasta / "index.html").write_text(pagina(t, d["videos"], TEMAS), encoding="utf-8")
        print("página:", t["slug"])
    urls = [SITE] + [SITE + t["slug"] + "/" for t in TEMAS]
    (RAIZ / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc><changefreq>daily</changefreq></url>\n" for u in urls)
        + "</urlset>\n", encoding="utf-8")


if __name__ == "__main__":
    main()
