import streamlit as st
import json
import os
from datetime import datetime, timedelta
import time

# ============================================================
# CONFIGURACAO DA PAGINA
# ============================================================
st.set_page_config(
    page_title="Activity Tracker - UpFlux",
    page_icon="https://upflux.io/wp-content/uploads/2023/03/favicon-upflux.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DADOS DE ORGANIZACOES E PROCESSOS (Fonte: planilha SharePoint - aba In)
# ============================================================
ORG_PROCESS_DATA = {
    "Circulo Saude": ["Centro Cirurgico", "Ciclo de Receitas", "Desospitalizacao", "Pronto Atendimento", "Protocolo Sepse", "Protocolo TEV", "Protocolo AVC", "Protocolo DorT", "Giro de Leito", "Solicitacao de Leito"],
    "Ciser": ["O2C", "O2C Torre de Controle"],
    "DASA": ["Ciclo de Receitas"],
    "DASA Hospitais": ["[HSP] Internacao e Desospitalizacao", "H9J - Ciclo de Receita (Gestao de Autorizacao)", "H9J - Ciclo de Receita KFlow", "H9J - Internacao e Desospitalizacao", "H9J - Pronto Atendimento", "H9J - Protocolo de Sepse", "HBR- Pronto Atendimento", "HSL - Internacao e Desospitalizacao", "HSP - Pronto Atendimento", "Protocolo AVC"],
    "DASA Laboratorios": ["Painel MDP"],
    "Duas Rodas": ["P2P"],
    "Electrolux - ADM - P2P": ["P2P-HML"],
    "Electrolux - Curitiba": ["Produtividade e Qualidade"],
    "Electrolux - Sao Carlos": ["1. Produtividade", "2. Logistica"],
    "FCMC - Fundacao Centro Medico Campinas": ["Pronto Atendimento", "Protocolo Dor Toracica / IAM"],
    "FCV - Hospital do Cancer de Muriae": ["Oncologia"],
    "Grupo Aldo": ["A2P", "P2P", "P2P-HML"],
    "Grupo Marista": ["Cajuru Internacao e Desospitalizacao", "Cajuru Pronto Socorro", "Centro Cirurgico", "Ciclo de Receitas", "Marcelino Internacao e Desospitalizacao", "Marcelino Pronto Atendimento"],
    "Hopsital PUC Campinas": ["Pronto Atendimento"],
    "Hospital Moinhos de Vento": ["Internacao e Desospitalizacao"],
    "Hospital Napoleao Laureano": ["Linha de Cuidado - Mama HNL"],
    "Hospital Porto Dias": ["Ciclo de Receita"],
    "Hospital Prontocardio": ["Centro Cirurgico", "Internacao e Desospitalizacao", "Pronto Atendimento"],
    "Hospital Regional Piracicaba": ["Centro Cirurgico", "Internacao e Desospitalizacao", "Linha de Cuidado Cirurgica"],
    "Hospital Santa Isabel": ["Protocolo Sepse v2", "Centro Cirurgico", "Internacao e Desospitalizacao", "ProntoAtendimento", "Protocolo AVC", "Protocolo Dor Toracica", "Protocolo TEV"],
    "Hospital Sao Jose": ["Centro de Imagem", "Pronto Atendimento"],
    "Imed Group": ["Sao Camilo - Pronto Atendimento"],
    "Lindt": ["P2P"],
    "OdontoPrev": ["Customer Services"],
    "Pronutrir": ["Ciclo de Receita"],
    "Rede Santa Catarina": ["Centro Cirurgico", "Pronto Atendimento", "Ciclo de Receita", "Sepse", "Oncologia"],
    "Romagnole": ["P2P"],
    "Santa Casa de Misericordia": ["Giro de Leito 2.0"],
    "UFENESP": ["Auditoria de Contas"],
    "Unimed Alem Paraiba": ["Homologacao - Auditoria de Contas"],
    "Unimed Anhanguera": ["1 - Auditoria de Contas"],
    "Unimed Apucarana": ["Contas Intercambio", "Contas Locais"],
    "Unimed BH": ["Protocolos", "Protocolo AVC", "Protocolo ITU", "Protocolo PNM", "Protocolo Diarreia", "Protocolo Asma", "Protocolo IAM", "Protocolo IVAS"],
    "Unimed Campo Grande": ["Linhas de Cuidado Viver Bem", "Ciclo de Receita Hospitalar", "Internacao de Desospitalizacao"],
    "Unimed Campo Mourao": ["Auditoria de Contas - Local", "Gestao de Intercambio", "JornadaOncologica - Cardio", "JornadaOncologica - Tasy", "Auditoria de Contas - Intercambio"],
    "Unimed Cianorte": ["Auditoria de Contas Intercambio", "Auditoria DGU"],
    "Unimed Costa Oeste": ["Intercambio", "Rede Local"],
    "Unimed Goiania": ["Inteligencia de Auditoria - Producao"],
    "Unimed Jaragua do Sul": ["Ciclo de Receitas", "Pronto Atendimento"],
    "Unimed Joinville - OPS": ["Analise de Custo", "Auditoria de Contas - Rede Prestadora", "Auditoria de Contas CHU", "Auditoria de Contas Intercambio"],
    "Unimed Maringa": ["Pronto Atendimento", "Pronto Atendimento-Produto"],
    "Unimed Norte Parana": ["Auditoria de Contas Intercambio", "Auditoria de Contas Rede"],
    "Unimed Norte Paulista": ["1 - Auditoria de Contas Intercambio (Em Implantacao)"],
    "Unimed Parana": ["Auditoria de Contas", "TEA", "Integra 2.0"],
    "Unimed Parana - Jornada do Paciente": ["Jornada do Paciente"],
    "Unimed Paranavai": ["Auditoria de Contas (Intercambio)"],
    "Unimed Pelotas": ["Centro de Imagens", "Jornada do Paciente", "Pronto Atendimento"],
    "Unimed Pindamonhangaba": ["Centro Cirurgico", "Ciclo de Receita", "Internacao e Desospitalizacao", "3. Auditoria de Contas - Intercambio (Em Implantacao)"],
    "Unimed Ponta Grossa": ["Pronto Atendimento", "Auditoria de Contas - Intercambio", "Auditoria de Contas - Local", "Auditoria de Liberacao", "Gestao de Oncologia", "Internacao", "Internacao e Desospitalizacao"],
    "Unimed Rio Grande do Sul - Federacao RS": ["1 - Auditoria de Contas (Em Implantacao)", "2 - Auditoria de Contas (Local) (Em Implantacao)"],
    "Unimed Rio Verde": ["1. Auditoria de Contas Intercambio - Producao", "2. Auditoria de Contas Local - Producao"],
    "Unimed Sao Jose do Rio Preto": ["Auditoria de Contas - Homologacao", "Contas a Pagar", "Pronto Atendimento"],
    "Unimed Sao Jose dos Campos": ["Governanca Clinica", "Assistencial - Internacao", "Assistencial - UTI", "Centro de Imagem", "Gestao de Riscos - Qualiex", "Jornada Cirurgica", "Pronto Atendimento"],
    "Unimed Sao Jose dos Campos - OPS": ["001 - Auditoria de Contas (Em Implantacao)"],
    "Unimed Sergipe": ["002 - Auditoria de Contas Local"],
    "Unimed Serra Gaucha": ["Jornada Hospitalar - Produto", "01 Auditoria de Contas Local (Em Implantacao)", "02 Auditoria de Contas Intercambio (Em Implantacao)"],
    "Unimed Sorocaba": ["Auditoria de Contas - Homologacao", "Intercambio", "Recurso Proprio", "Rede Prestadora"],
    "Unimed Tatui": ["Pronto Atendimento"],
    "Unimed Teresina": ["Auditoria Local - MV"],
    "Unimed VTRP": ["Area de Acao", "Intercambio", "Auditoria de Contas (Em Implantacao)"],
    "Unimed Vale do Aco": ["Intercambio - Producao"],
    "Unimed Vale do Piquiri": ["Auditoria de Contas"],
    "UpFlux Gerenciamento": ["Projects - Deploy", "Sevice Management - Support", "User 360 - UX + NPS"],
    "VR Beneficio": ["Incidentes", "Requisicoes de servicos"],
}

# ============================================================
# CAMINHOS DE DADOS
# ============================================================
DATA_DIR = "data"
ACTIVITIES_FILE = os.path.join(DATA_DIR, "activities.json")
INTEGRATORS_FILE = os.path.join(DATA_DIR, "integrators.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

# ============================================================
# FUNCOES DE PERSISTENCIA
# ============================================================
def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_json(filepath, default):
    ensure_data_dir()
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return default
    return default

def save_json(filepath, data):
    ensure_data_dir()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

def load_activities():
    return load_json(ACTIVITIES_FILE, [])

def save_activities(activities):
    save_json(ACTIVITIES_FILE, activities)

def load_integrators():
    default = [
        {"nome": "Luis Gabriel", "email": "luis.gabriel@upflux.ai"},
    ]
    return load_json(INTEGRATORS_FILE, default)

def save_integrators(integrators):
    save_json(INTEGRATORS_FILE, integrators)

def load_config():
    default = {
        "alert_threshold_minutes": 180,
        "critical_threshold_minutes": 240,
        "jira_threshold_minutes": 360,
        "teams_webhook_url": "",
        "jira_api_url": "",
        "jira_project_key": "SU"
    }
    return load_json(CONFIG_FILE, default)

def save_config(config):
    save_json(CONFIG_FILE, config)

# ============================================================
# CSS CUSTOMIZADO - CORES UPFLUX
# ============================================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global */
    .stApp {
        background-color: #0a0e1a;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0f1424 !important;
        border-right: 1px solid #1e2642;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #c8d1e0 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label {
        color: #c8d1e0 !important;
    }

    /* Header area */
    .app-header {
        background: linear-gradient(135deg, #0f1424 0%, #151b30 50%, #0f1424 100%);
        border: 1px solid #1e2642;
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .app-header img {
        height: 40px;
    }
    .app-header .title {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .app-header .subtitle {
        color: #7b88a0;
        font-size: 0.9rem;
        margin-top: 2px;
    }

    /* Metric Cards - UpFlux Style */
    .metric-card {
        background: linear-gradient(135deg, #111827 0%, #1a2235 100%);
        border: 1px solid #1e2642;
        border-radius: 14px;
        padding: 22px 20px;
        text-align: center;
        margin-bottom: 12px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 212, 170, 0.08);
    }
    .metric-card h3 {
        color: #7b88a0;
        font-size: 0.78rem;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
    }
    .metric-card .value {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.1;
    }

    /* Activity card */
    .activity-card {
        background: linear-gradient(135deg, #111827 0%, #1a2235 100%);
        border-left: 4px solid #00d4aa;
        border-radius: 10px;
        padding: 16px 22px;
        margin-bottom: 10px;
        transition: transform 0.15s;
    }
    .activity-card:hover {
        transform: translateX(3px);
    }
    .activity-card.warning {
        border-left-color: #f59e0b;
    }
    .activity-card.danger {
        border-left-color: #ef4444;
    }

    /* Ranking */
    .rank-item {
        background: linear-gradient(135deg, #111827 0%, #1a2235 100%);
        border: 1px solid #1e2642;
        border-radius: 10px;
        padding: 14px 22px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .rank-1 { border-left: 4px solid #fbbf24; }
    .rank-2 { border-left: 4px solid #94a3b8; }
    .rank-3 { border-left: 4px solid #cd7f32; }

    /* Section titles */
    .section-title {
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 24px 0 16px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Footer - UpFlux */
    .footer {
        text-align: center;
        padding: 24px;
        color: #4a5568;
        font-size: 0.78rem;
        margin-top: 48px;
        border-top: 1px solid #1e2642;
        letter-spacing: 0.3px;
    }
    .footer a {
        color: #00d4aa;
        text-decoration: none;
    }

    /* Status badge */
    .status-active {
        background-color: rgba(0, 212, 170, 0.12);
        color: #00d4aa;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .status-completed {
        background-color: rgba(74, 144, 217, 0.12);
        color: #4a90d9;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
    }

    /* Primary button override */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%) !important;
        color: #0a0e1a !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-size: 1rem !important;
        letter-spacing: 0.5px !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #00e6b8 0%, #00d4aa 100%) !important;
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3) !important;
    }

    /* Divider */
    hr {
        border-color: #1e2642 !important;
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #111827 !important;
        border-color: #1e2642 !important;
    }

    /* Text input */
    .stTextInput > div > div > input {
        background-color: #111827 !important;
        border-color: #1e2642 !important;
        color: #ffffff !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #111827;
        border-radius: 8px;
        color: #7b88a0;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1a2235 !important;
        color: #00d4aa !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 16px 0 8px 0;">
        <img src="https://upflux.io/wp-content/uploads/2023/03/logo-upflux-white.png" width="150" alt="UpFlux Logo" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
        <div style="display:none; color: #00d4aa; font-size: 1.5rem; font-weight: 800; letter-spacing: -1px;">UpFlux</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    integrators = load_integrators()
    integrator_names = [i["nome"] for i in integrators]

    if not integrator_names:
        st.warning("Nenhum integrador cadastrado. Va em Configuracoes.")
        selected_user = None
    else:
        selected_user = st.selectbox("Integrador", integrator_names, key="user_select")

    st.markdown("---")

    page = st.radio(
        "Navegacao",
        ["Dashboard", "Historico", "Ranking", "Configuracoes"],
        key="nav"
    )

# ============================================================
# FUNCOES AUXILIARES
# ============================================================
def get_active_activities(activities):
    return [a for a in activities if a.get("status") == "active"]

def get_user_active(activities, user):
    return [a for a in activities if a.get("status") == "active" and a.get("integrador") == user]

def get_completed_activities(activities):
    return [a for a in activities if a.get("status") == "completed"]

def format_duration(start_str):
    try:
        start = datetime.fromisoformat(start_str)
        delta = datetime.now() - start
        hours = int(delta.total_seconds() // 3600)
        minutes = int((delta.total_seconds() % 3600) // 60)
        return f"{hours:02d}h {minutes:02d}m"
    except:
        return "00h 00m"

def get_duration_minutes(start_str, end_str=None):
    try:
        start = datetime.fromisoformat(start_str)
        end = datetime.fromisoformat(end_str) if end_str else datetime.now()
        return (end - start).total_seconds() / 60
    except:
        return 0

def get_duration_class(start_str):
    minutes = get_duration_minutes(start_str)
    if minutes > 240:
        return "danger"
    elif minutes > 180:
        return "warning"
    return ""

# ============================================================
# PAGINA: DASHBOARD
# ============================================================
def page_dashboard():
    # Header with logo
    st.markdown("""
    <div class="app-header">
        <img src="https://upflux.io/wp-content/uploads/2023/03/logo-upflux-white.png" alt="UpFlux" onerror="this.outerHTML='<span style=\\'color:#00d4aa;font-size:1.8rem;font-weight:800;\\'>UpFlux</span>'">
        <div>
            <div class="title">Activity Tracker</div>
            <div class="subtitle">Controle de atividades da equipe de integracao UpFlux</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    activities = load_activities()
    active = get_active_activities(activities)
    completed_today = [
        a for a in get_completed_activities(activities)
        if a.get("fim", "")[:10] == datetime.now().strftime("%Y-%m-%d")
    ]

    # Metricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Atividades Ativas</h3>
            <div class="value">{len(active)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Concluidas Hoje</h3>
            <div class="value">{len(completed_today)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        alerts = len([a for a in active if get_duration_minutes(a["inicio"]) > 180])
        st.markdown(f"""
        <div class="metric-card">
            <h3>Alertas</h3>
            <div class="value" style="color: {'#ef4444' if alerts > 0 else '#00d4aa'}">{alerts}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Integradores Online</h3>
            <div class="value">{len(set(a['integrador'] for a in active))}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick Start
    if selected_user:
        st.markdown('<div class="section-title">Iniciar Atividade</div>', unsafe_allow_html=True)

        user_active = get_user_active(activities, selected_user)

        if user_active:
            st.info(f"Voce ja tem {len(user_active)} atividade(s) ativa(s). Finalize antes de iniciar outra.")

        col_org, col_proc, col_desc = st.columns([2, 2, 3])
        with col_org:
            org = st.selectbox("Organizacao", sorted(ORG_PROCESS_DATA.keys()), key="org_select")
        with col_proc:
            processes = ORG_PROCESS_DATA.get(org, [])
            proc = st.selectbox("Processo", processes, key="proc_select")
        with col_desc:
            desc = st.text_input("Descricao (opcional)", placeholder="Ex: Analise de conformidade...", key="desc_input")

        if st.button("INICIAR", use_container_width=True, type="primary"):
            if not user_active:
                new_activity = {
                    "id": f"{selected_user}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "integrador": selected_user,
                    "organizacao": org,
                    "processo": proc,
                    "descricao": desc,
                    "inicio": datetime.now().isoformat(),
                    "fim": None,
                    "status": "active",
                    "duracao_minutos": 0
                }
                activities.append(new_activity)
                save_activities(activities)
                st.success(f"Atividade iniciada: {org} - {proc}")
                st.rerun()
            else:
                st.warning("Finalize a atividade atual antes de iniciar uma nova.")

    st.markdown("---")

    # Atividades ativas
    st.markdown('<div class="section-title">Atividades em Andamento</div>', unsafe_allow_html=True)

    if not active:
        st.info("Nenhuma atividade em andamento no momento.")
    else:
        for act in active:
            duration_class = get_duration_class(act["inicio"])
            duration = format_duration(act["inicio"])
            minutes = get_duration_minutes(act["inicio"])

            alert_icon = ""
            if minutes > 240:
                alert_icon = "&#128308;"
            elif minutes > 180:
                alert_icon = "&#128993;"
            else:
                alert_icon = "&#128994;"

            st.markdown(f"""
            <div class="activity-card {duration_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #ffffff; font-size: 1.1rem;">{act['integrador']}</strong>
                        <span style="color: #7b88a0; margin-left: 10px;">{act['organizacao']} - {act['processo']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.3rem; font-weight: 700; color: #ffffff;">{alert_icon} {duration}</span>
                    </div>
                </div>
                {f'<div style="color: #5a6478; margin-top: 5px; font-size: 0.85rem;">{act.get("descricao", "")}</div>' if act.get("descricao") else ''}
            </div>
            """, unsafe_allow_html=True)

            # Stop button per activity
            if act.get("integrador") == selected_user:
                if st.button(f"PARAR ATIVIDADE", key=f"stop_{act['id']}", use_container_width=True):
                    for a in activities:
                        if a["id"] == act["id"]:
                            a["status"] = "completed"
                            a["fim"] = datetime.now().isoformat()
                            a["duracao_minutos"] = round(get_duration_minutes(a["inicio"], a["fim"]), 1)
                            break
                    save_activities(activities)
                    st.success("Atividade finalizada!")
                    st.rerun()

# ============================================================
# PAGINA: HISTORICO
# ============================================================
def page_historico():
    st.markdown('<div class="section-title" style="font-size: 1.5rem;">Historico de Atividades</div>', unsafe_allow_html=True)

    activities = load_activities()
    completed = get_completed_activities(activities)
    completed.sort(key=lambda x: x.get("fim", ""), reverse=True)

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        integrators = load_integrators()
        filter_user = st.selectbox("Filtrar por integrador", ["Todos"] + [i["nome"] for i in integrators], key="hist_filter_user")
    with col2:
        filter_org = st.selectbox("Filtrar por organizacao", ["Todas"] + sorted(ORG_PROCESS_DATA.keys()), key="hist_filter_org")
    with col3:
        filter_period = st.selectbox("Periodo", ["Hoje", "Ultimos 7 dias", "Ultimos 30 dias", "Tudo"], key="hist_filter_period")

    # Aplicar filtros
    filtered = completed
    if filter_user != "Todos":
        filtered = [a for a in filtered if a.get("integrador") == filter_user]
    if filter_org != "Todas":
        filtered = [a for a in filtered if a.get("organizacao") == filter_org]

    now = datetime.now()
    if filter_period == "Hoje":
        filtered = [a for a in filtered if a.get("fim", "")[:10] == now.strftime("%Y-%m-%d")]
    elif filter_period == "Ultimos 7 dias":
        cutoff = (now - timedelta(days=7)).strftime("%Y-%m-%d")
        filtered = [a for a in filtered if a.get("fim", "")[:10] >= cutoff]
    elif filter_period == "Ultimos 30 dias":
        cutoff = (now - timedelta(days=30)).strftime("%Y-%m-%d")
        filtered = [a for a in filtered if a.get("fim", "")[:10] >= cutoff]

    st.markdown(f"**{len(filtered)} atividades encontradas**")

    if filtered:
        for act in filtered[:50]:
            dur = act.get("duracao_minutos", 0)
            hours = int(dur // 60)
            mins = int(dur % 60)

            fim_str = ""
            if act.get("fim"):
                try:
                    fim_dt = datetime.fromisoformat(act["fim"])
                    fim_str = fim_dt.strftime("%d/%m/%Y %H:%M")
                except:
                    fim_str = act["fim"]

            st.markdown(f"""
            <div class="activity-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #ffffff;">{act['integrador']}</strong>
                        <span style="color: #7b88a0; margin-left: 10px;">{act['organizacao']} - {act['processo']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #00d4aa; font-weight: 600;">{hours:02d}h {mins:02d}m</span>
                        <div style="color: #5a6478; font-size: 0.75rem;">{fim_str}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma atividade encontrada com os filtros selecionados.")

# ============================================================
# PAGINA: RANKING
# ============================================================
def page_ranking():
    st.markdown('<div class="section-title" style="font-size: 1.5rem;">Ranking de Integradores</div>', unsafe_allow_html=True)
    st.markdown("*Pontuacao: (atividades x 10) + bonus por tempo medio abaixo de 2h*")

    activities = load_activities()
    completed = get_completed_activities(activities)
    integrators = load_integrators()

    # Filtro de periodo
    period = st.selectbox("Periodo", ["Ultimos 7 dias", "Ultimos 30 dias", "Todo o periodo"], key="rank_period")

    now = datetime.now()
    if period == "Ultimos 7 dias":
        cutoff = (now - timedelta(days=7)).strftime("%Y-%m-%d")
        completed = [a for a in completed if a.get("fim", "")[:10] >= cutoff]
    elif period == "Ultimos 30 dias":
        cutoff = (now - timedelta(days=30)).strftime("%Y-%m-%d")
        completed = [a for a in completed if a.get("fim", "")[:10] >= cutoff]

    # Calcular pontuacao
    ranking = []
    for integ in integrators:
        nome = integ["nome"]
        user_acts = [a for a in completed if a.get("integrador") == nome]
        count = len(user_acts)

        if count > 0:
            avg_duration = sum(a.get("duracao_minutos", 0) for a in user_acts) / count
            base_score = count * 10
            bonus = 20 if avg_duration < 120 else 0
            total_score = base_score + bonus
            ranking.append({
                "nome": nome,
                "atividades": count,
                "media_minutos": avg_duration,
                "pontuacao": total_score
            })
        else:
            ranking.append({
                "nome": nome,
                "atividades": 0,
                "media_minutos": 0,
                "pontuacao": 0
            })

    ranking.sort(key=lambda x: x["pontuacao"], reverse=True)

    medals = ["&#129351;", "&#129352;", "&#129353;"]
    for i, r in enumerate(ranking):
        medal = medals[i] if i < 3 else f"#{i+1}"
        rank_class = f"rank-{i+1}" if i < 3 else ""
        avg_h = int(r["media_minutos"] // 60)
        avg_m = int(r["media_minutos"] % 60)

        st.markdown(f"""
        <div class="rank-item {rank_class}">
            <div style="display: flex; align-items: center; gap: 15px;">
                <span style="font-size: 1.5rem;">{medal}</span>
                <div>
                    <strong style="color: #ffffff; font-size: 1.1rem;">{r['nome']}</strong>
                    <div style="color: #7b88a0; font-size: 0.8rem;">{r['atividades']} atividades - Media: {avg_h:02d}h {avg_m:02d}m</div>
                </div>
            </div>
            <div style="text-align: right;">
                <span style="color: #00d4aa; font-size: 1.5rem; font-weight: 700;">{r['pontuacao']}</span>
                <div style="color: #7b88a0; font-size: 0.75rem;">pontos</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# PAGINA: CONFIGURACOES
# ============================================================
def page_config():
    st.markdown('<div class="section-title" style="font-size: 1.5rem;">Configuracoes</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Integradores", "Alertas", "Integracoes"])

    with tab1:
        st.markdown("### Gerenciar Integradores")
        integrators = load_integrators()

        # Adicionar novo
        st.markdown("**Adicionar Integrador**")
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            new_name = st.text_input("Nome", key="new_integ_name")
        with col2:
            new_email = st.text_input("Email", key="new_integ_email")
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Adicionar", key="add_integ"):
                if new_name and new_email:
                    integrators.append({"nome": new_name, "email": new_email})
                    save_integrators(integrators)
                    st.success(f"Integrador {new_name} adicionado!")
                    st.rerun()
                else:
                    st.warning("Preencha nome e email.")

        # Lista atual
        st.markdown("**Integradores Cadastrados**")
        for i, integ in enumerate(integrators):
            col1, col2, col3 = st.columns([2, 3, 1])
            with col1:
                st.text(integ["nome"])
            with col2:
                st.text(integ["email"])
            with col3:
                if st.button("Remover", key=f"del_integ_{i}"):
                    integrators.pop(i)
                    save_integrators(integrators)
                    st.rerun()

    with tab2:
        st.markdown("### Configuracao de Alertas")
        config = load_config()

        config["alert_threshold_minutes"] = st.number_input(
            "Alerta gentil (minutos)",
            value=config["alert_threshold_minutes"],
            min_value=30, max_value=600,
            help="Lembrete gentil apos este tempo"
        )
        config["critical_threshold_minutes"] = st.number_input(
            "Alerta critico (minutos)",
            value=config["critical_threshold_minutes"],
            min_value=60, max_value=720,
            help="Alerta no canal do time apos este tempo"
        )
        config["jira_threshold_minutes"] = st.number_input(
            "Criar ticket Jira (minutos)",
            value=config["jira_threshold_minutes"],
            min_value=120, max_value=1440,
            help="Criacao automatica de ticket no Jira"
        )

        if st.button("Salvar Configuracoes de Alertas", key="save_alerts"):
            save_config(config)
            st.success("Configuracoes salvas!")

    with tab3:
        st.markdown("### Integracoes")
        config = load_config()

        st.markdown("**Microsoft Teams**")
        config["teams_webhook_url"] = st.text_input(
            "Webhook URL (Incoming Webhook)",
            value=config.get("teams_webhook_url", ""),
            type="password",
            key="teams_webhook"
        )

        st.markdown("**Jira**")
        config["jira_api_url"] = st.text_input(
            "Jira API URL",
            value=config.get("jira_api_url", ""),
            placeholder="https://sua-empresa.atlassian.net",
            key="jira_url"
        )
        config["jira_project_key"] = st.text_input(
            "Project Key",
            value=config.get("jira_project_key", "SU"),
            key="jira_key"
        )

        if st.button("Salvar Integracoes", key="save_integrations"):
            save_config(config)
            st.success("Integracoes salvas!")

# ============================================================
# ROTEAMENTO
# ============================================================
if page == "Dashboard":
    page_dashboard()
elif page == "Historico":
    page_historico()
elif page == "Ranking":
    page_ranking()
elif page == "Configuracoes":
    page_config()

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    Desenvolvido por Luis Gabriel Bernardi - <a href="https://upflux.io" target="_blank">UpFlux</a> Activity Tracker v1.0
</div>
""", unsafe_allow_html=True)
