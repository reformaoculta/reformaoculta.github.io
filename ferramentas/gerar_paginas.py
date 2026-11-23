"""Gera as páginas por tema do app (Pretos Velhos, Exu, Pombogira, Erês, Orixás, Ervas, Mediunidade, Ciganos, Magia) e o sitemap.xml.

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
    {
        "slug": "orixas",
        "nome": "Orixás",
        "titulo": "Orixás na Umbanda: Oxalá, Ogum, Oxóssi, Xangô, Iemanjá, Oxum e mais",
        "descricao": "Conheça os Orixás na Umbanda: Oxalá, Ogum, Oxóssi, Xangô, Iansã, Iemanjá, Oxum, Nanã, Obaluaê e Ossaim. Ensinamentos, oferendas e fundamentos em vídeos gratuitos da Rádio Reforma Interna.",
        "busca": r"orix|oxossi|ogum|xango|iemanja|yemanja|oxum|\bnana\b|obaluae|omulu|ossaim|ians[aã]|oxala|\bori\b|iyami",
        "saudacao": "Saravá os Orixás! Axé!",
        "texto": [
            "Os <strong>Orixás</strong> são as forças sagradas da natureza que regem a Umbanda. Cada um representa um aspecto da criação, como as matas, os mares, as cachoeiras, os raios e os caminhos, e também qualidades que existem dentro de cada um de nós.",
            "Na Umbanda, os Orixás orientam as linhas de trabalho dos guias. <strong>Oxalá</strong> traz a fé e a paz, <strong>Ogum</strong> a coragem e a abertura de caminhos, <strong>Oxóssi</strong> o conhecimento e a fartura, <strong>Xangô</strong> a justiça, <strong>Iansã</strong> o movimento, <strong>Iemanjá</strong> o acolhimento de mãe, <strong>Oxum</strong> o amor e a prosperidade, e <strong>Nanã</strong> e <strong>Obaluaê</strong> a sabedoria e a cura.",
            "No canal, você encontra vídeos sobre os fundamentos dos Orixás, as ervas de cada um e a relação deles com o nosso dia a dia.",
        ],
        "perguntas": [
            ("O que são os Orixás na Umbanda?", "São forças divinas ligadas à natureza, que regem as linhas de trabalho espiritual e representam qualidades como fé, coragem, justiça e amor."),
            ("Quais são os principais Orixás da Umbanda?", "Os mais cultuados são Oxalá, Ogum, Oxóssi, Xangô, Iansã, Iemanjá, Oxum, Nanã e Obaluaê/Omulu. Cada casa pode ter suas particularidades."),
            ("Como saber qual é o meu Orixá?", "Em geral, isso é confirmado dentro de um terreiro, com o dirigente espiritual, por meio do jogo ou da observação da mediunidade ao longo do tempo."),
        ],
    },
    {
        "slug": "ervas-banhos-velas",
        "nome": "Ervas, banhos e velas",
        "titulo": "Ervas, banhos, benzimentos e velas na Umbanda",
        "descricao": "Ervas na Umbanda: banhos de descarrego e de energização, benzimentos, defumação, velas e simpatias, com os ensinamentos de Pai Joaquim e outros guias. Vídeos gratuitos da Rádio Reforma Interna.",
        "busca": r"\bervas?\b|\bbanhos?\b|benz|defuma|simpatia|\bvelas?\b|incenso|sal grosso|oferenda|firmeza|macaia|fitoenerg",
        "saudacao": "Ewê ó! Salve as folhas!",
        "texto": [
            "As <strong>ervas</strong> são a base de muitos trabalhos na Umbanda. Com elas se fazem os banhos, as defumações e os benzimentos, que limpam energias pesadas, fortalecem a proteção e trazem equilíbrio para o corpo e o espírito.",
            "Os <strong>banhos de descarrego</strong> ajudam a tirar o que pesa. Os de <strong>energização</strong> renovam as forças. As <strong>velas</strong> e as <strong>firmezas</strong> ajudam a firmar o pensamento e a ligação com os guias. Tudo isso funciona com fé, intenção e respeito à natureza.",
            "Esse é o tema mais procurado do canal. Os ensinamentos de <strong>Pai Joaquim de Angola</strong> sobre ervas, simpatias e benzimentos já passaram de um milhão de visualizações.",
        ],
        "perguntas": [
            ("Para que serve o banho de ervas na Umbanda?", "Para limpar energias negativas (descarrego), renovar as forças (energização) e se preparar para os trabalhos espirituais."),
            ("Posso fazer banho de ervas em casa?", "Sim, muitos banhos simples podem ser feitos em casa, com fé e as ervas certas. Na dúvida, peça orientação ao seu terreiro."),
            ("Banho de ervas substitui o médico?", "Não. Os banhos e benzimentos são um apoio espiritual e não substituem o tratamento médico. Continue sempre o acompanhamento com profissionais de saúde."),
        ],
    },
    {
        "slug": "mediunidade",
        "nome": "Mediunidade",
        "titulo": "Mediunidade na Umbanda: desenvolvimento, incorporação e terreiro",
        "descricao": "Mediunidade na Umbanda: como funciona a incorporação, o desenvolvimento mediúnico, a gira e a vida no terreiro, além de obsessão, carma e proteção espiritual. Vídeos gratuitos da Rádio Reforma Interna.",
        "busca": r"medium|mediuni|incorpora|terreiro|(?<!pomb[ao] )\bgiras?\b|obsess|desencarn|\bcarma|\bkarma|\bmentor|pai de santo|mae de santo|desenvolvimento",
        "saudacao": "Saravá Umbanda!",
        "texto": [
            "A <strong>mediunidade</strong> é a capacidade de sentir e se comunicar com o plano espiritual. Na Umbanda, ela é desenvolvida com disciplina, estudo e caridade, dentro de um terreiro e com a orientação de um dirigente.",
            "A <strong>incorporação</strong> é a forma mais conhecida, mas existem muitas outras, como a intuição, a vidência e a audição. O desenvolvimento leva tempo e pede equilíbrio, humildade e reforma interna, que é o caminho que dá nome ao canal.",
            "Nos vídeos, os guias falam sobre a vida dos médiuns, a gira, a obsessão, o carma e como cuidar da própria energia.",
        ],
        "perguntas": [
            ("Como saber se tenho mediunidade?", "Sinais como intuições fortes, sensibilidade a ambientes e sonhos marcantes podem indicar mediunidade. O ideal é procurar um terreiro sério para orientação."),
            ("O que é incorporação na Umbanda?", "É quando o médium empresta seu corpo e sua voz para que um guia espiritual se manifeste, sempre de forma consciente ou semiconsciente e com preparo."),
            ("Médium precisa frequentar terreiro?", "Para desenvolver a mediunidade com segurança, sim: o terreiro oferece orientação, proteção e disciplina."),
        ],
    },
    {
        "slug": "ciganos",
        "nome": "Povo Cigano",
        "titulo": "Povo Cigano na Umbanda: ciganos, Santa Sara e oráculos",
        "descricao": "O Povo Cigano na Umbanda: quem são os ciganos e ciganas, Santa Sara Kali, baralho cigano, tarô, búzios e previsões. Vídeos gratuitos da Rádio Reforma Interna.",
        "busca": r"cigan|baralho|\btaro|buzios|santa sara|oracul",
        "saudacao": "Optchá! Salve o Povo Cigano!",
        "texto": [
            "O <strong>Povo Cigano</strong> é uma linha de trabalho que chegou à Umbanda trazendo alegria, liberdade e muita sabedoria sobre a sorte, os caminhos e o amor. Os ciganos e as ciganas trabalham com cores, perfumes, moedas, cristais e com a leitura dos oráculos.",
            "<strong>Santa Sara Kali</strong> é a padroeira desse povo, e muitos devotos a celebram em maio. Os ciganos ensinam a viver com leveza, a valorizar o presente e a não ter medo de mudar de rumo.",
            "No canal, você encontra vídeos sobre o Povo Cigano, o baralho cigano, o tarô, os búzios e as previsões.",
        ],
        "perguntas": [
            ("Quem é o Povo Cigano na Umbanda?", "É uma linha de espíritos ciganos que trabalha com alegria, prosperidade, amor e a leitura dos caminhos por meio dos oráculos."),
            ("Quem é Santa Sara Kali?", "É a padroeira do povo cigano. Muitos devotos a celebram em 24 de maio."),
            ("Qual a saudação ao Povo Cigano?", "Uma das saudações mais usadas é \"Optchá!\"."),
        ],
    },
    {
        "slug": "magia-bruxaria",
        "nome": "Magia e bruxaria",
        "titulo": "Magia e bruxaria: o que é, tradições e ensinamentos",
        "descricao": "Magia e bruxaria com responsabilidade: o que é magia, as tradições pagãs, feitiços, rituais e a visão espiritual da Umbanda sobre o assunto. Vídeos gratuitos da Rádio Reforma Interna.",
        "busca": r"magia|bruxa|feitic|goetia|cernunnos|pagao|pagan|wicca|\byule\b|bafome|\britua(l|is)\b|tecnomancia",
        "saudacao": "",
        "texto": [
            "<strong>Magia</strong> é a arte de usar a energia, a intenção e os elementos da natureza para provocar mudanças. Ela existe em muitas tradições, das bruxas europeias às religiões de matriz africana, e sempre esteve ligada ao conhecimento das plantas, dos astros e dos ciclos da vida.",
            "A <strong>bruxaria</strong> foi perseguida durante séculos, e por isso ainda é cercada de medo e preconceito. Na visão da Rádio Reforma Interna, toda magia traz responsabilidade: o que se planta, se colhe.",
            "No canal, você encontra vídeos sobre as tradições pagãs, Cernunnos, a Goétia, feitiços, a Roda do Ano e uma aula de bruxaria com Maria Quitéria.",
        ],
        "perguntas": [
            ("O que é magia?", "É o uso consciente da energia, da intenção e dos elementos da natureza para provocar mudanças, presente em várias tradições espirituais."),
            ("Bruxaria é do mal?", "Não necessariamente. A bruxaria é um conjunto de práticas e tradições antigas. Como toda magia, o resultado depende da intenção de quem pratica."),
            ("Umbanda é bruxaria?", "Não. A Umbanda é uma religião brasileira, com seus próprios fundamentos. Ela usa elementos mágicos, como ervas e velas, mas tem doutrina e culto próprios."),
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


def pagina(tema, videos, todos, lives=()):
    url = SITE + tema["slug"] + "/"
    busca = re.compile(tema["busca"])
    lista = [v for v in videos if busca.search(sem_acento(v["t"]))]
    top = sorted((v for v in lista if not SAUDE.search(v["t"])), key=lambda v: -v["v"])[:18]
    ids_top = {v["id"] for v in top}
    recentes = [v for v in sorted(lista, key=lambda v: v["o"]) if v["id"] not in ids_top][:6]
    total = len(lista)
    lives_tema = sorted((v for v in lives if busca.search(sem_acento(v["t"])) and not SAUDE.search(v["t"])),
                        key=lambda v: -v["v"])[:6]
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
    sec_lives = (f'<section class="bloco"><h2 class="titulo-bloco">Lives sobre {e(tema["nome"])}</h2>'
                 f'<p class="sub">Nas lives é o próprio apresentador do canal quem conversa com vocês sobre o tema.</p><div class="grade">'
                 f'{"".join(cartao(v) for v in lives_tema)}</div></section>') if lives_tema else ""
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
  {f'<p class="saudacao">{e(tema["saudacao"])}</p>' if tema["saudacao"] else ""}
  <section class="texto-tema">{texto}</section>

  <section class="bloco">
    <h2 class="titulo-bloco">Os mais assistidos sobre {e(tema["nome"])}</h2>
    <p class="sub">{total} vídeos sobre {e(tema["nome"])} no canal. Toque para assistir aqui mesmo.</p>
    <div class="grade">{"".join(cartao(v) for v in top)}</div>
  </section>
  {sec_recentes}
  {sec_lives}

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
        (pasta / "index.html").write_text(pagina(t, d["videos"], TEMAS, d.get("lives", [])), encoding="utf-8")
        print("página:", t["slug"])
    urls = [SITE] + [SITE + t["slug"] + "/" for t in TEMAS]
    (RAIZ / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc><changefreq>daily</changefreq></url>\n" for u in urls)
        + "</urlset>\n", encoding="utf-8")


if __name__ == "__main__":
    main()
