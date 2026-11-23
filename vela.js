/* "Acenda uma vela": tudo fica só no celular da pessoa (localStorage), sem enviar nada para servidor.
   A vela fica acesa por 7 dias. O PIX é sempre opcional e nunca condição para a vela. */
(() => {
  const DIAS = 7;
  const CHAVE = "velasAcesas";
  // cores mais comuns na Umbanda (podem variar de casa para casa)
  const PARA = [
    { id: "oxala", nome: "Oxalá", cor: "#f6f3ea", reza: "Que Oxalá cubra o seu caminho de paz e de luz. Êpa Babá!" },
    { id: "iemanja", nome: "Iemanjá", cor: "#9fd3f2", reza: "Que Mãe Iemanjá lave as suas dores nas águas do mar. Odoyá!" },
    { id: "oxum", nome: "Oxum", cor: "#f7d24a", reza: "Que Mamãe Oxum traga amor, doçura e prosperidade. Ora yê yê ô!" },
    { id: "ogum", nome: "Ogum", cor: "#d8312b", reza: "Que Ogum abra os seus caminhos e vença as suas demandas. Ogunhê!" },
    { id: "oxossi", nome: "Oxóssi", cor: "#2e9e4f", reza: "Que Oxóssi traga fartura, saúde e conhecimento. Okê Arô!" },
    { id: "xango", nome: "Xangô", cor: "#8a4b22", reza: "Que Xangô traga justiça e equilíbrio para a sua vida. Kaô Kabecilê!" },
    { id: "iansa", nome: "Iansã", cor: "#f2a23a", reza: "Que Iansã leve com os ventos tudo o que não te serve. Eparrey Oyá!" },
    { id: "nana", nome: "Nanã", cor: "#9b6fc6", reza: "Que Vovó Nanã traga sabedoria e calma ao seu coração. Saluba Nanã!" },
    { id: "omulu", nome: "Obaluaê / Omulu", cor: "#ece6d4", reza: "Que Obaluaê te cubra de proteção. Atotô!" },
    { id: "pretos-velhos", nome: "Pretos Velhos", cor: "#f4f0e8", reza: "Que os Pretos Velhos te abençoem com paciência e humildade. Adorei as Almas!" },
    { id: "caboclos", nome: "Caboclos", cor: "#3f8f3a", reza: "Que os Caboclos tragam força e cura das matas. Okê Caboclo!" },
    { id: "eres", nome: "Erês (Crianças)", cor: "#f6a9c8", reza: "Que os Erês tragam alegria e pureza para a sua casa. Oni Beijada!" },
    { id: "exu", nome: "Exu (Guardião)", cor: "#1c1c1c", reza: "Que Exu guarde a sua porteira e os seus caminhos. Laroyê Exu!" },
    { id: "pombogira", nome: "Pombogira", cor: "#b3122e", reza: "Que Pombogira fortaleça o seu amor-próprio e a sua autoestima. Laroyê Pombogira!" },
    { id: "ciganos", nome: "Povo Cigano", cor: "linear-gradient(#d8312b, #f7d24a, #2e9e4f, #3a6fd8)", reza: "Que o Povo Cigano ilumine os seus caminhos. Optchá!" },
    { id: "anjo", nome: "Anjo da Guarda", cor: "#ffffff", reza: "Que o seu Anjo da Guarda te proteja de dia e de noite." },
    { id: "almas", nome: "Pelas almas", cor: "#f4f0e8", reza: "Que as almas encontrem luz, paz e caminho. Adorei as Almas!" },
  ];
  const $ = (s) => document.querySelector(s);
  const form = $("#formVela"), acesa = $("#velaAcesa"), minhas = $("#minhasVelas"), sel = $("#velaPara");
  if (!form) return;
  sel.innerHTML = '<option value="" disabled selected>Escolha…</option>' +
    PARA.map((p) => `<option value="${p.id}">${p.nome}</option>`).join("");

  const ler = () => { try { return JSON.parse(localStorage.getItem(CHAVE)) || []; } catch { return []; } };
  const gravar = (l) => { try { localStorage.setItem(CHAVE, JSON.stringify(l)); } catch {} };
  const validas = () => { const agora = Date.now(); const l = ler().filter((v) => v.fim > agora); gravar(l); return l; };
  const dataBR = (ms) => new Date(ms).toLocaleDateString("pt-BR", { weekday: "long", day: "numeric", month: "long" });
  const achar = (id) => PARA.find((x) => x.id === id) || PARA[0];

  function mostrar(v) {
    const p = achar(v.para);
    $("#velaCorpo").style.background = p.cor;
    $("#velaTitulo").textContent = (v.nome ? v.nome + ", sua" : "Sua") + " vela para " + p.nome + " está acesa";
    $("#velaPedidoTexto").textContent = "“" + v.pedido + "”";
    $("#velaPrazo").textContent = "Fica acesa até " + dataBR(v.fim) + ".";
    $("#velaReza").textContent = p.reza;
    form.hidden = true; acesa.hidden = false;
    listar();
  }
  function listar() {
    const l = validas();
    if (l.length < 2) { minhas.hidden = true; return; }
    minhas.hidden = false;
    minhas.innerHTML = '<p class="titulo-minhas">Suas velas acesas</p>';
    l.forEach((v) => {
      const p = achar(v.para);
      const b = document.createElement("button"); b.type = "button"; b.className = "mini-vela";
      const i = document.createElement("i"); i.style.background = p.cor; b.append(i, p.nome);
      b.addEventListener("click", () => mostrar(v)); minhas.append(b);
    });
  }
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const pedido = $("#velaPedido").value.trim(); if (!sel.value || !pedido) return;
    const v = { para: sel.value, nome: $("#velaNome").value.trim().split(/\s+/)[0] || "", pedido,
      inicio: Date.now(), fim: Date.now() + DIAS * 864e5 };
    gravar([v, ...validas()].slice(0, 12));
    form.reset(); mostrar(v);
    acesa.scrollIntoView({ behavior: "smooth", block: "center" });
  });
  $("#novaVela").addEventListener("click", () => { acesa.hidden = true; form.hidden = false; listar(); });
  const ultima = validas()[0];
  if (ultima) mostrar(ultima); else listar();
})();
