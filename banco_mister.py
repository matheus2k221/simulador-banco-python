import streamlit as st
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime, date
import re
import random

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Banco Mister",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# Global CSS
# ------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: #07070f;
    background-image:
        radial-gradient(ellipse 70% 50% at 15% 5%,  rgba(212,175,55,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 85% 90%, rgba(212,175,55,0.05) 0%, transparent 60%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d18 0%, #07070f 100%);
    border-right: 1px solid rgba(212,175,55,0.18);
}

.brand-title {
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    background: linear-gradient(135deg, #d4af37 0%, #f5e27a 50%, #b8902a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin: 0;
}
.brand-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.28em;
    color: rgba(212,175,55,0.45);
    text-transform: uppercase;
    margin-top: 4px;
}
.brand-tagline {
    font-size: 0.68rem;
    color: rgba(255,255,255,0.2);
    font-style: italic;
    margin-top: 6px;
}

.card {
    background: linear-gradient(135deg, #13131e 0%, #18182a 100%);
    border: 1px solid rgba(212,175,55,0.14);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 16px;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #d4af37;
    margin-bottom: 4px;
}
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(212,175,55,0.4) 0%, transparent 100%);
    margin-bottom: 20px;
}

.balance-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    color: rgba(212,175,55,0.55);
    text-transform: uppercase;
}
.balance-value { font-family: 'DM Mono', monospace; color: #f5e27a; }

.badge-corrente {
    display:inline-block; background:rgba(100,180,255,0.1);
    border:1px solid rgba(100,180,255,0.3); color:#64b4ff;
    border-radius:20px; padding:2px 12px;
    font-size:0.68rem; font-family:'DM Mono',monospace; letter-spacing:.1em; text-transform:uppercase;
}
.badge-poupanca {
    display:inline-block; background:rgba(100,220,150,0.1);
    border:1px solid rgba(100,220,150,0.3); color:#64dc96;
    border-radius:20px; padding:2px 12px;
    font-size:0.68rem; font-family:'DM Mono',monospace; letter-spacing:.1em; text-transform:uppercase;
}

.tx-row {
    display:flex; justify-content:space-between; align-items:center;
    padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.05);
    font-size:0.82rem;
}
.tx-credit { color:#64dc96; font-family:'DM Mono',monospace; }
.tx-debit  { color:#ff6b6b; font-family:'DM Mono',monospace; }
.tx-date   { color:rgba(255,255,255,0.28); font-size:0.7rem; font-family:'DM Mono',monospace; }

div.stButton > button {
    background: linear-gradient(135deg, #d4af37, #b8902a) !important;
    color: #07070f !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em;
    transition: opacity .2s, transform .1s;
}
div.stButton > button:hover  { opacity:.85 !important; transform:translateY(-1px); }
div.stButton > button:active { transform:translateY(0); }

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background: #1a1a28 !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    color: #fff !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: #1a1a28 !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 8px !important;
}

div[data-testid="stRadio"] label { color:rgba(255,255,255,0.7) !important; }

::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:#07070f; }
::-webkit-scrollbar-thumb { background:rgba(212,175,55,0.3); border-radius:2px; }

.pix-key {
    display:inline-block;
    background: rgba(212,175,55,0.1);
    border: 1px solid rgba(212,175,55,0.3);
    border-radius: 8px;
    padding: 4px 14px;
    font-family:'DM Mono',monospace;
    font-size:0.85rem;
    color:#d4af37;
    margin: 4px 0;
}
.acct-num {
    font-family:'DM Mono',monospace;
    font-size:0.85rem;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# DOMAIN CLASSES
# ══════════════════════════════════════════════════════════════════
@dataclass
class ContaBancaria:
    numero_conta: str
    titular_cpf: str
    _saldo: float = field(default=0.0, init=False)
    historico: List[dict] = field(default_factory=list, init=False)

    def depositar(self, valor: float, descricao: str = "Deposito") -> str:
        if valor > 0:
            self._saldo += valor
            self._reg(descricao, valor)
            return f"Deposito de R$ {valor:.2f} realizado."
        return "Valor invalido."

    def _reg(self, tipo: str, valor: float):
        self.historico.append({
            "tipo": tipo, "valor": valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })

    @property
    def saldo(self): return self._saldo
    @property
    def tipo(self): return "?"


@dataclass
class ContaCorrente(ContaBancaria):
    _LIMITE: float = field(default=500.0, init=False)

    def sacar(self, valor: float, descricao: str = "Saque") -> str:
        if valor <= 0:
            return "ERRO: Valor invalido."
        if valor <= (self._saldo + self._LIMITE):
            self._saldo -= valor
            self._reg(descricao, -valor)
            return f"OK: Saque de R$ {valor:.2f} realizado."
        return "ERRO: Saldo + limite insuficiente."

    @property
    def tipo(self): return "Corrente"
    @property
    def limite(self): return self._LIMITE


@dataclass
class ContaPoupanca(ContaBancaria):
    def sacar(self, valor: float, descricao: str = "Saque") -> str:
        if valor <= 0:
            return "ERRO: Valor invalido."
        if valor <= self._saldo:
            self._saldo -= valor
            self._reg(descricao, -valor)
            return f"OK: Saque de R$ {valor:.2f} realizado."
        return "ERRO: Saldo insuficiente."

    def render(self) -> str:
        juros = self._saldo * 0.05
        self._saldo += juros
        self._reg("Rendimento 5%", juros)
        return f"OK: Rendimento de R$ {juros:.2f} aplicado."

    @property
    def tipo(self): return "Poupanca"


@dataclass
class Usuario:
    nome: str
    nascimento: date
    telefone: str
    email: str
    usuario: str
    senha: str
    cpf_fake: str
    contas: List[str] = field(default_factory=list)


# ══════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════
def _init():
    defaults = {
        "usuarios": {},
        "emails": {},
        "usernames": {},
        "banco": {},
        "conta_seq": 1,
        "logado": None,
        "pagina": "login",
        "msg": None,
        "msg_type": "info",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()


def set_msg(text, kind="success"):
    st.session_state.msg = text
    st.session_state.msg_type = kind


def show_flash():
    if st.session_state.msg:
        fn = {"success": st.success, "error": st.error,
              "info": st.info, "warning": st.warning}.get(st.session_state.msg_type, st.info)
        fn(st.session_state.msg)
        st.session_state.msg = None


def gerar_numero_conta() -> str:
    seq = st.session_state.conta_seq
    digito = random.randint(10, 99)
    st.session_state.conta_seq += 1
    return f"{seq:04d}-{digito}"


def gerar_cpf_fake() -> str:
    return f"USR{random.randint(100000, 999999)}"


def usuario_logado() -> Optional[Usuario]:
    if st.session_state.logado:
        return st.session_state.usuarios.get(st.session_state.logado)
    return None


def contas_do_usuario(u: Usuario) -> List[ContaBancaria]:
    return [st.session_state.banco[n] for n in u.contas if n in st.session_state.banco]


def calcular_idade(nascimento: date) -> int:
    hoje = date.today()
    return hoje.year - nascimento.year - (
        (hoje.month, hoje.day) < (nascimento.month, nascimento.day)
    )


def validar_telefone(tel: str) -> bool:
    digits = re.sub(r'\D', '', tel)
    return len(digits) in (10, 11)


def validar_email(email: str) -> bool:
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email))


def nome_titular(cpf: str) -> str:
    u = st.session_state.usuarios.get(cpf)
    return u.nome if u else "—"


# ══════════════════════════════════════════════════════════════════
# SHARED COMPONENTS
# ══════════════════════════════════════════════════════════════════
def card_conta_html(conta: ContaBancaria) -> str:
    sc = conta.saldo
    color = "#ff6b6b" if sc < 0 else "#f5e27a"
    badge = ("<span class='badge-corrente'>Corrente</span>"
             if isinstance(conta, ContaCorrente)
             else "<span class='badge-poupanca'>Poupanca</span>")
    extra = ""
    if isinstance(conta, ContaCorrente):
        extra = f"<div style='font-family:DM Mono;font-size:0.68rem;color:rgba(212,175,55,0.4);margin-top:2px;'>Limite fixo: R$ {conta.limite:.2f}</div>"
    nome = nome_titular(conta.titular_cpf)
    return f"""
        <div class='card' style='border-color:rgba(212,175,55,0.22);'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                <div>
                    {badge}
                    <div style='font-size:1rem;color:#fff;margin-top:8px;font-weight:500;'>{nome}</div>
                    <div class='acct-num' style='margin-top:2px;'>Conta #{conta.numero_conta}</div>
                    {extra}
                </div>
                <div style='text-align:right;'>
                    <div class='balance-label'>Saldo</div>
                    <div class='balance-value' style='font-size:1.5rem;color:{color};'>R$ {sc:,.2f}</div>
                </div>
            </div>
        </div>
    """


# ══════════════════════════════════════════════════════════════════
# PAGE: LOGIN
# ══════════════════════════════════════════════════════════════════
def page_login():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
            <div style='text-align:center;padding:36px 0 24px 0;'>
                <div style='font-size:3.2rem;'>🏦</div>
                <p class='brand-title' style='font-size:2.8rem;'>Mister</p>
                <p class='brand-sub'>Banco Digital</p>
                <p class='brand-tagline' style='color:#fff;'>"Aqui seu dinheiro some em um passe de magica"</p>
            </div>
        """, unsafe_allow_html=True)

        show_flash()

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#d4af37;font-family:Playfair Display,serif;font-size:1.15rem;margin-bottom:14px;'>Acesse sua conta</p>", unsafe_allow_html=True)

        usuario = st.text_input("Usuário", placeholder="seu_usuario", key="li_usuario")
        senha = st.text_input("Senha", type="password", placeholder="••••••••", key="li_senha")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Entrar", use_container_width=True, key="btn_entrar"):
                key = usuario.strip().lower()
                cpf = st.session_state.usernames.get(key) or st.session_state.emails.get(key)
                if not cpf:
                    set_msg("Usuário nao cadastrado.", "error")
                else:
                    u = st.session_state.usuarios[cpf]
                    if u.senha != senha:
                        set_msg("Senha incorreta.", "error")
                    else:
                        st.session_state.logado = cpf
                        st.session_state.pagina = "home"
                        set_msg(f"Bem-vindo, {u.nome.split()[0]}!", "success")
                st.rerun()
        with c2:
            if st.button("Cadastrar", use_container_width=True, key="btn_ir_cad"):
                st.session_state.pagina = "cadastro"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: CADASTRO
# ══════════════════════════════════════════════════════════════════
def page_cadastro():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
            <div style='text-align:center;padding:24px 0 18px 0;'>
                <div style='font-size:2.4rem;'>🏦</div>
                <p class='brand-title' style='font-size:2rem;'>Abrir Conta no Mister</p>
                <p class='brand-sub'>Cadastro de cliente</p>
            </div>
        """, unsafe_allow_html=True)

        show_flash()

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        nome   = st.text_input("Nome completo", placeholder="Joao da Silva Souza")
        usuario = st.text_input("Usuario", placeholder="seu_usuario")
        nasc   = st.date_input("Data de nascimento",
                              value=date(2000, 1, 1),
                              min_value=date(1920, 1, 1),
                              max_value=date.today(),
                              format="DD/MM/YYYY")
        tel    = st.text_input("Telefone", placeholder="(11) 9 9999-9999")
        email  = st.text_input("E-mail", placeholder="seu@email.com")
        senha  = st.text_input("Senha", type="password", placeholder="Minimo 6 caracteres")
        senha2 = st.text_input("Confirmar senha", type="password", placeholder="Repita a senha")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Criar Cadastro", use_container_width=True, key="btn_criar"):
                erros = []
                nome_s = nome.strip()
                usuario_s = usuario.strip()
                if len(nome_s.split()) < 2:
                    erros.append("Informe nome e sobrenome.")
                if not usuario_s:
                    erros.append("Informe um nome de usuário.")
                if " " in usuario_s:
                    erros.append("Usuario nao pode conter espacos.")
                if usuario_s.lower() in st.session_state.usernames:
                    erros.append("Usuario ja cadastrado.")
                if calcular_idade(nasc) < 18:
                    erros.append("Voce precisa ter pelo menos 18 anos.")
                if not validar_telefone(tel):
                    erros.append("Telefone invalido.")
                if not validar_email(email):
                    erros.append("E-mail invalido.")
                if email.strip().lower() in st.session_state.emails:
                    erros.append("E-mail ja cadastrado.")
                if len(senha) < 6:
                    erros.append("Senha deve ter pelo menos 6 caracteres.")
                if senha != senha2:
                    erros.append("As senhas nao coincidem.")

                if erros:
                    set_msg(" | ".join(erros), "error")
                    st.rerun()
                else:
                    cpf = gerar_cpf_fake()
                    u = Usuario(
                        nome=nome_s, nascimento=nasc,
                        telefone=tel.strip(), email=email.strip().lower(),
                        usuario=usuario_s, senha=senha, cpf_fake=cpf,
                    )
                    st.session_state.usuarios[cpf] = u
                    st.session_state.emails[email.strip().lower()] = cpf
                    st.session_state.usernames[usuario_s.lower()] = cpf
                    st.session_state.logado = cpf
                    st.session_state.pagina = "home"
                    set_msg(f"Cadastro realizado! Bem-vindo, {nome_s.split()[0]}!", "success")
                    st.rerun()
        with c2:
            if st.button("Voltar ao Login", use_container_width=True, key="btn_voltar"):
                st.session_state.pagina = "login"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════
def render_sidebar(u: Usuario) -> str:
    with st.sidebar:
        st.markdown(f"""
            <div style='padding:18px 0 14px 0;text-align:center;'>
                <div style='font-size:2.2rem;'>🏦</div>
                <p class='brand-title' style='font-size:1.9rem;'>Mister</p>
                <p class='brand-sub'>Banco Digital</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style='background:rgba(212,175,55,0.07);border:1px solid rgba(212,175,55,0.15);
                 border-radius:12px;padding:12px 14px;margin-bottom:16px;'>
                <div style='font-size:0.62rem;color:rgba(212,175,55,0.5);letter-spacing:.15em;text-transform:uppercase;'>Ola,</div>
                <div style='color:#fff;font-size:0.95rem;font-weight:600;margin-top:2px;'>{u.nome.split()[0]} {u.nome.split()[-1]}</div>
                <div style='font-family:DM Mono;font-size:0.65rem;color:rgba(255,255,255,0.25);margin-top:2px;'>{u.cpf_fake}</div>
            </div>
        """, unsafe_allow_html=True)

        pagina = st.radio("Menu", [
            "🏠  Inicio",
            "🏦  Minhas Contas",
            "➕  Abrir Conta",
            "💰  Deposito",
            "💸  Saque",
            "🔄  Transferencia",
            "📱  PIX",
            "📊  Extrato",
        ], label_visibility="collapsed")

        st.markdown("<hr style='border-color:rgba(212,175,55,0.1);margin:14px 0;'>", unsafe_allow_html=True)

        total = sum(c.saldo for c in contas_do_usuario(u))
        st.markdown(f"""
            <div style='padding:8px 0;'>
                <div class='balance-label'>Patrimonio total</div>
                <div style='font-family:DM Mono;color:#d4af37;font-size:1.1rem;'>R$ {total:,.2f}</div>
                <div class='balance-label' style='margin-top:8px;'>Contas ativas</div>
                <div style='font-family:DM Mono;color:#fff;font-size:1rem;'>{len(u.contas)}</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Sair", use_container_width=True, key="btn_sair"):
            st.session_state.logado = None
            st.session_state.pagina = "login"
            st.rerun()

        return pagina


# ══════════════════════════════════════════════════════════════════
# PAGES (logado)
# ══════════════════════════════════════════════════════════════════

def page_home(u: Usuario):
    st.markdown('<p class="brand-title" style="font-size:1.8rem;">Inicio</p>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    show_flash()

    contas = contas_do_usuario(u)
    if not contas:
        st.markdown("""
            <div class='card' style='text-align:center;padding:48px;'>
                <div style='font-size:2.8rem;margin-bottom:12px;'>🏦</div>
                <div style='color:rgba(255,255,255,0.4);font-size:0.92rem;'>
                    Voce ainda nao tem contas.<br>
                    Use <b style='color:#d4af37;'>Abrir Conta</b> no menu para criar a sua primeira.
                </div>
            </div>
        """, unsafe_allow_html=True)
        return

    correntes = [c for c in contas if isinstance(c, ContaCorrente)]
    poupancas = [c for c in contas if isinstance(c, ContaPoupanca)]
    total = sum(c.saldo for c in contas)

    c1, c2, c3 = st.columns(3)
    for col, label, val, color in [
        (c1, "Saldo Total", f"R$ {total:,.2f}", "#f5e27a"),
        (c2, "Contas Correntes", str(len(correntes)), "#64b4ff"),
        (c3, "Poupancas", str(len(poupancas)), "#64dc96"),
    ]:
        with col:
            st.markdown(f"""
                <div class='card'>
                    <div class='balance-label'>{label}</div>
                    <div class='balance-value' style='font-size:1.6rem;color:{color};'>{val}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title" style="font-size:1.15rem;">Suas Contas</p>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    for c in contas:
        st.markdown(card_conta_html(c), unsafe_allow_html=True)


def page_minhas_contas(u: Usuario):
    st.markdown('<p class="brand-title" style="font-size:1.8rem;">Minhas Contas</p>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    show_flash()
    contas = contas_do_usuario(u)
    if not contas:
        st.info("Voce nao tem contas. Use Abrir Conta para criar.")
        return
    for c in contas:
        st.markdown(card_conta_html(c), unsafe_allow_html=True)


def page_abrir_conta(u: Usuario):
    st.markdown('<p class="brand-title" style="font-size:1.8rem;">Abrir Nova Conta</p>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    show_flash()

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    tipo = st.selectbox("Tipo de conta", ["Corrente", "Poupanca"])

    if tipo == "Corrente":
        st.markdown("""
            <div style='background:rgba(100,180,255,0.06);border:1px solid rgba(100,180,255,0.2);
                 border-radius:10px;padding:10px 14px;margin:8px 0;font-size:0.82rem;color:#64b4ff;'>
            Conta Corrente inclui <b>limite de R$ 500,00</b>. .
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background:rgba(100,220,150,0.06);border:1px solid rgba(100,220,150,0.2);
                 border-radius:10px;padding:10px 14px;margin:8px 0;font-size:0.82rem;color:#64dc96;'>
            Poupanca rende <b>5% ao mes</b> sobre o saldo. Use a opcao Extrato para aplicar.
            </div>
        """, unsafe_allow_html=True)

    dep = st.number_input("Deposito inicial (R$)", min_value=0.0, value=0.0, step=100.0, format="%.2f")

    if st.button("Criar Conta", key="btn_criar_conta"):
        num = gerar_numero_conta()
        if tipo == "Corrente":
            nova = ContaCorrente(numero_conta=num, titular_cpf=u.cpf_fake)
        else:
            nova = ContaPoupanca(numero_conta=num, titular_cpf=u.cpf_fake)
        if dep > 0:
            nova.depositar(dep, "Deposito inicial")
        st.session_state.banco[num] = nova
        u.contas.append(num)
        set_msg(f"Conta {num} ({tipo}) aberta com sucesso!", "success")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def _sel_conta(u: Usuario, label: str, key: str):
    """Selectbox de conta do usuario, retorna ContaBancaria ou None."""
    contas = contas_do_usuario(u)
    if not contas:
        st.info("Voce nao tem contas.")
        return None
    opcoes = {c.numero_conta: c for c in contas}
    sel = st.selectbox(label, list(opcoes.keys()),
                       format_func=lambda x: f"#{x} ({opcoes[x].tipo}) — Saldo: R$ {opcoes[x].saldo:,.2f}",
                       key=key)
    return opcoes[sel]


def page_deposito(u: Usuario):
    st.markdown('<p class="brand-title" style="font-size:1.8rem;">Deposito</p>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    show_flash()

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    conta = _sel_conta(u, "Conta de destino", "dep_conta")
    if conta:
        valor = st.number_input("Valor (R$)", min_value=0.01, value=100.0, step=50.0, format="%.2f", key="dep_val")
        if st.button("Confirmar Deposito", key="btn_dep"):
            msg = conta.depositar(valor)
            set_msg(f"Deposito de R$ {valor:.2f} realizado!", "success") if not msg.startswith("Valor") else set_msg(msg, "error")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def page_saque(u: Usuario):
    st.markdown('<p class="brand-title" style="font-size:1.8rem;">Saque</p>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    show_flash()

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    conta = _sel_conta(u, "Conta de origem", "saq_conta")
    if conta:
        if isinstance(conta, ContaCorrente):
            disp = conta.saldo + conta.limite
            st.markdown(f"<span style='font-size:0.78rem;color:rgba(100,180,255,0.8);'>Disponivel (saldo + limite): <b>R$ {disp:,.2f}</b></span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='font-size:0.78rem;color:rgba(100,220,150,0.8);'>Disponivel: <b>R$ {conta.saldo:,.2f}</b></span>", unsafe_allow_html=True)

        valor = st.number_input("Valor (R$)", min_value=0.01, value=50.0, step=10.0, format="%.2f", key="saq_val")
        if st.button("Confirmar Saque", key="btn_saq"):
            msg = conta.sacar(valor)
            if msg.startswith("OK"):
                set_msg(f"Saque de R$ {valor:.2f} realizado!", "success")
            else:
                set_msg(msg.replace("ERRO: ", ""), "error")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def page_transferencia(u: Usuario):
    st.markdown('<p class="brand-title" style="font-size:1.8rem;">Transferencia</p>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    show_flash()

    minhas = contas_do_usuario(u)
    todas  = st.session_state.banco

    if not minhas:
        st.info("Voce nao tem contas.")
        return

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    opc_orig = {c.numero_conta: c for c in minhas}
    sel_orig = st.selectbox("Conta de origem (sua)", list(opc_orig.keys()),
                            format_func=lambda x: f"#{x} ({opc_orig[x].tipo}) — R$ {opc_orig[x].saldo:,.2f}",
                            key="trf_orig")
    origem = opc_orig[sel_orig]

    destinos = {k: v for k, v in todas.items() if k != sel_orig}
    if not destinos:
        st.warning("Nao ha outras contas disponiveis.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    def fmt_dest(x):
        c = destinos[x]
        return f"#{x} ({c.tipo}) — {nome_titular(c.titular_cpf)}"

    sel_dest = st.selectbox("Conta de destino", list(destinos.keys()), format_func=fmt_dest, key="trf_dest")
    destino = destinos[sel_dest]

    if isinstance(origem, ContaCorrente):
        disp = origem.saldo + origem.limite
        st.markdown(f"<span style='font-size:0.78rem;color:rgba(100,180,255,0.8);'>Disponivel: <b>R$ {disp:,.2f}</b></span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span style='font-size:0.78rem;color:rgba(100,220,150,0.8);'>Disponivel: <b>R$ {origem.saldo:,.2f}</b></span>", unsafe_allow_html=True)

    valor = st.number_input("Valor (R$)", min_value=0.01, value=100.0, step=50.0, format="%.2f", key="trf_val")
    nd = nome_titular(destino.titular_cpf)

    st.markdown(f"""
        <div style='background:rgba(212,175,55,0.05);border:1px solid rgba(212,175,55,0.15);
             border-radius:10px;padding:10px 14px;margin:10px 0;font-size:0.82rem;'>
            Transferindo <b style='color:#d4af37;'>R$ {valor:,.2f}</b>
            para <b style='color:#fff;'>{nd}</b>
            (Conta #{destino.numero_conta} — {destino.tipo})
        </div>
    """, unsafe_allow_html=True)

    if st.button("Confirmar Transferencia", key="btn_trf"):
        msg = origem.sacar(valor, f"Transf. para #{destino.numero_conta}")
        if msg.startswith("OK"):
            destino.depositar(valor, f"Transf. de #{origem.numero_conta}")
            set_msg(f"Transferencia de R$ {valor:.2f} para {nd} realizada!", "success")
        else:
            set_msg(msg.replace("ERRO: ", ""), "error")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def page_pix(u: Usuario):
    st.markdown('<p class="brand-title" style="font-size:1.8rem;">PIX</p>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    show_flash()

    tab_env, tab_rec = st.tabs(["Enviar PIX", "Receber / Minhas Chaves"])

    with tab_env:
        minhas = contas_do_usuario(u)
        if not minhas:
            st.info("Voce nao tem contas.")
        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            opc = {c.numero_conta: c for c in minhas}
            sel = st.selectbox("Debitar de", list(opc.keys()),
                               format_func=lambda x: f"#{x} ({opc[x].tipo}) — R$ {opc[x].saldo:,.2f}",
                               key="pix_orig")
            origem = opc[sel]

            chave = st.text_input("Chave PIX (email, telefone ou numero de conta)", placeholder="email@exemplo.com", key="pix_chave")
            valor = st.number_input("Valor (R$)", min_value=0.01, value=50.0, step=10.0, format="%.2f", key="pix_val")

            def resolver_pix(ch: str):
                ch = ch.strip().lower()
                # por email
                cpf_t = st.session_state.emails.get(ch)
                if cpf_t and st.session_state.usuarios[cpf_t].contas:
                    uu = st.session_state.usuarios[cpf_t]
                    return st.session_state.banco[uu.contas[0]], uu.nome
                # por numero de conta (com ou sem #)
                num = ch.lstrip('#')
                if num in st.session_state.banco:
                    c = st.session_state.banco[num]
                    return c, nome_titular(c.titular_cpf)
                # por telefone
                digits_in = re.sub(r'\D', '', ch)
                for cpf_t2, uu2 in st.session_state.usuarios.items():
                    if digits_in and re.sub(r'\D', '', uu2.telefone) == digits_in and uu2.contas:
                        return st.session_state.banco[uu2.contas[0]], uu2.nome
                return None, None

            if chave.strip():
                conta_dest, nome_dest = resolver_pix(chave)
                if conta_dest and conta_dest.numero_conta != sel:
                    st.markdown(f"""
                        <div style='background:rgba(100,220,150,0.06);border:1px solid rgba(100,220,150,0.2);
                             border-radius:10px;padding:10px 14px;margin:8px 0;font-size:0.82rem;color:#64dc96;'>
                            Destinatario: <b>{nome_dest}</b> — Conta #{conta_dest.numero_conta} ({conta_dest.tipo})
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("Enviar PIX", key="btn_pix_env"):
                        msg = origem.sacar(valor, f"PIX para {nome_dest}")
                        if msg.startswith("OK"):
                            conta_dest.depositar(valor, f"PIX de {u.nome.split()[0]}")
                            set_msg(f"PIX de R$ {valor:.2f} enviado para {nome_dest}!", "success")
                        else:
                            set_msg(msg.replace("ERRO: ", ""), "error")
                        st.rerun()
                elif conta_dest and conta_dest.numero_conta == sel:
                    st.warning("A conta de destino nao pode ser a mesma de origem.")
                else:
                    st.markdown("""
                        <div style='background:rgba(255,100,100,0.06);border:1px solid rgba(255,100,100,0.2);
                             border-radius:10px;padding:10px 14px;margin:8px 0;font-size:0.82rem;color:#ff9a9a;'>
                            Chave PIX nao encontrada.
                        </div>
                    """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    with tab_rec:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<span style='color:rgba(255,255,255,0.45);font-size:0.82rem;'>Suas chaves PIX registradas automaticamente:</span>", unsafe_allow_html=True)
        contas_nums = "".join(f"<div class='pix-key'>🏦 #{n}</div>" for n in u.contas) if u.contas else "<span style='color:rgba(255,255,255,0.3);font-size:0.8rem;'>Nenhuma conta ainda.</span>"
        st.markdown(f"""
            <div style='margin-top:14px;'>
                <div class='balance-label'>E-mail</div>
                <div class='pix-key'>✉️ {u.email}</div>
            </div>
            <div style='margin-top:12px;'>
                <div class='balance-label'>Telefone</div>
                <div class='pix-key'>📱 {u.telefone}</div>
            </div>
            <div style='margin-top:12px;'>
                <div class='balance-label'>Contas</div>
                {contas_nums}
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def page_extrato(u: Usuario):
    st.markdown('<p class="brand-title" style="font-size:1.8rem;">Extrato</p>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    show_flash()

    contas = contas_do_usuario(u)
    if not contas:
        st.info("Voce nao tem contas.")
        return

    opc = {c.numero_conta: c for c in contas}
    sel = st.selectbox("Selecione a conta", list(opc.keys()),
                       format_func=lambda x: f"#{x} ({opc[x].tipo}) — R$ {opc[x].saldo:,.2f}",
                       key="ext_sel")
    conta = opc[sel]

    st.markdown(card_conta_html(conta), unsafe_allow_html=True)

    if isinstance(conta, ContaPoupanca):
        prev = conta.saldo * 0.05
        st.markdown(f"""
            <div style='background:rgba(100,220,150,0.06);border:1px solid rgba(100,220,150,0.2);
                 border-radius:10px;padding:12px 16px;margin-bottom:12px;font-size:0.82rem;color:#64dc96;'>
            📈 Rendimento disponivel: <b>+R$ {prev:.2f}</b> (5% sobre saldo)
            </div>
        """, unsafe_allow_html=True)
        if st.button("Aplicar Rendimento", key="btn_render"):
            msg = conta.render()
            set_msg(msg.replace("OK: ", ""), "success")
            st.rerun()

    st.markdown('<p class="section-title" style="font-size:1.1rem;margin-top:20px;">Historico</p>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if not conta.historico:
        st.markdown("<span style='color:rgba(255,255,255,0.3);font-size:0.85rem;'>Sem transacoes ainda.</span>", unsafe_allow_html=True)
        return

    rows = ""
    for tx in reversed(conta.historico):
        v = tx["valor"]
        cls  = "tx-credit" if v >= 0 else "tx-debit"
        sign = "+" if v >= 0 else ""
        rows += f"""
            <div class='tx-row'>
                <div><span style='color:rgba(255,255,255,0.85);'>{tx['tipo']}</span></div>
                <div style='display:flex;gap:20px;align-items:center;'>
                    <span class='tx-date'>{tx['data']}</span>
                    <span class='{cls}'>{sign}R$ {abs(v):,.2f}</span>
                </div>
            </div>
        """
    st.markdown(f"<div class='card'>{rows}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════
pg = st.session_state.pagina

if pg == "login":
    page_login()
elif pg == "cadastro":
    page_cadastro()
else:
    u = usuario_logado()
    if not u:
        st.session_state.pagina = "login"
        st.rerun()

    menu = render_sidebar(u)

    if   menu == "🏠  Inicio":         page_home(u)
    elif menu == "🏦  Minhas Contas":  page_minhas_contas(u)
    elif menu == "➕  Abrir Conta":    page_abrir_conta(u)
    elif menu == "💰  Deposito":       page_deposito(u)
    elif menu == "💸  Saque":          page_saque(u)
    elif menu == "🔄  Transferencia":  page_transferencia(u)
    elif menu == "📱  PIX":            page_pix(u)
    elif menu == "📊  Extrato":        page_extrato(u)