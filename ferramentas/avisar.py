"""Manda o aviso de vídeo novo (OneSignal) para quem ligou os avisos no app.

Uso: python ferramentas/avisar.py ids_antes.txt dados/videos.json
Compara a lista de antes com a nova; para cada vídeo novo publicado nos últimos 2 dias, envia um aviso.
Precisa das variáveis ONESIGNAL_APP_ID e ONESIGNAL_API_KEY (segredo do GitHub). Sem elas, não faz nada.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, timedelta

APP_ID = os.environ.get("ONESIGNAL_APP_ID", "").strip()
CHAVE = os.environ.get("ONESIGNAL_API_KEY", "").strip()
SITE = "https://reformaoculta.github.io/"


def enviar(titulo, texto, url, imagem):
    corpo = {
        "app_id": APP_ID,
        "target_channel": "push",
        "included_segments": ["Total Subscriptions"],
        "headings": {"en": titulo, "pt": titulo},
        "contents": {"en": texto, "pt": texto},
        "url": url,
        "chrome_web_image": imagem,
        "chrome_web_icon": SITE + "icones/icone-192.png",
    }
    req = urllib.request.Request("https://api.onesignal.com/notifications?c=push",
                                 data=json.dumps(corpo).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "Authorization": f"Key {CHAVE}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("aviso enviado:", r.status, r.read()[:300].decode(errors="replace"))
    except urllib.error.HTTPError as e:
        print("OneSignal recusou:", e.code, e.read()[:300].decode(errors="replace"))
        if e.code in (401, 403):
            sys.exit("chave ONESIGNAL_API_KEY inválida")


def main():
    if "--teste" in sys.argv:
        if not (APP_ID and CHAVE):
            sys.exit("falta ONESIGNAL_API_KEY")
        v = json.load(open(sys.argv[2], encoding="utf-8"))["videos"][0]
        enviar("Teste de aviso", v["t"], f"https://www.youtube.com/watch?v={v['id']}",
               f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg")
        return
    antes = set(open(sys.argv[1], encoding="utf-8").read().split())
    d = json.load(open(sys.argv[2], encoding="utf-8"))
    if not antes:
        print("sem lista anterior: não avisa nada")
        return
    limite = (date.today() - timedelta(days=2)).isoformat()
    novos = [v for v in d["videos"] + d["shorts"] if v["id"] not in antes and v.get("pub", "") >= limite]
    if not novos:
        print("nenhum vídeo novo")
        return
    if not (APP_ID and CHAVE):
        print("avisos ainda não configurados (falta ONESIGNAL_APP_ID / ONESIGNAL_API_KEY)")
        return
    for v in novos[:2]:  # no máximo 2 avisos por vez
        short = v["tipo"] == "short"
        url = f"https://www.youtube.com/shorts/{v['id']}" if short else f"https://www.youtube.com/watch?v={v['id']}"
        enviar("Short novo no canal!" if short else "Vídeo novo no canal!", v["t"], url,
               f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg")


if __name__ == "__main__":
    main()
