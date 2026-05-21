import csv
import io
import json
import re
from datetime import datetime

import streamlit as st

st.set_page_config(
    page_title="Figurinhas Copa 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

SECTIONS = {
    "FWC": "🏆 Abertura / Especiais",
    "ALG": "🇩🇿 Argélia",
    "ARG": "🇦🇷 Argentina",
    "AUS": "🇦🇺 Austrália",
    "AUT": "🇦🇹 Áustria",
    "BEL": "🇧🇪 Bélgica",
    "BIH": "🇧🇦 Bósnia e Herzegovina",
    "BRA": "🇧🇷 Brasil",
    "CAN": "🇨🇦 Canadá",
    "CIV": "🇨🇮 Costa do Marfim",
    "COD": "🇨🇩 RD Congo",
    "COL": "🇨🇴 Colômbia",
    "CPV": "🇨🇻 Cabo Verde",
    "CRO": "🇭🇷 Croácia",
    "CUW": "🇨🇼 Curaçao",
    "CZE": "🇨🇿 Tchéquia",
    "ECU": "🇪🇨 Equador",
    "EGY": "🇪🇬 Egito",
    "ENG": "🏴 Inglaterra",
    "ESP": "🇪🇸 Espanha",
    "FRA": "🇫🇷 França",
    "GER": "🇩🇪 Alemanha",
    "GHA": "🇬🇭 Gana",
    "HAI": "🇭🇹 Haiti",
    "IRN": "🇮🇷 Irã",
    "IRQ": "🇮🇶 Iraque",
    "JOR": "🇯🇴 Jordânia",
    "JPN": "🇯🇵 Japão",
    "KOR": "🇰🇷 Coreia do Sul",
    "KSA": "🇸🇦 Arábia Saudita",
    "MAR": "🇲🇦 Marrocos",
    "MEX": "🇲🇽 México",
    "NED": "🇳🇱 Países Baixos",
    "NOR": "🇳🇴 Noruega",
    "NZL": "🇳🇿 Nova Zelândia",
    "PAN": "🇵🇦 Panamá",
    "PAR": "🇵🇾 Paraguai",
    "POR": "🇵🇹 Portugal",
    "QAT": "🇶🇦 Catar",
    "RSA": "🇿🇦 África do Sul",
    "SCO": "🏴 Escócia",
    "SEN": "🇸🇳 Senegal",
    "SUI": "🇨🇭 Suíça",
    "SWE": "🇸🇪 Suécia",
    "TUN": "🇹🇳 Tunísia",
    "TUR": "🇹🇷 Turquia",
    "URU": "🇺🇾 Uruguai",
    "USA": "🇺🇸 Estados Unidos",
    "UZB": "🇺🇿 Uzbequistão",
}

INITIAL_OWNED_TEXT = """
FWC-1 FWC-2 FWC-5 FWC-6 FWC-8 FWC-9 FWC-10 FWC-11 FWC-13 FWC-14 FWC-15 FWC-16 FWC-17 FWC-19 FWC-20 MEX-1 MEX-3 MEX-15 MEX-17 MEX-18 MEX-19 RSA-2 RSA-4 RSA-5 RSA-6 RSA-10 RSA-14 RSA-15 RSA-16 RSA-19 KOR-3 KOR-5 KOR-6 KOR-8 KOR-9 KOR-12 KOR-14 KOR-17 KOR-18 CZE-5 CZE-6 CZE-9 CZE-10 CZE-18 CZE-19 CZE-20 CAN-1 CAN-5 CAN-8 CAN-10 CAN-11 CAN-13 BIH-4 BIH-7 BIH-8 BIH-3 BIH-11 BIH-16 BIH-20 QAT-3 QAT-4 QAT-7 QAT-9 QAT-14 QAT-17 QAT-18 SUI-1 SUI-2 SUI-6 SUI-8 SUI-9 SUI-10 SUI-11 SUI-12 SUI-14 SUI-16 SUI-18 SUI-19 SUI-20 BRA-2 BRA-3 BRA-4 BRA-5 BRA-6 BRA-9 BRA-10 BRA-11 BRA-13 BRA-14 BRA-15 BRA-16 BRA-18 MAR-3 MAR-8 MAR-9 MAR-14 MAR-18 HAI-1 HAI-5 HAI-9 HAI-10 HAI-14 HAI-15 HAI-16 HAI-18 HAI-19 HAI-20 SCO-2 SCO-5 SCO-8 SCO-13 SCO-18 SCO-20 USA-1 USA-2 USA-3 USA-4 USA-13 USA-15 USA-16 USA-20 PAR-2 PAR-3 PAR-4 PAR-6 PAR-7 PAR-5 PAR-9 PAR-10 PAR-11 PAR-13 PAR-14 PAR-15 PAR-16 PAR-18 AUS-1 AUS-2 AUS-4 AUS-11 AUS-12 AUS-16 AUS-17 AUS-18 TUR-1 TUR-5 TUR-7 TUR-9 TUR-12 TUR-14 TUR-18 TUR-20 GER-4 GER-7 GER-8 GER-9 GER-11 GER-12 GER-14 GER-15 GER-17 GER-18 GER-19 GER-20 CUW-1 CUW-2 CUW-4 CUW-6 CUW-8 CUW-10 CUW-12 CUW-14 CUW-15 CUW-16 CUW-17 CUW-19 CIV-1 CIV-2 CIV-7 CIV-9 CIV-10 CIV-11 CIV-13 CIV-15 CIV-16 ECU-1 ECU-2 ECU-3 ECU-6 ECU-7 ECU-9 ECU-10 ECU-11 ECU-14 ECU-17 ECU-18 ECU-19 NED-8 NED-12 NED-13 NED-19 NED-20 JPN-3 JPN-7 JPN-8 JPN-9 JPN-10 JPN-15 JPN-18 JPN-20 SWE-1 SWE-2 SWE-4 SWE-5 SWE-6 SWE-8 SWE-9 SWE-11 SWE-12 SWE-14 SWE-20 TUN-3 TUN-4 TUN-7 TUN-10 TUN-15 TUN-19 BEL-2 BEL-3 BEL-5 BEL-6 BEL-7 BEL-9 BEL-11 BEL-16 BEL-20 EGY-7 EGY-8 EGY-10 EGY-12 EGY-17 EGY-18 EGY-20 IRN-1 IRN-10 IRN-17 IRN-18 IRN-19 IRN-20 NZL-2 NZL-5 NZL-6 NZL-8 NZL-9 NZL-10 NZL-17 NZL-18 ESP-1 ESP-2 ESP-3 ESP-4 ESP-5 ESP-6 ESP-7 ESP-8 ESP-9 ESP-10 ESP-11 ESP-12 ESP-13 ESP-14 ESP-15 ESP-17 ESP-18 ESP-20 CPV-8 CPV-9 CPV-11 CPV-12 CPV-20 KSA-1 KSA-2 KSA-3 KSA-7 KSA-8 KSA-9 KSA-10 KSA-12 KSA-13 KSA-14 KSA-15 KSA-16 KSA-18 KSA-19 KSA-20 URU-1 URU-4 URU-7 URU-10 URU-11 URU-15 URU-16 URU-20 FRA-1 FRA-2 FRA-4 FRA-5 FRA-6 FRA-7 FRA-8 FRA-9 FRA-10 FRA-11 FRA-12 FRA-14 FRA-15 FRA-16 FRA-17 FRA-18 FRA-19 FRA-20 SEN-5 SEN-9 SEN-13 SEN-14 SEN-17 SEN-20 IRQ-1 IRQ-3 IRQ-4 IRQ-5 IRQ-7 IRQ-9 IRQ-10 IRQ-13 IRQ-14 IRQ-16 IRQ-19 IRQ-20 NOR-1 NOR-5 NOR-13 NOR-15 NOR-20 ARG-1 ARG-2 ARG-3 ARG-7 ARG-10 ARG-11 ARG-13 ARG-14 ARG-15 ARG-18 ARG-19 ARG-20 ALG-3 ALG-7 ALG-9 ALG-10 ALG-11 ALG-13 ALG-15 ALG-16 ALG-18 ALG-19 ALG-20 AUT-2 AUT-3 AUT-7 AUT-12 AUT-14 AUT-18 JOR-2 JOR-5 JOR-12 JOR-18 JOR-20 POR-1 POR-6 POR-7 POR-9 POR-10 POR-14 POR-15 POR-18 POR-19 COD-1 COD-3 COD-11 COD-14 COD-16 COD-20 UZB-1 UZB-7 UZB-8 UZB-18 UZB-19 COL-4 COL-15 COL-17 COL-19 ENG-1 ENG-2 ENG-3 ENG-4 ENG-5 ENG-6 ENG-7 ENG-8 ENG-10 ENG-11 ENG-13 ENG-14 ENG-15 ENG-16 ENG-17 ENG-18 ENG-19 ENG-20 CRO-1 CRO-3 CRO-7 CRO-15 CRO-16 CRO-17 CRO-19 CRO-20 GHA-1 GHA-2 GHA-15 GHA-16 PAN-5 PAN-9 PAN-11 PAN-12 PAN-13 PAN-14 PAN-15 PAN-16 PAN-17 PAN-18 PAN-19 PAN-20
"""

TOTAL_ALBUM = 980


def all_codes() -> list[str]:
    return [f"{sec}-{n}" for sec in SECTIONS for n in range(1, 21)]


def initial_qty() -> dict[str, int]:
    valid = set(all_codes())
    return {code: 1 for code in INITIAL_OWNED_TEXT.split() if code in valid}


def get_qty() -> dict[str, int]:
    return st.session_state.setdefault("qty", initial_qty())


def set_qty(code: str, value: int) -> None:
    qty = get_qty()
    value = int(value)
    if value <= 0:
        qty.pop(code, None)
    else:
        qty[code] = min(value, 99)


def stats():
    qty = get_qty()
    codes = all_codes()
    owned = sum(1 for c in codes if int(qty.get(c, 0)) > 0)
    duplicates = sum(max(0, int(qty.get(c, 0)) - 1) for c in codes)
    missing = TOTAL_ALBUM - owned
    complete_sections = sum(
        all(int(qty.get(f"{sec}-{n}", 0)) > 0 for n in range(1, 21))
        for sec in SECTIONS
    )
    pct = owned / TOTAL_ALBUM if TOTAL_ALBUM else 0
    return owned, missing, duplicates, complete_sections, pct


def missing_text() -> str:
    qty = get_qty()
    owned, missing, duplicates, complete_sections, pct = stats()
    lines = [
        f"Álbum Copa do Mundo FIFA 2026 — faltam {missing} de {TOTAL_ALBUM} figurinhas ({pct:.1%} completo).",
        "",
    ]
    for sec, name in SECTIONS.items():
        missing_nums = [str(n) for n in range(1, 21) if int(qty.get(f"{sec}-{n}", 0)) == 0]
        if missing_nums:
            lines.append(f"{sec} — {name}: " + ", ".join(missing_nums))
    if missing == 0:
        lines.append("Álbum completo! 🏆")
    return "\n".join(lines)


def duplicates_text() -> str:
    qty = get_qty()
    lines = ["Repetidas para troca:"]
    found = False
    for sec, name in SECTIONS.items():
        reps = []
        for n in range(1, 21):
            code = f"{sec}-{n}"
            q = int(qty.get(code, 0))
            if q > 1:
                reps.append(f"{code} (+{q - 1})")
        if reps:
            found = True
            lines.append(f"{sec} — {name}: " + ", ".join(reps))
    if not found:
        lines.append("Nenhuma repetida registrada.")
    return "\n".join(lines)


def export_json() -> str:
    return json.dumps(
        {
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "app": "figurinhas_copa_2026_streamlit",
            "version": 1,
            "state": {
                "qty": {k: int(v) for k, v in get_qty().items() if int(v) > 0},
                "includeBonus": False,
                "collapsed": {},
                "lastCompleted": {},
            },
        },
        ensure_ascii=False,
        indent=2,
    )


def export_csv() -> bytes:
    out = io.StringIO()
    writer = csv.writer(out, delimiter=";")
    writer.writerow(["codigo", "secao", "nome_secao", "numero", "quantidade", "status"])
    qty = get_qty()
    for sec, name in SECTIONS.items():
        for n in range(1, 21):
            code = f"{sec}-{n}"
            q = int(qty.get(code, 0))
            status = "faltando" if q == 0 else "tenho" if q == 1 else "repetida"
            writer.writerow([code, sec, name, n, q, status])
    return out.getvalue().encode("utf-8-sig")


def parse_batch(text: str) -> list[str]:
    text = text.upper()
    text = re.sub(r"([A-Z]{2,4})\s*[- ]?\s*(\d{1,2})", r"\1-\2", text)
    return re.findall(r"[A-Z]{2,4}-\d{1,2}", text)


st.markdown(
    """
    <style>
    .block-container { padding-top: 1.1rem; max-width: 100%; }
    .hero {
        padding: 24px;
        border-radius: 24px;
        background: radial-gradient(circle at 20% 0%, rgba(39,217,128,.22), transparent 30%),
                    radial-gradient(circle at 90% 15%, rgba(77,169,255,.24), transparent 34%),
                    linear-gradient(135deg, #06101f, #122844);
        border: 1px solid rgba(255,255,255,.16);
        box-shadow: 0 16px 36px rgba(0,0,0,.25);
        margin-bottom: 16px;
    }
    .hero h1 { margin: 0 0 8px 0; font-size: 42px; line-height: 1.05; }
    .hero p { color: #c5d6e8; font-size: 16px; }
    .pill { display:inline-block; padding:7px 11px; border-radius:999px; margin:8px 6px 0 0; border:1px solid rgba(255,255,255,.18); background:rgba(255,255,255,.07); }
    </style>
    <div class="hero">
        <h1>⚽ Controle de Figurinhas — Copa do Mundo FIFA 2026</h1>
        <p>App independente no Streamlit, iniciado com o backup das figurinhas já marcadas.</p>
        <span class="pill">980 figurinhas-base</span>
        <span class="pill">443 carregadas inicialmente</span>
        <span class="pill">Exporta JSON/CSV</span>
        <span class="pill">Lista para WhatsApp</span>
    </div>
    """,
    unsafe_allow_html=True,
)

owned, missing, duplicates, complete_sections, pct = stats()
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Tenho únicas", owned)
c2.metric("Faltam", missing)
c3.metric("Repetidas", duplicates)
c4.metric("Seções completas", complete_sections)
c5.metric("Progresso", f"{pct:.1%}")
st.progress(pct)

with st.sidebar:
    st.title("⚽ Figurinhas")
    section = st.selectbox(
        "Seleção / seção",
        list(SECTIONS.keys()),
        format_func=lambda sec: f"{sec} — {SECTIONS[sec]}",
    )

    st.divider()
    batch = st.text_area("Adicionar pacotinho/lote", placeholder="Ex.: BRA 14, ARG 10, FWC 3")
    if st.button("Adicionar lote", type="primary", use_container_width=True):
        valid_codes = set(all_codes())
        added, invalid = 0, []
        for code in parse_batch(batch):
            if code in valid_codes:
                set_qty(code, int(get_qty().get(code, 0)) + 1)
                added += 1
            else:
                invalid.append(code)
        if added:
            st.success(f"{added} figurinha(s) adicionada(s).")
        if invalid:
            st.warning("Não reconhecidas: " + ", ".join(invalid))
        st.rerun()

    st.divider()
    uploaded = st.file_uploader("Importar backup JSON", type=["json"])
    if uploaded is not None:
        try:
            data = json.loads(uploaded.read().decode("utf-8"))
            imported = data.get("state", data).get("qty", {})
            valid_codes = set(all_codes())
            st.session_state.qty = {
                k: int(v) for k, v in imported.items() if k in valid_codes and int(v) > 0
            }
            st.success("Backup importado.")
            st.rerun()
        except Exception as exc:
            st.error(f"Não consegui importar o JSON: {exc}")

    if st.button("Restaurar JSON inicial", use_container_width=True):
        st.session_state.qty = initial_qty()
        st.rerun()

    if st.button("Zerar controle", use_container_width=True):
        st.session_state.qty = {}
        st.rerun()

st.subheader(f"{section} — {SECTIONS[section]}")
cols = st.columns(5)
for idx, n in enumerate(range(1, 21)):
    code = f"{section}-{n}"
    with cols[idx % 5]:
        current = int(get_qty().get(code, 0))
        new_value = st.number_input(code, min_value=0, max_value=99, value=current, step=1, key=f"qty_{code}")
        set_qty(code, int(new_value))

tab_missing, tab_duplicates, tab_exports = st.tabs(["📌 Faltantes", "🔁 Repetidas", "⬇️ Exportações"])

with tab_missing:
    st.text_area("Lista pronta para copiar/WhatsApp", missing_text(), height=460)

with tab_duplicates:
    st.text_area("Lista de repetidas para troca", duplicates_text(), height=420)

with tab_exports:
    st.download_button(
        "Baixar backup JSON",
        data=export_json(),
        file_name="backup_controle_figurinhas_copa_2026.json",
        mime="application/json",
        use_container_width=True,
    )
    st.download_button(
        "Baixar CSV",
        data=export_csv(),
        file_name="controle_figurinhas_copa_2026.csv",
        mime="text/csv",
        use_container_width=True,
    )
