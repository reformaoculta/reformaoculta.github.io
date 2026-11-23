"""Gera app/dados/videos.json (catálogo do aplicativo do canal) a partir das listas do yt-dlp.

Uso:
  1) baixar as listas (no PC com AVG usar --compat-options no-certifi):
     yt-dlp --flat-playlist --dump-single-json URL_CANAL/videos > cache/app/videos.json   (idem shorts)
  2) python scripts/app_gerar_dados.py [pasta_das_listas] [saida.json]
"""
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "cache" / "app"
SAIDA = Path(sys.argv[2]) if len(sys.argv) > 2 else RAIZ / "app" / "dados" / "videos.json"
CANAL = "UCXF-4pobMGoKSlgOB3P28Zw"

# tema -> palavras (sem acento, minúsculas). Um vídeo pode ter vários temas.
TEMAS = {
    "exu-pombogira": ["exu", "pombogira", "pomba gira", "pombagira", "tranca rua", "ventania", "quiteria",
                      "mulambo", "pade", "figueira", "destranca", "guardioes", "guardias"],
    "pretos-velhos": ["pai joaquim", "preto velho", "pretos velhos", "pai benedito", "angola"],
    "orixas": ["orixa", "oxossi", "ogum", "xango", "iemanja", "yemanja", "oxum", "nana", "obaluae", "omulu",
               "ossaim", "iansa", "oxala", "ori", "odu", "iyami"],
    "ervas-banhos-velas": ["erva", "banho", "vela", "defuma", "simpatia", "macaia", "incenso", "fitoenerg",
                           "sal grosso", "oferenda", "firmeza", "ametista", "pedra", "receita"],
    "magia-bruxaria": ["magia", "bruxa", "cernunnos", "goetia", "bafome", "feitic", "amarracao", "espelho",
                       "pacto", "yule", "punhal", "pagao"],
    "ciganos-oraculos": ["cigan", "baralho", "taro", "buzios", "santa sara", "previs", "zodiaco", "folhas",
                         "aries", "touro", "gemeos", "cancer", "leao", "virgem", "libra", "escorpiao",
                         "sagitario", "capricornio", "aquario", "peixes"],
    "eres": ["ere ", "eres", "luizinho", "criancas", "cosme"],
    "mediunidade": ["medium", "mediunidade", "incorpora", "gira", "terreiro", "pai de santo", "cavalo",
                    "mentor", "guia", "obsess", "egun", "desencarn", "carma", "karma", "projecao", "sonho"],
    "misterios": ["uap", "ufolog", "esfinge", "james webb", "galaxia", "minhoca", "slender", "priorado",
                  "reset", "assustador"],
}
NOMES = {
    "exu-pombogira": "Exu e Pombogira",
    "pretos-velhos": "Pretos Velhos",
    "orixas": "Orixás",
    "ervas-banhos-velas": "Ervas, banhos e velas",
    "magia-bruxaria": "Magia e bruxaria",
    "ciganos-oraculos": "Ciganos e oráculos",
    "eres": "Erês",
    "mediunidade": "Mediunidade e terreiro",
    "misterios": "Mistérios",
    "espiritualidade": "Espiritualidade e fé",
}
FORA_DO_TEMA = ["witcher", "covid", "rio grande do sul precisa"]


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def limpar_titulo(t):
    t = re.sub(r"^t[ií]tulo:\s*", "", t, flags=re.I)
    t = re.sub(r"\s#\S+", "", t)            # tira hashtags do fim
    t = re.sub(r"\s{2,}", " ", t).strip()
    return t


PALAVRA_INTEIRA = {"ori", "ere", "eres", "nana", "odu", "leao", "touro", "libra", "cancer", "aries", "guia", "gira"}


def _casa(p, s):
    p = p.strip()
    fim = r"s?\b" if p in PALAVRA_INTEIRA else ""
    return re.search(r"\b" + re.escape(p) + fim, s) is not None


def temas_de(titulo):
    s = sem_acento(titulo)
    achados = [k for k, ps in TEMAS.items() if any(_casa(p, s) for p in ps)]
    return achados or ["espiritualidade"]


def carregar(nome):
    p = PASTA / f"{nome}.json"
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8")).get("entries") or []


def main():
    # títulos vêm da lista em português (lang=pt); as visualizações da lista em inglês (lang=en),
    # porque o yt-dlp lê "7,9 mil" como 79.
    vis = {e["id"]: e.get("view_count") for n in ("videos_en", "shorts_en", "streams_en") for e in carregar(n)}
    itens = []
    for ordem, e in enumerate(carregar("videos")):
        e["view_count"] = vis.get(e["id"], e.get("view_count"))
        if e.get("availability") == "subscriber_only" or not e.get("view_count"):
            continue  # exclusivo para membros (ou sem dados públicos)
        titulo = limpar_titulo(e["title"])
        if any(f in sem_acento(titulo) for f in FORA_DO_TEMA):
            continue
        itens.append({"id": e["id"], "t": titulo, "d": e.get("duration") or 0, "v": e.get("view_count") or 0,
                      "tipo": "video", "o": ordem, "temas": temas_de(titulo)})
    shorts = []
    for ordem, e in enumerate(carregar("shorts")):
        e["view_count"] = vis.get(e["id"], e.get("view_count"))
        titulo = limpar_titulo(e["title"])
        shorts.append({"id": e["id"], "t": titulo, "v": e.get("view_count") or 0, "tipo": "short", "o": ordem,
                       "temas": temas_de(titulo)})
    lives = []
    for ordem, e in enumerate(carregar("streams")):
        e["view_count"] = vis.get(e["id"], e.get("view_count"))
        if e.get("availability") == "subscriber_only" or e.get("live_status") in ("is_upcoming", "is_live")                 or not e.get("view_count"):
            continue
        titulo = limpar_titulo(re.sub(r"^\W*(ao vivo|live)\W*", "", e["title"], flags=re.I)) or limpar_titulo(e["title"])
        lives.append({"id": e["id"], "t": titulo, "d": e.get("duration") or 0, "v": e.get("view_count") or 0,
                      "tipo": "live", "o": ordem, "temas": temas_de(titulo)})
    # datas de publicação dos 15 mais recentes (feed público do canal)
    datas, do_feed = {}, []
    feed = PASTA / "feed.xml"
    if feed.exists():
        import xml.etree.ElementTree as ET
        ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
        for e in ET.parse(feed).getroot().findall("a:entry", ns):
            vid = e.find("yt:videoId", ns).text
            datas[vid] = e.find("a:published", ns).text[:10]
            href = e.find("a:link", ns).get("href", "")
            do_feed.append((vid, limpar_titulo(e.find("a:title", ns).text or ""), "/shorts/" in href))

    # plano B: se o YouTube bloqueou a lista completa, mantém o catálogo anterior
    # e só acrescenta os vídeos novos que aparecem no feed público.
    if not itens and SAIDA.exists():
        antigo = json.loads(SAIDA.read_text(encoding="utf-8"))
        itens, shorts = antigo["videos"], antigo["shorts"]
        lives = lives or antigo.get("lives", [])
        conhecidos = {v["id"] for v in itens + shorts}
        for vid, titulo, eh_short in reversed(do_feed):
            if vid in conhecidos or any(f in sem_acento(titulo) for f in FORA_DO_TEMA):
                continue
            novo = {"id": vid, "t": titulo, "v": 0, "tipo": "short" if eh_short else "video", "o": -1,
                    "temas": temas_de(titulo)}
            if eh_short:
                shorts.insert(0, novo)
            else:
                novo["d"] = 0
                itens.insert(0, novo)
        print("lista completa indisponível: usei o feed (plano B)")
    for v in itens + shorts:
        if v["id"] in datas:
            v["pub"] = datas[v["id"]]
    dados = {
        "canal": CANAL,
        "atualizado": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "temas": NOMES,
        "videos": itens,   # ordem do canal: o primeiro é o mais recente
        "shorts": shorts,
        "lives": lives,
    }
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(dados, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    from collections import Counter
    c = Counter(t for v in itens for t in v["temas"])
    print(f"{len(itens)} vídeos, {len(shorts)} shorts, {len(lives)} lives -> {SAIDA}")
    for k, n in c.most_common():
        print(f"  {NOMES[k]}: {n}")


if __name__ == "__main__":
    main()
