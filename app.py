import streamlit as st
import json
import os
from datetime import datetime, timedelta
import time

# Page config - NO sidebar
st.set_page_config(
    page_title="Activity Tracker - UpFlux",
    page_icon="*",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ORG_PROCESS_DATA - All 64 organizations exactly as specified
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

# Data paths
DATA_DIR = "data"
ACTIVITIES_FILE = os.path.join(DATA_DIR, "activities.json")
INTEGRATORS_FILE = os.path.join(DATA_DIR, "integrators.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

# Persistence functions
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

# Helper functions
def get_active_activities(activities):
    return [a for a in activities if a.get("status") == "active"]

def get_completed_activities(activities):
    return [a for a in activities if a.get("status") == "completed"]

def get_today_completed(activities):
    today = datetime.now().strftime("%Y-%m-%d")
    return [a for a in activities if a.get("status") == "completed" and a.get("fim", "")[:10] == today]

def get_user_active(activities, user):
    return [a for a in activities if a.get("status") == "active" and a.get("integrador") == user]

def get_duration_minutes(start_str, end_str=None):
    try:
        start = datetime.fromisoformat(start_str)
        end = datetime.fromisoformat(end_str) if end_str else datetime.now()
        return (end - start).total_seconds() / 60
    except:
        return 0

def format_duration(start_str):
    minutes = get_duration_minutes(start_str)
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    secs = int((minutes * 60) % 60)
    return f"{hours:02d}:{mins:02d}:{secs:02d}"

def get_duration_class(start_str):
    minutes = get_duration_minutes(start_str)
    if minutes > 240:
        return "danger"
    elif minutes > 180:
        return "warning"
    return ""

def get_initials(name):
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    return name[:2].upper()

# CSS - Professional dark theme matching reference
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        background-color: #0a0e1a;
        font-family: 'Inter', sans-serif;
    }

    /* Hide sidebar completely */
    section[data-testid="stSidebar"] { display: none; }
    button[data-testid="stSidebarCollapsedControl"] { display: none; }

    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    /* Top header bar */
    .top-header {
        background: linear-gradient(135deg, #0f1424 0%, #151b30 100%);
        border-bottom: 1px solid #1e2642;
        padding: 16px 32px;
        margin: -1rem -1rem 24px -1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .logo-area {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .logo-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #00d4aa, #00b894);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    .logo-text {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .logo-text span {
        color: #00d4aa;
    }

    /* Tabs styling - make them look like the reference nav */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background: linear-gradient(135deg, #0f1424 0%, #151b30 100%);
        border: 1px solid #1e2642;
        border-radius: 12px;
        padding: 4px;
        margin-bottom: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #7b88a0;
        font-weight: 500;
        font-size: 0.95rem;
        padding: 10px 24px;
        border-radius: 8px;
        background: transparent;
        border: none;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
        background: rgba(0, 212, 170, 0.08);
    }
    .stTabs [aria-selected="true"] {
        color: #00d4aa !important;
        background: rgba(0, 212, 170, 0.12) !important;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #00d4aa;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* Section cards */
    .section-card {
        background: linear-gradient(135deg, #111827 0%, #1a2235 100%);
        border: 1px solid #1e2642;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #111827 0%, #1a2235 100%);
        border: 1px solid #1e2642;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 212, 170, 0.08);
    }
    .metric-card h3 {
        color: #7b88a0;
        font-size: 0.72rem;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
    }
    .metric-card .value {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.2;
    }
    .metric-card .subtitle {
        color: #5a6478;
        font-size: 0.75rem;
        margin-top: 4px;
    }

    /* Activity card - rich design */
    .activity-card {
        background: linear-gradient(135deg, #111827 0%, #1a2235 100%);
        border: 1px solid #1e2642;
        border-left: 4px solid #00d4aa;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        transition: transform 0.15s;
    }
    .activity-card:hover { transform: translateX(3px); }
    .activity-card.warning { border-left-color: #f59e0b; }
    .activity-card.danger { border-left-color: #ef4444; }

    .avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        color: #ffffff;
        flex-shrink: 0;
    }
    .avatar-green { background: linear-gradient(135deg, #00d4aa, #00b894); }
    .avatar-blue { background: linear-gradient(135deg, #3b82f6, #2563eb); }
    .avatar-purple { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }
    .avatar-orange { background: linear-gradient(135deg, #f59e0b, #d97706); }

    .activity-info { flex: 1; }
    .activity-name {
        color: #ffffff;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .activity-detail {
        color: #7b88a0;
        font-size: 0.8rem;
        margin-top: 2px;
    }
    .activity-timer {
        font-family: 'JetBrains Mono', 'Courier New', monospace;
        font-size: 1.2rem;
        font-weight: 700;
        color: #ffffff;
        min-width: 100px;
        text-align: center;
    }
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .badge-active { background: rgba(0, 212, 170, 0.15); color: #00d4aa; }
    .badge-warning { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
    .badge-danger { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

    /* Section title */
    .section-title {
        color: #ffffff;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 20px 0 16px 0;
        display: flex;
        align-items: center;
        gap: 10px;
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

    /* Constrain form elements width */
    .stSelectbox, .stTextInput, .stNumberInput {
        max-width: 100%;
    }

    /* Button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00d4aa, #00b894) !important;
        color: #0a0e1a !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 8px 24px !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 24px;
        color: #4a5568;
        font-size: 0.78rem;
        margin-top: 48px;
        border-top: 1px solid #1e2642;
    }
    .footer a { color: #00d4aa; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# TOP HEADER with logo and user selector
# ============================================================
header_col1, header_col2 = st.columns([4, 1])
with header_col1:
    st.markdown("""
    <div class="logo-area">
        <div class="logo-icon">!</div>
        <div class="logo-text"><span>Activity</span> Tracker</div>
    </div>
    """, unsafe_allow_html=True)
with header_col2:
    integrators = load_integrators()
    integrator_names = [i["nome"] for i in integrators]
    selected_user = st.selectbox("Integrador", integrator_names, key="user_select", label_visibility="collapsed")

# ============================================================
# HORIZONTAL TABS for navigation
# ============================================================
tab_dashboard, tab_historico, tab_ranking, tab_config = st.tabs(["Dashboard", "Historico", "Ranking", "Configuracoes"])

# ============================================================
# TAB: DASHBOARD
# ============================================================
with tab_dashboard:
    activities = load_activities()
    active = get_active_activities(activities)
    today_completed = get_today_completed(activities)
    config = load_config()
    alerts = len([a for a in active if get_duration_minutes(a["inicio"]) > config["alert_threshold_minutes"]])

    # Metric Cards Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Atividades em Andamento</h3>
            <div class="value" style="color: #00d4aa">{len(active)}</div>
            <div class="subtitle">Integradores trabalhando agora</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Finalizadas Hoje</h3>
            <div class="value">{len(today_completed)}</div>
            <div class="subtitle">Concluidas no dia</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        avg_min = 0
        if today_completed:
            avg_min = sum(a.get("duracao_minutos", 0) for a in today_completed) / len(today_completed)
        avg_h = int(avg_min // 60)
        avg_m = int(avg_min % 60)
        st.markdown(f"""
        <div class="metric-card">
            <h3>Tempo Medio Hoje</h3>
            <div class="value">{avg_h}h {avg_m:02d}m</div>
            <div class="subtitle">Meta: abaixo de 2h</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Alertas Pendentes</h3>
            <div class="value" style="color: {'#ef4444' if alerts > 0 else '#00d4aa'}">{alerts}</div>
            <div class="subtitle">Atividades > 4h abertas</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Registration - constrained width
    if selected_user:
        st.markdown('<div class="section-title">Registro Rapido de Atividade</div>', unsafe_allow_html=True)

        user_active = get_user_active(activities, selected_user)
        if user_active:
            st.info(f"Voce ja tem {len(user_active)} atividade(s) ativa(s). Finalize antes de iniciar outra.")

        # Use columns with spacers to constrain width - 3 selectors + 1 button in a row
        col_org, col_proc, col_btn = st.columns([3, 3, 1])
        with col_org:
            org = st.selectbox("Cliente (Organizacao)", sorted(ORG_PROCESS_DATA.keys()), key="org_select")
        with col_proc:
            processes = ORG_PROCESS_DATA.get(org, [])
            proc = st.selectbox("Processo", processes, key="proc_select")
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            start_btn = st.button("Iniciar", use_container_width=True, type="primary")

        # Description field - constrained to 2/3 width
        col_desc, col_space = st.columns([5, 2])
        with col_desc:
            desc = st.text_input("Observacao (opcional)", placeholder="Ex: Ajustando modelo de referencia, corrigindo ETL...", key="desc_input")

        if start_btn:
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

    st.markdown("<br>", unsafe_allow_html=True)

    # Active activities and Timeline side by side
    col_activities, col_timeline = st.columns([3, 2])

    with col_activities:
        st.markdown('<div class="section-title">Atividades em Andamento</div>', unsafe_allow_html=True)

        if not active:
            st.info("Nenhuma atividade em andamento no momento.")
        else:
            avatar_colors = ["avatar-green", "avatar-blue", "avatar-purple", "avatar-orange"]
            for idx, act in enumerate(active):
                duration_class = get_duration_class(act["inicio"])
                duration = format_duration(act["inicio"])
                minutes = get_duration_minutes(act["inicio"])
                initials = get_initials(act["integrador"])
                avatar_class = avatar_colors[idx % len(avatar_colors)]

                if minutes > 240:
                    badge_class = "badge-danger"
                    badge_text = f"+ {int(minutes//60)}h"
                elif minutes > 180:
                    badge_class = "badge-warning"
                    badge_text = "Atencao"
                else:
                    badge_class = "badge-active"
                    badge_text = "Ativo"

                st.markdown(f"""
                <div class="activity-card {duration_class}">
                    <div class="avatar {avatar_class}">{initials}</div>
                    <div class="activity-info">
                        <div class="activity-name">{act['integrador']}</div>
                        <div class="activity-detail">{act['organizacao']} - {act['processo']}</div>
                    </div>
                    <div class="activity-timer">{duration}</div>
                    <span class="status-badge {badge_class}">{badge_text}</span>
                </div>
                """, unsafe_allow_html=True)

                # Stop button only for current user
                if act.get("integrador") == selected_user:
                    if st.button(f"Parar", key=f"stop_{act['id']}"):
                        for a in activities:
                            if a["id"] == act["id"]:
                                a["status"] = "completed"
                                a["fim"] = datetime.now().isoformat()
                                a["duracao_minutos"] = round(get_duration_minutes(a["inicio"], a["fim"]), 1)
                                break
                        save_activities(activities)
                        st.success("Atividade finalizada!")
                        st.rerun()

    with col_timeline:
        st.markdown('<div class="section-title">Timeline Recente</div>', unsafe_allow_html=True)

        # Show recent completed activities as a timeline
        all_completed = get_completed_activities(activities)
        all_completed.sort(key=lambda x: x.get("fim", ""), reverse=True)
        recent = all_completed[:8]

        if not recent:
            st.info("Nenhuma atividade finalizada ainda.")
        else:
            for act in recent:
                fim_str = ""
                if act.get("fim"):
                    try:
                        fim_dt = datetime.fromisoformat(act["fim"])
                        fim_str = fim_dt.strftime("%H:%M")
                    except:
                        fim_str = ""
                dur = act.get("duracao_minutos", 0)
                dur_h = int(dur // 60)
                dur_m = int(dur % 60)

                st.markdown(f"""
                <div style="border-left: 2px solid #1e2642; padding-left: 16px; margin-bottom: 16px; margin-left: 8px;">
                    <div style="color: #5a6478; font-size: 0.75rem;">{fim_str}</div>
                    <div style="color: #ffffff; font-size: 0.85rem; margin-top: 2px;">
                        <strong>{act['integrador']}</strong> finalizou {act['processo']} em <strong>{act['organizacao']}</strong>
                    </div>
                    <div style="color: #7b88a0; font-size: 0.75rem;">Duracao: {dur_h}h {dur_m:02d}m</div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# TAB: HISTORICO
# ============================================================
with tab_historico:
    st.markdown('<div class="section-title" style="font-size: 1.3rem;">Historico de Atividades</div>', unsafe_allow_html=True)

    activities = load_activities()
    completed = get_completed_activities(activities)
    completed.sort(key=lambda x: x.get("fim", ""), reverse=True)

    # Filters - constrained in a row
    col1, col2, col3, col_space = st.columns([2, 2, 2, 1])
    with col1:
        integrators = load_integrators()
        filter_user = st.selectbox("Filtrar por integrador", ["Todos"] + [i["nome"] for i in integrators], key="hist_filter_user")
    with col2:
        filter_org = st.selectbox("Filtrar por organizacao", ["Todas"] + sorted(ORG_PROCESS_DATA.keys()), key="hist_filter_org")
    with col3:
        filter_period = st.selectbox("Periodo", ["Hoje", "Ultimos 7 dias", "Ultimos 30 dias", "Tudo"], key="hist_filter_period")

    # Apply filters
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
                <div class="avatar avatar-blue">{get_initials(act.get('integrador', 'XX'))}</div>
                <div class="activity-info">
                    <div class="activity-name">{act['integrador']}</div>
                    <div class="activity-detail">{act['organizacao']} - {act['processo']}</div>
                </div>
                <div style="text-align: right;">
                    <span style="color: #00d4aa; font-weight: 600;">{hours:02d}h {mins:02d}m</span>
                    <div style="color: #5a6478; font-size: 0.75rem;">{fim_str}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma atividade encontrada com os filtros selecionados.")

# ============================================================
# TAB: RANKING
# ============================================================
with tab_ranking:
    st.markdown('<div class="section-title" style="font-size: 1.3rem;">Ranking de Integradores</div>', unsafe_allow_html=True)
    st.markdown("*Pontuacao: (atividades x 10) + bonus por tempo medio abaixo de 2h*")

    activities = load_activities()
    completed = get_completed_activities(activities)
    integrators = load_integrators()

    # Period filter - constrained width
    col_period, col_space1, col_space2 = st.columns([2, 3, 3])
    with col_period:
        period = st.selectbox("Periodo", ["Ultimos 7 dias", "Ultimos 30 dias", "Todo o periodo"], key="rank_period")

    now = datetime.now()
    if period == "Ultimos 7 dias":
        cutoff = (now - timedelta(days=7)).strftime("%Y-%m-%d")
        completed = [a for a in completed if a.get("fim", "")[:10] >= cutoff]
    elif period == "Ultimos 30 dias":
        cutoff = (now - timedelta(days=30)).strftime("%Y-%m-%d")
        completed = [a for a in completed if a.get("fim", "")[:10] >= cutoff]

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
            ranking.append({"nome": nome, "atividades": count, "media_minutos": avg_duration, "pontuacao": total_score})
        else:
            ranking.append({"nome": nome, "atividades": 0, "media_minutos": 0, "pontuacao": 0})

    ranking.sort(key=lambda x: x["pontuacao"], reverse=True)

    medals = ["1", "2", "3"]
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
# TAB: CONFIGURACOES
# ============================================================
with tab_config:
    st.markdown('<div class="section-title" style="font-size: 1.3rem;">Configuracoes</div>', unsafe_allow_html=True)

    config_tab1, config_tab2, config_tab3 = st.tabs(["Integradores", "Alertas", "Integracoes"])

    with config_tab1:
        st.markdown("### Gerenciar Integradores")
        integrators = load_integrators()

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

    with config_tab2:
        st.markdown("### Configuracao de Alertas")
        config = load_config()

        col1, col2, col3 = st.columns(3)
        with col1:
            config["alert_threshold_minutes"] = st.number_input(
                "Alerta gentil (minutos)", value=config["alert_threshold_minutes"],
                min_value=30, max_value=600, help="Lembrete gentil apos este tempo"
            )
        with col2:
            config["critical_threshold_minutes"] = st.number_input(
                "Alerta critico (minutos)", value=config["critical_threshold_minutes"],
                min_value=60, max_value=720, help="Alerta no canal do time apos este tempo"
            )
        with col3:
            config["jira_threshold_minutes"] = st.number_input(
                "Criar ticket Jira (minutos)", value=config["jira_threshold_minutes"],
                min_value=120, max_value=1440, help="Criacao automatica de ticket no Jira"
            )

        if st.button("Salvar Configuracoes de Alertas", key="save_alerts"):
            save_config(config)
            st.success("Configuracoes salvas!")

    with config_tab3:
        st.markdown("### Integracoes")
        config = load_config()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Microsoft Teams**")
            config["teams_webhook_url"] = st.text_input(
                "Webhook URL (Incoming Webhook)", value=config.get("teams_webhook_url", ""),
                type="password", key="teams_webhook"
            )
        with col2:
            st.markdown("**Jira**")
            config["jira_api_url"] = st.text_input(
                "Jira API URL", value=config.get("jira_api_url", ""),
                placeholder="https://sua-empresa.atlassian.net", key="jira_url"
            )
            config["jira_project_key"] = st.text_input(
                "Project Key", value=config.get("jira_project_key", "SU"), key="jira_key"
            )

        if st.button("Salvar Integracoes", key="save_integrations"):
            save_config(config)
            st.success("Integracoes salvas!")

# Footer
st.markdown("""
<div class="footer">
    Desenvolvido por Luis Gabriel Bernardi - <a href="https://upflux.io" target="_blank">UpFlux</a> Activity Tracker v2.0
</div>
""", unsafe_allow_html=True)
