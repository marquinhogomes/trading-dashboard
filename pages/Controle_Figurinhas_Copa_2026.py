import csv
import io
import json
import re
from datetime import datetime

import streamlit as st

st.set_page_config(page_title='Controle de Figurinhas | Copa 2026', page_icon='⚽', layout='wide')

SECTIONS = {
    'FWC':'🏆 Abertura / Especiais','ALG':'🇩🇿 Argélia','ARG':'🇦🇷 Argentina','AUS':'🇦🇺 Austrália','AUT':'🇦🇹 Áustria',
    'BEL':'🇧🇪 Bélgica','BIH':'🇧🇦 Bósnia e Herzegovina','BRA':'🇧🇷 Brasil','CAN':'🇨🇦 Canadá','CIV':'🇨🇮 Costa do Marfim',
    'COD':'🇨🇩 RD Congo','COL':'🇨🇴 Colômbia','CPV':'🇨🇻 Cabo Verde','CRO':'🇭🇷 Croácia','CUW':'🇨🇼 Curaçao',
    'CZE':'🇨🇿 Tchéquia','ECU':'🇪🇨 Equador','EGY':'🇪🇬 Egito','ENG':'🏴 Inglaterra','ESP':'🇪🇸 Espanha',
    'FRA':'🇫🇷 França','GER':'🇩🇪 Alemanha','GHA':'🇬🇭 Gana','HAI':'🇭🇹 Haiti','IRN':'🇮🇷 Irã','IRQ':'🇮🇶 Iraque',
    'JOR':'🇯🇴 Jordânia','JPN':'🇯🇵 Japão','KOR':'🇰🇷 Coreia do Sul','KSA':'🇸🇦 Arábia Saudita','MAR':'🇲🇦 Marrocos',
    'MEX':'🇲🇽 México','NED':'🇳🇱 Países Baixos','NOR':'🇳🇴 Noruega','NZL':'🇳🇿 Nova Zelândia','PAN':'🇵🇦 Panamá',
    'PAR':'🇵🇾 Paraguai','POR':'🇵🇹 Portugal','QAT':'🇶🇦 Catar','RSA':'🇿🇦 África do Sul','SCO':'🏴 Escócia',
    'SEN':'🇸🇳 Senegal','SUI':'🇨🇭 Suíça','SWE':'🇸🇪 Suécia','TUN':'🇹🇳 Tunísia','TUR':'🇹🇷 Turquia',
    'URU':'🇺🇾 Uruguai','USA':'🇺🇸 Estados Unidos','UZB':'🇺🇿 Uzbequistão'
}

INITIAL_OWNED = '''
FWC-1 FWC-2 FWC-5 FWC-6 FWC-8 FWC-9 FWC-10 FWC-11 FWC-13 FWC-14 FWC-15 FWC-16 FWC-17 FWC-19 FWC-20 MEX-1 MEX-3 MEX-15 MEX-17 MEX-18 MEX-19 RSA-2 RSA-4 RSA-5 RSA-6 RSA-10 RSA-14 RSA-15 RSA-16 RSA-19 KOR-3 KOR-5 KOR-6 KOR-8 KOR-9 KOR-12 KOR-14 KOR-17 KOR-18 CZE-5 CZE-6 CZE-9 CZE-10 CZE-18 CZE-19 CZE-20 CAN-1 CAN-5 CAN-8 CAN-10 CAN-11 CAN-13 BIH-4 BIH-7 BIH-8 BIH-3 BIH-11 BIH-16 BIH-20 QAT-3 QAT-4 QAT-7 QAT-9 QAT-14 QAT-17 QAT-18 SUI-1 SUI-2 SUI-6 SUI-8 SUI-9 SUI-10 SUI-11 SUI-12 SUI-14 SUI-16 SUI-18 SUI-19 SUI-20 BRA-2 BRA-3 BRA-4 BRA-5 BRA-6 BRA-9 BRA-10 BRA-11 BRA-13 BRA-14 BRA-15 BRA-16 BRA-18 MAR-3 MAR-8 MAR-9 MAR-14 MAR-18 HAI-1 HAI-5 HAI-9 HAI-10 HAI-14 HAI-15 HAI-16 HAI-18 HAI-19 HAI-20 SCO-2 SCO-5 SCO-8 SCO-13 SCO-18 SCO-20 USA-1 USA-2 USA-3 USA-4 USA-13 USA-15 USA-16 USA-20 PAR-2 PAR-3 PAR-4 PAR-6 PAR-7 PAR-5 PAR-9 PAR-10 PAR-11 PAR-13 PAR-14 PAR-15 PAR-16 PAR-18 AUS-1 AUS-2 AUS-4 AUS-11 AUS-12 AUS-16 AUS-17 AUS-18 TUR-1 TUR-5 TUR-7 TUR-9 TUR-12 TUR-14 TUR-18 TUR-20 GER-4 GER-7 GER-8 GER-9 GER-11 GER-12 GER-14 GER-15 GER-17 GER-18 GER-19 GER-20 CUW-1 CUW-2 CUW-4 CUW-6 CUW-8 CUW-10 CUW-12 CUW-14 CUW-15 CUW-16 CUW-17 CUW-19 CIV-1 CIV-2 CIV-7 CIV-9 CIV-10 CIV-11 CIV-13 CIV-15 CIV-16 ECU-1 ECU-2 ECU-3 ECU-6 ECU-7 ECU-9 ECU-10 ECU-11 ECU-14 ECU-17 ECU-18 ECU-19 NED-8 NED-12 NED-13 NED-19 NED-20 JPN-3 JPN-7 JPN-8 JPN-9 JPN-10 JPN-15 JPN-18 JPN-20 SWE-1 SWE-2 SWE-4 SWE-5 SWE-6 SWE-8 SWE-9 SWE-11 SWE-12 SWE-14 SWE-20 TUN-3 TUN-4 TUN-7 TUN-10 TUN-15 TUN-19 BEL-2 BEL-3 BEL-5 BEL-6 BEL-7 BEL-9 BEL-11 BEL-16 BEL-20 EGY-7 EGY-8 EGY-10 EGY-12 EGY-17 EGY-18 EGY-20 IRN-1 IRN-10 IRN-17 IRN-18 IRN-19 IRN-20 NZL-2 NZL-5 NZL-6 NZL-8 NZL-9 NZL-10 NZL-17 NZL-18 ESP-1 ESP-2 ESP-3 ESP-4 ESP-5 ESP-6 ESP-7 ESP-8 ESP-9 ESP-10 ESP-11 ESP-12 ESP-13 ESP-14 ESP-15 ESP-17 ESP-18 ESP-20 CPV-8 CPV-9 CPV-11 CPV-12 CPV-20 KSA-1 KSA-2 KSA-3 KSA-7 KSA-8 KSA-9 KSA-10 KSA-12 KSA-13 KSA-14 KSA-15 KSA-16 KSA-18 KSA-19 KSA-20 URU-1 URU-4 URU-7 URU-10 URU-11 URU-15 URU-16 URU-20 FRA-1 FRA-2 FRA-4 FRA-5 FRA-6 FRA-7 FRA-8 FRA-9 FRA-10 FRA-11 FRA-12 FRA-14 FRA-15 FRA-16 FRA-17 FRA-18 FRA-19 FRA-20 SEN-5 SEN-9 SEN-13 SEN-14 SEN-17 SEN-20 IRQ-1 IRQ-3 IRQ-4 IRQ-5 IRQ-7 IRQ-9 IRQ-10 IRQ-13 IRQ-14 IRQ-16 IRQ-19 IRQ-20 NOR-1 NOR-5 NOR-13 NOR-15 NOR-20 ARG-1 ARG-2 ARG-3 ARG-7 ARG-10 ARG-11 ARG-13 ARG-14 ARG-15 ARG-18 ARG-19 ARG-20 ALG-3 ALG-7 ALG-9 ALG-10 ALG-11 ALG-13 ALG-15 ALG-16 ALG-18 ALG-19 ALG-20 AUT-2 AUT-3 AUT-7 AUT-12 AUT-14 AUT-18 JOR-2 JOR-5 JOR-12 JOR-18 JOR-20 POR-1 POR-6 POR-7 POR-9 POR-10 POR-14 POR-15 POR-18 POR-19 COD-1 COD-3 COD-11 COD-14 COD-16 COD-20 UZB-1 UZB-7 UZB-8 UZB-18 UZB-19 COL-4 COL-15 COL-17 COL-19 ENG-1 ENG-2 ENG-3 ENG-4 ENG-5 ENG-6 ENG-7 ENG-8 ENG-10 ENG-11 ENG-13 ENG-14 ENG-15 ENG-16 ENG-17 ENG-18 ENG-19 ENG-20 CRO-1 CRO-3 CRO-7 CRO-15 CRO-16 CRO-17 CRO-19 CRO-20 GHA-1 GHA-2 GHA-15 GHA-16 PAN-5 PAN-9 PAN-11 PAN-12 PAN-13 PAN-14 PAN-15 PAN-16 PAN-17 PAN-18 PAN-19 PAN-20
'''

TOTAL = 980


def inicial():
    return {c: 1 for c in INITIAL_OWNED.split()}


def all_codes():
    return [f'{sec}-{n}' for sec in SECTIONS for n in range(1, 21)]


def safe_qty():
    return {k: int(v) for k, v in st.session_state.qty.items() if int(v) > 0}


def resumo():
    qty = st.session_state.qty
    tenho = sum(1 for c in all_codes() if int(qty.get(c, 0)) > 0)
    reps = sum(max(0, int(qty.get(c, 0)) - 1) for c in all_codes())
    faltam = TOTAL - tenho
    completas = sum(all(int(qty.get(f'{sec}-{n}', 0)) > 0 for n in range(1, 21)) for sec in SECTIONS)
    return tenho, faltam, reps, completas, tenho / TOTAL


def faltantes_texto():
    qty = st.session_state.qty
    tenho, faltam, reps, completas, pct = resumo()
    linhas = [f'Álbum Copa do Mundo FIFA 2026 — faltam {faltam} de {TOTAL} figurinhas ({pct:.1%} completo).', '']
    for sec, nome in SECTIONS.items():
        nums = [str(n) for n in range(1, 21) if int(qty.get(f'{sec}-{n}', 0)) == 0]
        if nums:
            linhas.append(f'{sec} — {nome}: ' + ', '.join(nums))
    return '\n'.join(linhas)


def repetidas_texto():
    qty = st.session_state.qty
    linhas = ['Repetidas:']
    achou = False
    for sec, nome in SECTIONS.items():
        reps = [f'{sec}-{n} (+{int(qty.get(f"{sec}-{n}", 0)) - 1})' for n in range(1, 21) if int(qty.get(f'{sec}-{n}', 0)) > 1]
        if reps:
            achou = True
            linhas.append(f'{sec} — {nome}: ' + ', '.join(reps))
    if not achou:
        linhas.append('Nenhuma repetida registrada.')
    return '\n'.join(linhas)


def export_json():
    return json.dumps({
        'exported_at': datetime.utcnow().isoformat() + 'Z',
        'app': 'controle_figurinhas_copa_2026_streamlit',
        'version': 1,
        'state': {'qty': safe_qty(), 'includeBonus': False, 'collapsed': {}, 'lastCompleted': {}}
    }, ensure_ascii=False, indent=2)


def export_csv():
    out = io.StringIO()
    w = csv.writer(out, delimiter=';')
    w.writerow(['codigo', 'secao', 'numero', 'quantidade', 'status'])
    for sec in SECTIONS:
        for n in range(1, 21):
            c = f'{sec}-{n}'
            q = int(st.session_state.qty.get(c, 0))
            w.writerow([c, sec, n, q, 'faltando' if q == 0 else 'tenho' if q == 1 else 'repetida'])
    return out.getvalue()


def parse_lote(txt):
    txt = txt.upper()
    txt = re.sub(r'([A-Z]{2,4})\s*[- ]?\s*(\d{1,2})', r'\1-\2', txt)
    return re.findall(r'[A-Z]{2,4}-\d{1,2}', txt)


if 'qty' not in st.session_state:
    st.session_state.qty = inicial()

st.markdown('''
<style>
.block-container {padding-top: 1rem; max-width: 100%;}
.hero {padding: 22px; border-radius: 22px; background: linear-gradient(135deg,#06101f,#122844); border: 1px solid rgba(255,255,255,.14); margin-bottom: 16px;}
.hero h1 {margin: 0; font-size: 42px;}
.pill {display:inline-block; padding:7px 10px; border-radius:999px; margin:8px 6px 0 0; border:1px solid rgba(255,255,255,.18); background:rgba(255,255,255,.07);}
</style>
<div class='hero'>
<h1>⚽ Controle de Figurinhas — Copa do Mundo FIFA 2026</h1>
<p>Controle integrado diretamente ao Streamlit, já iniciado com o JSON enviado: 443 figurinhas únicas carregadas.</p>
<span class='pill'>980 figurinhas-base</span><span class='pill'>48 seleções × 20</span><span class='pill'>Exporta JSON/CSV</span><span class='pill'>Lista para WhatsApp</span>
</div>
''', unsafe_allow_html=True)

tenho, faltam, reps, completas, pct = resumo()
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric('Tenho únicas', tenho)
c2.metric('Faltam', faltam)
c3.metric('Repetidas', reps)
c4.metric('Seções completas', completas)
c5.metric('Progresso', f'{pct:.1%}')
st.progress(pct)

with st.sidebar:
    st.title('⚽ Figurinhas')
    secao = st.selectbox('Seleção / seção', list(SECTIONS.keys()), format_func=lambda x: f'{x} — {SECTIONS[x]}')
    st.divider()
    lote = st.text_area('Adicionar pacotinho/lote', placeholder='Ex.: BRA 14, ARG 10, FWC 3')
    if st.button('Adicionar lote', type='primary', use_container_width=True):
        adicionadas, invalidas = 0, []
        for c in parse_lote(lote):
            if c in all_codes():
                st.session_state.qty[c] = int(st.session_state.qty.get(c, 0)) + 1
                adicionadas += 1
            else:
                invalidas.append(c)
        st.success(f'{adicionadas} figurinha(s) adicionada(s).')
        if invalidas:
            st.warning('Não reconhecidas: ' + ', '.join(invalidas))
        st.rerun()
    st.divider()
    upload = st.file_uploader('Importar backup JSON', type=['json'])
    if upload is not None:
        data = json.loads(upload.read().decode('utf-8'))
        imported = data.get('state', data).get('qty', {})
        st.session_state.qty = {k: int(v) for k, v in imported.items() if k in all_codes() and int(v) > 0}
        st.success('Backup importado.')
        st.rerun()
    if st.button('Restaurar JSON inicial', use_container_width=True):
        st.session_state.qty = inicial()
        st.rerun()
    if st.button('Zerar controle', use_container_width=True):
        st.session_state.qty = {}
        st.rerun()

st.subheader(f'{secao} — {SECTIONS[secao]}')
cols = st.columns(5)
for i, n in enumerate(range(1, 21)):
    codigo = f'{secao}-{n}'
    with cols[i % 5]:
        atual = int(st.session_state.qty.get(codigo, 0))
        novo = st.number_input(codigo, min_value=0, max_value=99, step=1, value=atual, key=f'input_{codigo}')
        st.session_state.qty[codigo] = int(novo)

t1, t2, t3 = st.tabs(['📌 Faltantes', '🔁 Repetidas', '⬇️ Exportações'])
with t1:
    st.text_area('Lista pronta para copiar/WhatsApp', faltantes_texto(), height=420)
with t2:
    st.text_area('Lista de repetidas para troca', repetidas_texto(), height=420)
with t3:
    st.download_button('Baixar backup JSON', export_json(), 'backup_controle_figurinhas_copa_2026.json', 'application/json', use_container_width=True)
    st.download_button('Baixar CSV', export_csv().encode('utf-8-sig'), 'controle_figurinhas_copa_2026.csv', 'text/csv', use_container_width=True)
