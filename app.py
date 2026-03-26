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
    page_icon="\u26a1",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DADOS DE ORGANIZACOES E PROCESSOS
# ============================================================
ORG_PROCESS_DATA = {
    "Acelen": ["P2P"],
    "Algar": ["P2P"],
    "Allies Of Skin": ["O2C"],
    "Assai": ["P2P"],
    "BRK Ambiental": ["P2P"],
    "Bayer": ["P2P"],
    "Braskem": ["P2P"],
    "C&A": ["P2P"],
    "CPFL": ["P2P"],
    "CTG": ["P2P"],
    "Carrefour": ["P2P"],
    "Casa & Video": ["P2P"],
    "Cobasi": ["P2P"],
    "Comgas": ["P2P"],
    "Copel": ["P2P"],
    "Cosan": ["P2P"],
    "Creditas": ["P2P"],
    "Dasa": ["P2P"],
    "EDP": ["P2P"],
    "Electrolux": ["P2P"],
    "Eletrobras": ["P2P"],
    "Energisa": ["P2P"],
    "Eneva": ["P2P"],
    "Equatorial": ["P2P"],
    "Eurofarma": ["P2P"],
    "GPA": ["P2P"],
    "Gerdau": ["P2P"],
    "Getninjas": ["P2P"],
    "Globalweb": ["P2P"],
    "Grupo Boticario": ["P2P"],
    "Grupo Petropolis": ["P2P"],
    "Grupo Soma": ["P2P"],
    "Hospital Albert Einstein": ["Assistencial Hospitalar"],
    "Hospital Sirio-Libanes": ["Assistencial Hospitalar"],
    "Hypera": ["P2P"],
    "ISA CTEEP": ["P2P"],
    "Intermedica": ["Auditoria Hospitalar"],
    "JBS": ["P2P"],
    "Klabin": ["P2P"],
    "Localiza": ["P2P"],
    "MRV": ["P2P"],
    "Marfrig": ["P2P"],
    "Minerva Foods": ["P2P"],
    "Movida": ["P2P"],
    "Natura": ["P2P"],
    "Neoenergia": ["P2P"],
    "OdontoPrev": ["Auditoria Hospitalar"],
    "Pague Menos": ["P2P"],
    "Petz": ["P2P"],
    "Qualicorp": ["Auditoria Hospitalar"],
    "Raizen": ["P2P"],
    "Rede D'Or": ["Assistencial Hospitalar", "P2P"],
    "Rumo": ["P2P"],
    "SLC Agricola": ["P2P"],
    "Sabesp": ["P2P"],
    "Santos Brasil": ["P2P"],
    "Suzano": ["P2P"],
    "Supergasbras": ["P2P"],
    "TOTVS": ["P2P"],
    "Taesa": ["P2P"],
    "Unimed": ["Auditoria Hospitalar", "Assistencial Hospitalar"],
    "Usiminas": ["P2P"],
    "Vale": ["P2P"],
    "Via": ["P2P"],
    "Votorantim": ["P2P"],
    "Weg": ["P2P"]
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
# CSS CUSTOMIZADO
# ============================================================
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .metric-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        border: 1px solid #2d3548; border-radius: 12px;
        padding: 20px; text-align: center; margin-bottom: 10px;
    }
    .metric-card h3 { color: #8b95a5; font-size: 0.85rem; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }
    .metric-card .value { color: #ffffff; font-size: 2rem; font-weight: 700; }
    .activity-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        border-left: 4px solid #00d4aa; border-radius: 8px;
        padding: 15px 20px; margin-bottom: 10px;
    }
    .activity-card.warning { border-left-color: #ffaa00; }
    .activity-card.danger { border-left-color: #ff4444; }
    .rank-item {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        border-radius: 8px; padding: 12px 20px; margin-bottom: 8px;
        display: flex; align-items: center; justify-content: space-between;
    }
    .rank-1 { border-left: 4px solid #ffd700; }
    .rank-2 { border-left: 4px solid #c0c0c0; }
    .rank-3 { border-left: 4px solid #cd7f32; }
    .footer { text-align: center; padding: 20px; color: #4a5568; font-size: 0.8rem; margin-top: 40px; border-top: 1px solid #2d3548; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.image("https://upflux.io/wp-content/uploads/2023/03/logo-upflux-white.png", width=160)
    st.markdown("---")
    integrators = load_integrators()
    integrator_names = [i["nome"] for i in integrators]
    if not integrator_names:
        st.warning("Nenhum integrador cadastrado. Va em Configuracoes.")
        selected_user = None
    else:
        selected_user = st.selectbox("Integrador", integrator_names, key="user_select")
    st.markdown("---")
    page = st.radio("Navegacao", ["Dashboard", "Historico", "Ranking", "Configuracoes"], key="nav")

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
    st.markdown("## Activity Tracker")
    st.markdown("*Controle de atividades da equipe de integracao UpFlux*")
    activities = load_activities()
    active = get_active_activities(activities)
    completed_today = [a for a in get_completed_activities(activities) if a.get("fim", "")[:10] == datetime.now().strftime("%Y-%m-%d")]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>Atividades Ativas</h3><div class="value">{len(active)}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>Concluidas Hoje</h3><div class="value">{len(completed_today)}</div></div>', unsafe_allow_html=True)
    with col3:
        alerts = len([a for a in active if get_duration_minutes(a["inicio"]) > 180])
        color = "#ff4444" if alerts > 0 else "#00d4aa"
        st.markdown(f'<div class="metric-card"><h3>Alertas</h3><div class="value" style="color: {color}">{alerts}</div></div>', unsafe_allow_html=True)
    with col4:
        online = len(set(a["integrador"] for a in active))
        st.markdown(f'<div class="metric-card"><h3>Integradores Online</h3><div class="value">{online}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    if selected_user:
        st.markdown("### Iniciar Atividade")
        user_active = get_user_active(activities, selected_user)
        if user_active:
            st.info(f"Voce ja tem {len(user_active)} atividade(s) ativa(s). Finalize antes de iniciar outra.")

        col_org, col_proc, col_desc = st.columns([2, 2, 3])
        with col_org:
            org = st.selectbox("Organizacao", sorted(ORG_PROCESS_DATA.keys()), key="org_select")
        with col_proc:
            processes = ORG_PROCESS_DATA.get(org, ["P2P"])
            proc = st.selectbox("Processo", processes, key="proc_select")
        with col_desc:
            desc = st.text_input("Descricao (opcional)", placeholder="Ex: Analise de conformidade...", key="desc_input")

        col_start, col_stop = st.columns(2)
        with col_start:
            if st.button("INICIAR", use_container_width=True, type="primary"):
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

        with col_stop:
            if user_active:
                if st.button("PARAR ATIVIDADE", use_container_width=True):
                    for act in activities:
                        if act["id"] == user_active[0]["id"]:
                            act["status"] = "completed"
                            act["fim"] = datetime.now().isoformat()
                            act["duracao_minutos"] = round(get_duration_minutes(act["inicio"], act["fim"]), 1)
                            break
                    save_activities(activities)
                    st.success("Atividade finalizada!")
                    st.rerun()

    st.markdown("---")
    st.markdown("### Atividades em Andamento")
    if not active:
        st.info("Nenhuma atividade em andamento no momento.")
    else:
        for act in active:
            dc = get_duration_class(act["inicio"])
            dur = format_duration(act["inicio"])
            mins = get_duration_minutes(act["inicio"])
            icon = "\U0001f534" if mins > 240 else ("\U0001f7e1" if mins > 180 else "\U0001f7e2")
            desc_html = f'<div style="color: #6b7585; margin-top: 5px; font-size: 0.85rem;">{act.get("descricao", "")}</div>' if act.get("descricao") else ""
            st.markdown(f'<div class="activity-card {dc}"><div style="display:flex;justify-content:space-between;align-items:center;"><div><strong style="color:#fff;font-size:1.1rem;">{act["integrador"]}</strong><span style="color:#8b95a5;margin-left:10px;">{act["organizacao"]} - {act["processo"]}</span></div><div style="text-align:right;"><span style="font-size:1.3rem;font-weight:700;color:#fff;">{icon} {dur}</span></div></div>{desc_html}</div>', unsafe_allow_html=True)

# ============================================================
# PAGINA: HISTORICO
# ============================================================
def page_historico():
    st.markdown("## Historico de Atividades")
    activities = load_activities()
    completed = get_completed_activities(activities)
    completed.sort(key=lambda x: x.get("fim", ""), reverse=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        integrators = load_integrators()
        filter_user = st.selectbox("Filtrar por integrador", ["Todos"] + [i["nome"] for i in integrators], key="hist_filter_user")
    with col2:
        filter_org = st.selectbox("Filtrar por organizacao", ["Todas"] + sorted(ORG_PROCESS_DATA.keys()), key="hist_filter_org")
    with col3:
        filter_period = st.selectbox("Periodo", ["Hoje", "Ultimos 7 dias", "Ultimos 30 dias", "Tudo"], key="hist_filter_period")

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
            st.markdown(f'<div class="activity-card"><div style="display:flex;justify-content:space-between;align-items:center;"><div><strong style="color:#fff;">{act["integrador"]}</strong><span style="color:#8b95a5;margin-left:10px;">{act["organizacao"]} - {act["processo"]}</span></div><div style="text-align:right;"><span style="color:#00d4aa;font-weight:600;">{hours:02d}h {mins:02d}m</span><div style="color:#6b7585;font-size:0.75rem;">{fim_str}</div></div></div></div>', unsafe_allow_html=True)
    else:
        st.info("Nenhuma atividade encontrada com os filtros selecionados.")

# ============================================================
# PAGINA: RANKING
# ============================================================
def page_ranking():
    st.markdown("## Ranking de Integradores")
    st.markdown("*Pontuacao: (atividades x 10) + bonus por tempo medio abaixo de 2h*")
    activities = load_activities()
    completed = get_completed_activities(activities)
    integrators = load_integrators()

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
    medals = ["\U0001f947", "\U0001f948", "\U0001f949"]
    for i, r in enumerate(ranking):
        medal = medals[i] if i < 3 else f"#{i+1}"
        rank_class = f"rank-{i+1}" if i < 3 else ""
        avg_h = int(r["media_minutos"] // 60)
        avg_m = int(r["media_minutos"] % 60)
        st.markdown(f'<div class="rank-item {rank_class}"><div style="display:flex;align-items:center;gap:15px;"><span style="font-size:1.5rem;">{medal}</span><div><strong style="color:#fff;font-size:1.1rem;">{r["nome"]}</strong><div style="color:#8b95a5;font-size:0.8rem;">{r["atividades"]} atividades - Media: {avg_h:02d}h {avg_m:02d}m</div></div></div><div style="text-align:right;"><span style="color:#00d4aa;font-size:1.5rem;font-weight:700;">{r["pontuacao"]}</span><div style="color:#8b95a5;font-size:0.75rem;">pontos</div></div></div>', unsafe_allow_html=True)

# ============================================================
# PAGINA: CONFIGURACOES
# ============================================================
def page_config():
    st.markdown("## Configuracoes")
    tab1, tab2, tab3 = st.tabs(["Integradores", "Alertas", "Integracoes"])

    with tab1:
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

    with tab2:
        st.markdown("### Configuracao de Alertas")
        config = load_config()
        config["alert_threshold_minutes"] = st.number_input("Alerta gentil (minutos)", value=config["alert_threshold_minutes"], min_value=30, max_value=600, help="Lembrete gentil apos este tempo")
        config["critical_threshold_minutes"] = st.number_input("Alerta critico (minutos)", value=config["critical_threshold_minutes"], min_value=60, max_value=720, help="Alerta no canal do time apos este tempo")
        config["jira_threshold_minutes"] = st.number_input("Criar ticket Jira (minutos)", value=config["jira_threshold_minutes"], min_value=120, max_value=1440, help="Criacao automatica de ticket no Jira")
        if st.button("Salvar Configuracoes de Alertas", key="save_alerts"):
            save_config(config)
            st.success("Configuracoes salvas!")

    with tab3:
        st.markdown("### Integracoes")
        config = load_config()
        st.markdown("**Microsoft Teams**")
        config["teams_webhook_url"] = st.text_input("Webhook URL (Incoming Webhook)", value=config.get("teams_webhook_url", ""), type="password", key="teams_webhook")
        st.markdown("**Jira**")
        config["jira_api_url"] = st.text_input("Jira API URL", value=config.get("jira_api_url", ""), placeholder="https://sua-empresa.atlassian.net", key="jira_url")
        config["jira_project_key"] = st.text_input("Project Key", value=config.get("jira_project_key", "SU"), key="jira_key")
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
    Desenvolvido por Luis Gabriel Bernardi - UpFlux Activity Tracker v1.0
</div>
""", unsafe_allow_html=True)
