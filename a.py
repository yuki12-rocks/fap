#!/usr/bin/env python3
"""
Unix Permission Calculator & Simulator
Deployable on Streamlit Cloud — no local filesystem access needed.
"""
 
import streamlit as st
 
# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Unix Permission Calculator",
    page_icon="🔐",
    layout="wide"
)
 
# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');
 
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}
 
/* Dark industrial theme */
.stApp {
    background: #0d0d0f;
    color: #e8e8e8;
}
 
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
}
 
/* Permission bit card */
.bit-card {
    background: #1a1a1f;
    border: 1px solid #2a2a32;
    border-radius: 12px;
    padding: 18px 14px;
    text-align: center;
    transition: all 0.2s ease;
}
 
.bit-card.active {
    background: #1a2a1a;
    border-color: #4ade80;
    box-shadow: 0 0 20px rgba(74,222,128,0.15);
}
 
.bit-card.inactive {
    background: #1a1a1f;
    border-color: #2a2a32;
    opacity: 0.5;
}
 
/* Octal display */
.octal-display {
    font-family: 'JetBrains Mono', monospace;
    font-size: 4rem;
    font-weight: 700;
    color: #4ade80;
    text-align: center;
    letter-spacing: 0.15em;
    padding: 20px;
    background: #0a1a0a;
    border: 2px solid #4ade80;
    border-radius: 16px;
    text-shadow: 0 0 30px rgba(74,222,128,0.4);
}
 
/* Symbolic display */
.symbolic-display {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #a78bfa;
    text-align: center;
    letter-spacing: 0.2em;
    padding: 16px;
    background: #0f0a1a;
    border: 2px solid #a78bfa;
    border-radius: 16px;
    text-shadow: 0 0 20px rgba(167,139,250,0.3);
}
 
/* Permission group box */
.perm-group {
    background: #13131a;
    border: 1px solid #252530;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
}
 
.perm-group-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 12px;
}
 
/* Warning boxes */
.warn-box {
    background: #1a1200;
    border-left: 4px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.9rem;
    color: #fcd34d;
}
 
.danger-box {
    background: #1a0000;
    border-left: 4px solid #ef4444;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.9rem;
    color: #fca5a5;
}
 
.safe-box {
    background: #001a08;
    border-left: 4px solid #4ade80;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.9rem;
    color: #86efac;
}
 
/* Common presets */
.preset-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    padding: 4px 10px;
    border-radius: 6px;
    margin: 2px;
    background: #1e1e28;
    border: 1px solid #3a3a4a;
    color: #a0a0b8;
}
 
/* Section headers */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    border-bottom: 1px solid #252530;
    padding-bottom: 8px;
    margin: 24px 0 16px 0;
}
 
/* Chmod command */
.chmod-cmd {
    font-family: 'JetBrains Mono', monospace;
    background: #0a0a12;
    border: 1px solid #2a2a40;
    border-radius: 10px;
    padding: 14px 20px;
    font-size: 1.1rem;
    color: #67e8f9;
    display: block;
    margin: 8px 0;
}
 
/* Tab styling override */
.stTabs [data-baseweb="tab-list"] {
    background: #13131a;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
}
 
/* Metric override */
[data-testid="metric-container"] {
    background: #13131a;
    border: 1px solid #252530;
    border-radius: 12px;
    padding: 16px;
}
 
.stCheckbox label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
}
</style>
""", unsafe_allow_html=True)
 
 
# ─── Helper Functions ─────────────────────────────────────────────────────────
 
def bits_to_octal(r, w, x):
    return (4 if r else 0) + (2 if w else 0) + (1 if x else 0)
 
def octal_to_bits(n):
    return bool(n & 4), bool(n & 2), bool(n & 1)
 
def bits_to_sym(r, w, x):
    return f"{'r' if r else '-'}{'w' if w else '-'}{'x' if x else '-'}"
 
def full_symbolic(ftype, or_, ow, ox, gr, gw, gx, otr, otw, otx):
    t = "d" if ftype == "Directory" else "-"
    return t + bits_to_sym(or_, ow, ox) + bits_to_sym(gr, gw, gx) + bits_to_sym(otr, otw, otx)
 
def octal_str(or_, ow, ox, gr, gw, gx, otr, otw, otx):
    return f"{bits_to_octal(or_, ow, ox)}{bits_to_octal(gr, gw, gx)}{bits_to_octal(otr, otw, otx)}"
 
def get_warnings(ftype, or_, ow, ox, gr, gw, gx, otr, otw, otx):
    warnings = []
    dangers = []
 
    if otw:
        dangers.append("World-writable: **anyone** on the system can modify or delete this.")
    if otr and ftype == "File":
        warnings.append("World-readable: anyone can read the contents of this file.")
    if not or_:
        warnings.append("Owner cannot read their own file — unusual and potentially problematic.")
    if ox and ftype == "File":
        warnings.append("Owner-executable: this file can be run as a program by the owner.")
    if gw:
        warnings.append("Group-writable: any member of the file's group can modify it.")
    if otx:
        warnings.append("World-executable: anyone can execute this file or traverse this directory.")
    if or_ and ow and ox and gr and gw and gx and otr and otw and otx:
        dangers.append("Permission 777: completely open — this is almost never safe.")
    if ftype == "Directory" and otw and not (bits_to_octal(otr, otw, otx) == 1):
        dangers.append("World-writable directory without sticky bit — users can delete each other's files!")
 
    return warnings, dangers
 
def get_use_case(octal):
    cases = {
        "644": "Standard file — owner reads/writes, everyone else reads. Default for web files.",
        "755": "Standard directory or executable — owner full access, everyone can read/execute.",
        "600": "Private file — only owner can read/write. Good for SSH keys, config files.",
        "700": "Private directory — only owner can access. Good for personal scripts.",
        "777": "⚠️ Fully open — dangerous! Only use for testing, never in production.",
        "640": "Group-readable file — owner writes, group reads. Common for shared configs.",
        "750": "Group-accessible directory — owner full, group can read/execute.",
        "444": "Read-only for all — no one can write. Good for shared reference files.",
        "400": "Owner read-only — very restrictive. Common for private keys (chmod 400 id_rsa).",
        "664": "Collaborative file — owner and group can write, others read.",
        "775": "Collaborative directory — owner and group full access, others read/execute.",
        "666": "⚠️ World-readable and writable — rarely appropriate.",
        "711": "Execute-only directory for others — they can access if they know the path.",
        "chmod +x": "Makes a file executable.",
    }
    return cases.get(octal, None)
 
 
# ─── Session State Init ────────────────────────────────────────────────────────
defaults = {
    "owner_r": True, "owner_w": True, "owner_x": False,
    "group_r": True, "group_w": False, "group_x": False,
    "others_r": True, "others_w": False, "others_x": False,
    "ftype": "File",
    "octal_input": "644",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v
 
 
def apply_octal(octal_str_val):
    """Parse a 3-digit octal string and update session state bits."""
    try:
        digits = octal_str_val.strip().lstrip("0o").zfill(3)
        if len(digits) != 3 or not all(c in "01234567" for c in digits):
            return False
        o, g, t = int(digits[0]), int(digits[1]), int(digits[2])
        st.session_state.owner_r, st.session_state.owner_w, st.session_state.owner_x = octal_to_bits(o)
        st.session_state.group_r, st.session_state.group_w, st.session_state.group_x = octal_to_bits(g)
        st.session_state.others_r, st.session_state.others_w, st.session_state.others_x = octal_to_bits(t)
        return True
    except Exception:
        return False
 
 
def apply_symbolic(sym):
    """Parse symbolic like rwxr-xr-- and update session state."""
    try:
        sym = sym.strip()
        # Accept with or without leading file type char
        if len(sym) == 10:
            sym = sym[1:]
        if len(sym) != 9:
            return False
        valid = set("rwx-")
        if not all(c in valid for c in sym):
            return False
        st.session_state.owner_r = sym[0] == 'r'
        st.session_state.owner_w = sym[1] == 'w'
        st.session_state.owner_x = sym[2] == 'x'
        st.session_state.group_r = sym[3] == 'r'
        st.session_state.group_w = sym[4] == 'w'
        st.session_state.group_x = sym[5] == 'x'
        st.session_state.others_r = sym[6] == 'r'
        st.session_state.others_w = sym[7] == 'w'
        st.session_state.others_x = sym[8] == 'x'
        return True
    except Exception:
        return False
 
 
# ─── Title ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 10px 0 30px 0;'>
    <div style='font-family: Syne, sans-serif; font-size: 2.8rem; font-weight: 800;
                letter-spacing: -0.03em; line-height: 1.1;'>
        🔐 Unix Permission <span style='color: #4ade80;'>Calculator</span>
    </div>
    <div style='color: #666; font-size: 1rem; margin-top: 8px; font-family: JetBrains Mono, monospace;'>
        Build, decode & understand file permissions — deployable anywhere
    </div>
</div>
""", unsafe_allow_html=True)
 
# ─── Main Layout ──────────────────────────────────────────────────────────────
left, right = st.columns([1.1, 0.9], gap="large")
 
with left:
    # ── Mode Tabs ──────────────────────────────────────────────────────────────
    tab_build, tab_decode, tab_presets = st.tabs([
        "🔧 Build Permissions",
        "🔍 Decode Permission",
        "📚 Common Presets"
    ])
 
    # ── Tab 1: Build with checkboxes ───────────────────────────────────────────
    with tab_build:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
 
        ftype_col, _ = st.columns([1, 2])
        with ftype_col:
            st.session_state.ftype = st.selectbox(
                "File Type", ["File", "Directory"],
                index=0 if st.session_state.ftype == "File" else 1,
                key="ftype_select"
            )
 
        st.markdown("<div class='section-header'>Toggle Permissions</div>", unsafe_allow_html=True)
 
        for group, key_prefix, color, icon in [
            ("Owner",  "owner",  "#4ade80", "👤"),
            ("Group",  "group",  "#a78bfa", "👥"),
            ("Others", "others", "#fb923c", "🌐"),
        ]:
            st.markdown(f"""
            <div style='font-family: Syne, sans-serif; font-weight: 700; font-size: 0.8rem;
                        letter-spacing: 0.12em; text-transform: uppercase; color: {color};
                        margin: 16px 0 8px 0;'>
                {icon} {group}
            </div>
            """, unsafe_allow_html=True)
 
            c1, c2, c3 = st.columns(3)
            with c1:
                st.session_state[f"{key_prefix}_r"] = st.checkbox(
                    "Read (r)", value=st.session_state[f"{key_prefix}_r"],
                    key=f"cb_{key_prefix}_r"
                )
            with c2:
                st.session_state[f"{key_prefix}_w"] = st.checkbox(
                    "Write (w)", value=st.session_state[f"{key_prefix}_w"],
                    key=f"cb_{key_prefix}_w"
                )
            with c3:
                st.session_state[f"{key_prefix}_x"] = st.checkbox(
                    "Execute (x)", value=st.session_state[f"{key_prefix}_x"],
                    key=f"cb_{key_prefix}_x"
                )
 
    # ── Tab 2: Decode input ────────────────────────────────────────────────────
    with tab_decode:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown("Enter an octal (e.g. `755`) or symbolic (e.g. `rwxr-xr-x`) permission:")
 
        decode_input = st.text_input(
            "Permission string",
            placeholder="755  or  rwxr-xr-x  or  -rwxr-xr-x",
            label_visibility="collapsed",
            key="decode_input"
        )
 
        if st.button("🔍 Decode", type="primary", use_container_width=True):
            val = decode_input.strip()
            if val:
                # Try octal first
                clean = val.lstrip("0o")
                if clean.isdigit() and len(clean) <= 3 and all(c in "01234567" for c in clean):
                    if apply_octal(clean.zfill(3)):
                        st.success(f"✅ Decoded octal `{clean.zfill(3)}`")
                    else:
                        st.error("Invalid octal value. Use digits 0–7 only.")
                else:
                    # Try symbolic
                    if apply_symbolic(val):
                        st.success(f"✅ Decoded symbolic `{val}`")
                    else:
                        st.error("Invalid format. Use octal like `755` or symbolic like `rwxr-xr-x`.")
 
        st.markdown("<br>**Examples to try:**", unsafe_allow_html=True)
        ex_cols = st.columns(4)
        for col, ex in zip(ex_cols, ["755", "644", "600", "777"]):
            if col.button(ex, use_container_width=True, key=f"ex_{ex}"):
                apply_octal(ex)
                st.rerun()
 
    # ── Tab 3: Presets ─────────────────────────────────────────────────────────
    with tab_presets:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
 
        presets = [
            ("644", "File", "Standard file",         "Default for most files. Owner edits, everyone reads."),
            ("755", "Dir",  "Standard directory",    "Default for directories and executables."),
            ("600", "File", "Private file",           "SSH keys, secrets. Only owner reads/writes."),
            ("700", "Dir",  "Private directory",      "Only owner can enter. Good for personal scripts."),
            ("777", "Both", "⚠️ Fully open",           "Dangerous. Everything allowed for everyone."),
            ("640", "File", "Group-readable",         "Owner writes, group reads. Shared configs."),
            ("750", "Dir",  "Group-accessible dir",  "Owner full, group can browse."),
            ("444", "File", "Read-only",              "Nobody can write. Reference/shared files."),
            ("400", "File", "Owner read-only",        "Very restrictive. Private key standard."),
            ("664", "File", "Collaborative file",     "Owner + group write, others read."),
            ("775", "Dir",  "Collaborative dir",      "Owner + group full access."),
        ]
 
        for octal, ftype, name, desc in presets:
            c1, c2 = st.columns([1, 3])
            with c1:
                if st.button(f"`{octal}`", key=f"preset_{octal}", use_container_width=True):
                    apply_octal(octal)
                    st.session_state.ftype = "Directory" if ftype == "Dir" else "File"
                    st.rerun()
            with c2:
                st.markdown(f"""
                <div style='padding: 6px 0;'>
                    <span style='font-weight:700; color:#e8e8e8;'>{name}</span>
                    <span style='color:#666; font-size:0.85rem; margin-left:8px;'>[{ftype}]</span><br>
                    <span style='color:#888; font-size:0.85rem;'>{desc}</span>
                </div>
                """, unsafe_allow_html=True)
 
 
# ─── Right Panel: Live Results ────────────────────────────────────────────────
with right:
    # Read current state
    or_ = st.session_state.owner_r
    ow  = st.session_state.owner_w
    ox  = st.session_state.owner_x
    gr  = st.session_state.group_r
    gw  = st.session_state.group_w
    gx  = st.session_state.group_x
    otr = st.session_state.others_r
    otw = st.session_state.others_w
    otx = st.session_state.others_x
    ftype = st.session_state.get("ftype_select", st.session_state.ftype)
 
    oct_val = octal_str(or_, ow, ox, gr, gw, gx, otr, otw, otx)
    sym_val = full_symbolic(ftype, or_, ow, ox, gr, gw, gx, otr, otw, otx)
 
    st.markdown("<div class='section-header'>Live Result</div>", unsafe_allow_html=True)
 
    st.markdown(f"<div class='octal-display'>{oct_val}</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='symbolic-display'>{sym_val}</div>", unsafe_allow_html=True)
 
    # chmod commands
    st.markdown("<div class='section-header'>chmod Commands</div>", unsafe_allow_html=True)
    st.markdown(f"<code class='chmod-cmd'>chmod {oct_val} filename</code>", unsafe_allow_html=True)
    st.markdown(f"<code class='chmod-cmd'>chmod {oct_val} /path/to/file</code>", unsafe_allow_html=True)
 
    # Use case hint
    use_case = get_use_case(oct_val)
    if use_case:
        st.markdown(f"""
        <div style='background:#0f1a10; border:1px solid #2a3a2a; border-radius:10px;
                    padding:12px 16px; margin:8px 0; font-size:0.9rem; color:#86efac;'>
            💡 {use_case}
        </div>
        """, unsafe_allow_html=True)
 
    # Permission breakdown table
    st.markdown("<div class='section-header'>Breakdown</div>", unsafe_allow_html=True)
 
    header = st.columns([2, 1, 1, 1])
    header[0].markdown("**Who**")
    header[1].markdown("**Read**")
    header[2].markdown("**Write**")
    header[3].markdown("**Execute**")
 
    for label, r, w, x, octal_digit in [
        ("👤 Owner",  or_, ow, ox, bits_to_octal(or_, ow, ox)),
        ("👥 Group",  gr,  gw, gx, bits_to_octal(gr, gw, gx)),
        ("🌐 Others", otr, otw, otx, bits_to_octal(otr, otw, otx)),
    ]:
        row = st.columns([2, 1, 1, 1])
        row[0].markdown(f"{label} `({octal_digit})`")
        row[1].write("✅" if r else "❌")
        row[2].write("✅" if w else "❌")
        row[3].write("✅" if x else "❌")
 
    # Security analysis
    st.markdown("<div class='section-header'>Security Analysis</div>", unsafe_allow_html=True)
    warnings, dangers = get_warnings(ftype, or_, ow, ox, gr, gw, gx, otr, otw, otx)
 
    if not warnings and not dangers:
        st.markdown("<div class='safe-box'>✅ No security issues — this is a safe permission set.</div>", unsafe_allow_html=True)
    for d in dangers:
        st.markdown(f"<div class='danger-box'>🚨 {d}</div>", unsafe_allow_html=True)
    for w in warnings:
        st.markdown(f"<div class='warn-box'>⚠️ {w}</div>", unsafe_allow_html=True)
 
    # Visual bars
    st.markdown("<div class='section-header'>Visual</div>", unsafe_allow_html=True)
    v1, v2, v3 = st.columns(3)
    for col, label, icon, color, r, w, x in [
        (v1, "Owner",  "👤", "#4ade80", or_, ow, ox),
        (v2, "Group",  "👥", "#a78bfa", gr,  gw, gx),
        (v3, "Others", "🌐", "#fb923c", otr, otw, otx),
    ]:
        perm = bits_to_sym(r, w, x)
        col.markdown(f"""
        <div style='background:#13131a; border:1px solid #252530; border-radius:14px;
                    padding:16px 10px; text-align:center;'>
            <div style='font-size:1.4rem; margin-bottom:6px;'>{icon}</div>
            <div style='font-family: Syne, sans-serif; font-size:0.7rem; font-weight:700;
                        letter-spacing:0.1em; text-transform:uppercase; color:#666;
                        margin-bottom:8px;'>{label}</div>
            <div style='font-family: JetBrains Mono, monospace; font-size:1.6rem;
                        font-weight:700; color:{color};
                        text-shadow: 0 0 15px {color}66;'>{perm}</div>
            <div style='font-family: JetBrains Mono, monospace; font-size:1.1rem;
                        color:#555; margin-top:4px;'>{bits_to_octal(r,w,x)}</div>
        </div>
        """, unsafe_allow_html=True)
 
# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#333; font-size:0.8rem;
            font-family: JetBrains Mono, monospace; border-top:1px solid #1a1a22;
            padding-top:20px;'>
    Unix Permission Calculator — works anywhere, no filesystem access needed
</div>
""", unsafe_allow_html=True)
 