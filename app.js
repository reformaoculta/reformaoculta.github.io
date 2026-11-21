/* Aplicativo do canal Rádio Reforma Interna.
   Tudo é calculado no próprio celular a partir de dados/videos.json:
   - vídeo do dia e sugestões mudam a cada dia (mesmo resultado para todo mundo no mesmo dia);
   - vídeo publicado há até 3 dias aparece em destaque como "Novo". */
(() => {
  const POR_PAGINA = 24;
  const $ = (s) => document.querySelector(s);
  const thumb = (id, q = "mqdefault") => `https://i.ytimg.com/vi/${id}/${q}.jpg`;
  const link = (id) => `https://www.youtube.com/watch?v=${id}`;
  const esc = (t) => t.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const semAcento = (t) => t.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();

  // dia de hoje no horário de Brasília
  const hojeBR = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Sao_Paulo" }).format(new Date());
  const diaN = Math.floor(Date.parse(hojeBR + "T00:00:00Z") / 864e5);

  // gerador pseudoaleatório com semente (o mesmo dia sempre dá o mesmo resultado)
  function sorteio(semente) {
    let s = semente >>> 0;
    return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  const embaralhar = (arr, rnd) => { const a = arr.slice(); for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  const duracao = (s) => { if (!s) return ""; const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60);
    return h ? `${h}h${String(m).padStart(2, "0")}` : `${m} min`; };
  const views = (v) => v >= 1e6 ? (v / 1e6).toFixed(1).replace(".", ",") + " mi" :
    v >= 1e3 ? Math.round(v / 1e3) + " mil" : String(v);

  function cartao(v, temas) {
    const tema = temas[v.temas[0]] || "";
    return `<a class="cartao" href="${link(v.id)}" target="_blank" rel="noopener">
      <img loading="lazy" src="${thumb(v.id)}" alt="">
      <div class="corpo"><span class="tema">${esc(tema)}</span><h3>${esc(v.t)}</h3>
      <p class="info">${duracao(v.d)}${v.v ? " • " + views(v.v) + " visualizações" : ""}</p></div></a>`;
  }

  function player(v) {
    const el = document.createElement("div");
    el.className = "player";
    el.innerHTML = `<img src="${thumb(v.id, "hqdefault")}" alt="${esc(v.t)}"><span class="play" aria-hidden="true"></span>`;
    el.addEventListener("click", () => {
      el.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${v.id}?autoplay=1&rel=0"
        title="${esc(v.t)}" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>`;
    }, { once: true });
    return el;
  }

  // títulos com promessa de saúde não entram no destaque (regras do Google e da Play Store)
  const saude = /c[aâ]ncer|\bcura\b|doen[cç]a|covid/i;

  function montar(d) {
    const temas = d.temas, todos = d.videos;
    const videos = todos;
    const destacaveis = todos.filter((v) => !saude.test(v.t));
    $("#totalVideos").textContent = videos.length;
    $("#dataHoje").textContent = new Date().toLocaleDateString("pt-BR",
      { weekday: "long", day: "numeric", month: "long", timeZone: "America/Sao_Paulo" });

    // 1) vídeo novo (até 3 dias) ganha destaque
    const recentes = [...videos, ...d.shorts].filter((v) => v.pub)
      .sort((a, b) => b.pub.localeCompare(a.pub));
    const novo = recentes.find((v) => (Date.parse(hojeBR) - Date.parse(v.pub)) / 864e5 <= 3);
    if (novo) {
      const n = $("#novo");
      n.innerHTML = `<span class="selo">NOVO</span><div><b>Saiu vídeo novo no canal!</b>${esc(novo.t)}</div>`;
      n.outerHTML = `<a id="novo" class="aviso-novo" href="${link(novo.id)}" target="_blank" rel="noopener">${n.innerHTML}</a>`;
    }

    // 2) vídeo do dia: o vídeo longo mais recente se saiu há até 2 dias; senão um sorteado entre os mais vistos
    const rnd = sorteio(diaN * 7919);
    const bons = destacaveis.filter((v) => v.v >= 3000 && v.d >= 300);
    const ultimoLongo = videos.find((v) => v.pub);
    const fresco = ultimoLongo && (Date.parse(hojeBR) - Date.parse(ultimoLongo.pub)) / 864e5 <= 2;
    const base = bons.length ? bons : videos;
    const doDia = fresco ? ultimoLongo : base[Math.floor(rnd() * base.length)];
    const caixa = $("#videoDia");
    caixa.append(player(doDia));
    caixa.insertAdjacentHTML("beforeend", `<h2 class="titulo-dia">${esc(doDia.t)}</h2>
      <p class="info">${esc(temas[doDia.temas[0]])} • ${duracao(doDia.d)}${doDia.v ? " • " + views(doDia.v) + " visualizações" : ""}</p>`);

    // 3) sugestões: 4 temas que mudam a cada dia, 1 vídeo de cada
    const chaves = Object.keys(temas).filter((k) => videos.some((v) => v.temas.includes(k)));
    const usados = new Set([doDia.id]);
    const sug = [];
    for (const k of embaralhar(chaves, sorteio(diaN * 31 + 7)).slice(0, 4)) {
      const opcoes = embaralhar(destacaveis.filter((v) => v.temas.includes(k) && !usados.has(v.id) && v.d >= 120),
        sorteio(diaN * 131 + k.length));
      if (opcoes[0]) { usados.add(opcoes[0].id); sug.push({ ...opcoes[0], temas: [k, ...opcoes[0].temas] }); }
    }
    $("#sugestoes").innerHTML = sug.map((v) => cartao(v, temas)).join("");

    // 4) explorar por tema + busca
    let temaAtual = "todos", pagina = 1;
    const chips = [["todos", "Todos"], ...chaves.map((k) => [k, temas[k]])];
    $("#temas").innerHTML = chips.map(([k, n]) =>
      `<button role="tab" data-k="${k}" aria-selected="${k === temaAtual}">${esc(n)}</button>`).join("");
    const lista = () => {
      const q = semAcento($("#busca").value.trim());
      const r = videos.filter((v) => (q || temaAtual === "todos" || v.temas.includes(temaAtual)) &&
        (!q || semAcento(v.t).includes(q)));
      $("#lista").innerHTML = r.slice(0, pagina * POR_PAGINA).map((v) => cartao(v, temas)).join("") ||
        `<p class="sub">Nenhum vídeo encontrado.</p>`;
      $("#maisVideos").hidden = r.length <= pagina * POR_PAGINA;
    };
    $("#temas").addEventListener("click", (e) => {
      const b = e.target.closest("button"); if (!b) return;
      temaAtual = b.dataset.k; pagina = 1;
      $("#temas").querySelectorAll("button").forEach((x) => x.setAttribute("aria-selected", x === b));
      lista();
    });
    $("#busca").addEventListener("input", () => { pagina = 1; lista(); });
    $("#maisVideos").addEventListener("click", () => { pagina++; lista(); });
    lista();

    // 5) shorts: os 12 mais recentes
    $("#shorts").innerHTML = d.shorts.slice(0, 12).map((v) =>
      `<a class="short" href="https://www.youtube.com/shorts/${v.id}" target="_blank" rel="noopener">
        <img loading="lazy" src="https://i.ytimg.com/vi/${v.id}/oar2.jpg" onerror="this.src='${thumb(v.id, "hqdefault")}'" alt="">
        <span>${esc(v.t)}</span></a>`).join("");
  }

  const buscar = (n = 3) => fetch("dados/videos.json").then((r) => r.json())
    .catch((e) => n > 1 ? new Promise((ok) => setTimeout(ok, 800)).then(() => buscar(n - 1)) : Promise.reject(e));
  buscar().then(montar)
    .catch((erro) => { console.error(erro); $("#videoDia").innerHTML = `<p class="sub">Não foi possível carregar os vídeos. Verifique a internet.</p>`; });

  // PIX copia e cola
  $("#copiarPix").addEventListener("click", async (e) => {
    const codigo = e.currentTarget.dataset.pix;
    try { await navigator.clipboard.writeText(codigo); }
    catch { const t = document.createElement("textarea"); t.value = codigo; document.body.append(t); t.select();
      document.execCommand("copy"); t.remove(); }
    $("#pixCopiado").hidden = false;
  });

  // instalação do app
  let pedido = null;
  const barra = $("#instalar");
  const fechado = () => { try { return localStorage.getItem("instalarFechado") === "1"; } catch { return false; } };
  const ehIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
  const instalado = matchMedia("(display-mode: standalone)").matches || navigator.standalone;
  window.addEventListener("beforeinstallprompt", (e) => { e.preventDefault(); pedido = e; if (!fechado()) barra.hidden = false; });
  if (ehIOS && !instalado && !fechado()) {
    $("#textoInstalar").textContent = "Para instalar: toque em Compartilhar e depois em \"Adicionar à Tela de Início\".";
    $("#botaoInstalar").hidden = true; barra.hidden = false;
  }
  $("#botaoInstalar").addEventListener("click", async () => { if (!pedido) return; pedido.prompt(); await pedido.userChoice; barra.hidden = true; });
  $("#fecharInstalar").addEventListener("click", () => { barra.hidden = true; try { localStorage.setItem("instalarFechado", "1"); } catch {} });

  if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {});
})();
