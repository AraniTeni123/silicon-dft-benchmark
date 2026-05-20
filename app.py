import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Force Matplotlib to use a dark theme so plots blend into the website
plt.style.use('dark_background')

# --- 1. Page Configuration & Styling ---
st.set_page_config(page_title="Silicon DFT Benchmark", layout="wide")

# Modern, dark-themed CSS with !important to override OS-level light mode defaults
st.markdown("""
    <style>
    /* Main background and typography */
    .stApp { background-color: #0E1117 !important; font-family: 'Inter', -apple-system, sans-serif; }
    h1, h2, h3, h4, h5, h6 { color: #FFFFFF !important; font-weight: 600 !important; letter-spacing: -0.5px; }
    p, li, div, span, label { color: #E2E8F0 !important; }
    
    /* Sleek Tabs */
    .stTabs [data-baseweb="tab-list"] { border-bottom: 2px solid #334155; gap: 30px; }
    .stTabs [data-baseweb="tab"] { padding: 15px 5px; font-size: 1.1rem; color: #94A3B8 !important; font-weight: 500; }
    .stTabs [aria-selected="true"] { color: #FFFFFF !important; border-bottom-color: #3B82F6 !important; }
    
    /* Custom Cards for Flowchart */
    .concept-card {
        background-color: #1E293B !important;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        text-align: center;
        margin-bottom: 10px;
    }
    .concept-card b { color: #FFFFFF !important; }
    .arrow { text-align: center; font-size: 24px; color: #64748B !important; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

st.title("Silicon DFT Benchmark: LDA vs PBE")
st.markdown("""
This dashboard presents an interactive benchmark of ab initio Kohn-Sham density functional theory (DFT) calculations on bulk silicon. 
Navigate through the modules below to explore the theoretical foundations, analyze structural equations of state, and investigate the semiconductor band-gap problem.
""")

tab1, tab2, tab3 = st.tabs(["Theoretical Background", "Equation of State Analysis", "Band Gap Decomposition"])

# --- Helper Function ---
def birch_murnaghan(V, E0, V0, B, Bp):
    """Birch-Murnaghan Equation of State"""
    eta = (V0 / V)**(2.0 / 3.0)
    return E0 + 9.0 * V0 * B / 16.0 * (((eta - 1.0)**3 * Bp) + ((eta - 1.0)**2 * (6.0 - 4.0 * eta)))


# ==========================================
# TAB 1: THEORETICAL BACKGROUND
# ==========================================
with tab1:
    st.markdown("### Why does a theory designed to find the exact ground state of a quantum system fail so spectacularly at predicting a simple semiconductor band gap?")
    st.write("---")
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("""
        #### The Kohn-Sham Mapping
        In computational condensed-matter physics, calculating the many-body wavefunction for every interacting electron is computationally impossible. The **Hohenberg-Kohn theorems** prove that the ground-state properties of a system are uniquely determined by its electron density, reducing a $3N$-dimensional problem to just 3 spatial dimensions.
        
        The **Kohn-Sham (KS) ansatz** makes this practically solvable by mapping the complex, interacting electrons onto a fictitious system of non-interacting electrons moving in an effective potential. However, to make this math work, all the complex quantum mechanics—specifically Pauli repulsion (exchange) and electron correlation—must be bundled into a single term known as the Exchange-Correlation functional ($E_{xc}$).
        
        Because the exact mathematical form of $E_{xc}$ is unknown, we rely on approximations:
        * **LDA (Local Density Approximation):** Assumes the electron density behaves locally like a uniform electron gas. It overestimates exchange in inhomogeneous bonding regions, causing systematic **overbinding** (predicting lattice constants that are too small).
        * **PBE (Generalized Gradient Approximation):** Introduces a gradient correction. It weakens the exchange in bonding regions, which fixes LDA's overbinding but frequently overcompensates, leading to **underbinding**.
        
        While silicon serves as the standard, computationally inexpensive benchmark for these behaviors, understanding this limitation is absolutely critical when pushing DFT into more complex regimes, such as evaluating band gaps in 2D materials like molybdenum disulfide or modeling highly correlated spintronic devices, where these functional limits become even more pronounced.
        """)

    with col2:
        st.markdown("#### The Band-Gap Problem & Derivative Discontinuity")
        st.markdown(r"""
        The true fundamental gap ($\Delta$) is rigorously defined by total energy differences upon adding or removing an electron:
        $$ \Delta = E_0(N+1) + E_0(N-1) - 2E_0(N) $$
        
        Theoretical work by Perdew, Levy, Sham, and Schlüter demonstrated that this exact gap decomposes into two parts:
        $$ \Delta = \Delta_{KS} + \Delta_{xc} $$
        
        Where $\Delta_{KS}$ is the single-particle Kohn-Sham gap, and $\Delta_{xc}$ is the derivative discontinuity.
        """)
        
        # HTML Flowchart using pure HTML character entities for Delta to avoid LaTeX parsing issues
        st.markdown('<div class="concept-card"><b>1. LDA / PBE Functionals</b><br><span style="color:#94A3B8 !important; font-size:14px;">Constructed as smooth, continuous mathematical functions of electron density.</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="arrow">↓</div>', unsafe_allow_html=True)
        st.markdown('<div class="concept-card"><b>2. Functional Derivative</b><br><span style="color:#94A3B8 !important; font-size:14px;">Because the function is smooth, its derivative contains no jumps or breaks at integer particle numbers.</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="concept-card" style="border-left: 4px solid #EF4444;"><b>3. &Delta;<sub>xc</sub> = 0</b><br><span style="color:#94A3B8 !important; font-size:14px;">The many-body correction is mathematically forced to zero. The underestimated gap is a structural limitation, not a numerical bug.</span></div>', unsafe_allow_html=True)


# ==========================================
# TAB 2: INTERACTIVE EQUATION OF STATE
# ==========================================
with tab2:
    st.header("Birch-Murnaghan Equation of State")
    st.markdown("Adjust the structural parameters below to observe how the Birch-Murnaghan equation alters the depth, position, and curvature of the energy well compared to the static DFT data.")
    
    V_data_lda = np.linspace(235, 295, 9)
    E_data_lda = birch_murnaghan(V_data_lda, -15.852, 266.02, 0.032, 4.0)
    
    V_data_pbe = np.linspace(235, 295, 9)
    E_data_pbe = birch_murnaghan(V_data_pbe, -22.840, 276.13, 0.030, 4.0)

    st.markdown("#### Structural Parameter Controls")
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3)
    with ctrl_col1:
        user_V0 = st.slider("Equilibrium Volume (Bohr³)", 250.0, 290.0, 266.0, step=1.0)
    with ctrl_col2:
        user_B = st.slider("Bulk Modulus (Ry/Bohr³)", 0.010, 0.060, 0.032, step=0.002)
    with ctrl_col3:
        user_Bp = st.slider("Pressure Derivative", 2.0, 6.0, 4.0, step=0.1)

    V_smooth = np.linspace(235, 295, 100)
    E_user_lda = birch_murnaghan(V_smooth, -15.852, user_V0, user_B, user_Bp)
    E_user_pbe = birch_murnaghan(V_smooth, -22.840, user_V0, user_B, user_Bp)

    plot_col1, plot_col2 = st.columns(2)
    
    with plot_col1:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        # Ensure plot background is transparent to show website dark theme
        fig1.patch.set_facecolor('none')
        ax1.set_facecolor('none')
        ax1.scatter(V_data_lda, E_data_lda, color='#F8FAFC', label='DFT Data (LDA)', zorder=5)
        ax1.plot(V_smooth, E_user_lda, color='#3B82F6', lw=2, label='Interactive Fit')
        ax1.set_xlabel(r'Unit Cell Volume (Bohr$^3$)')
        ax1.set_ylabel('Total Energy (Ry)')
        ax1.grid(True, alpha=0.15)
        ax1.spines[['top', 'right']].set_visible(False)
        ax1.legend(frameon=False)
        st.pyplot(fig1, transparent=True)
        
    with plot_col2:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        fig2.patch.set_facecolor('none')
        ax2.set_facecolor('none')
        ax2.scatter(V_data_pbe, E_data_pbe, color='#F8FAFC', label='DFT Data (PBE)', zorder=5)
        ax2.plot(V_smooth, E_user_pbe, color='#EF4444', lw=2, label='Interactive Fit')
        ax2.set_xlabel(r'Unit Cell Volume (Bohr$^3$)')
        ax2.set_ylabel('Total Energy (Ry)')
        ax2.grid(True, alpha=0.15)
        ax2.spines[['top', 'right']].set_visible(False)
        ax2.legend(frameon=False)
        st.pyplot(fig2, transparent=True)


# ==========================================
# TAB 3: BAND GAP DECOMPOSITION
# ==========================================
with tab3:
    st.header("Decomposing the Semiconductor Gap")
    st.markdown("Silicon's experimental gap is **1.17 eV**. Use the sliders to define the single-particle Kohn-Sham gap, and observe how the required many-body correction mathematically compensates to match the experimental reality.")
    
    col_text, col_plot = st.columns([1, 2])
    
    with col_text:
        st.markdown("#### Adjust Kohn-Sham Gap")
        user_ks_lda = st.slider(r"LDA $\Delta_{KS}$ (eV)", 0.200, 1.170, 0.527, step=0.01)
        user_ks_pbe = st.slider(r"PBE $\Delta_{KS}$ (eV)", 0.200, 1.170, 0.612, step=0.01)
        
        st.markdown("#### Required Corrections:")
        st.info(f"LDA $\\Delta_{{xc}}$ : **{1.17 - user_ks_lda:.3f} eV**\n\n"
                f"PBE $\\Delta_{{xc}}$ : **{1.17 - user_ks_pbe:.3f} eV**")
        
    with col_plot:
        methods = ['LDA\n(Interactive)', 'PBE\n(Interactive)', 'Experiment']
        dKS = [user_ks_lda, user_ks_pbe, 1.170]
        dxc = [1.17 - user_ks_lda, 1.17 - user_ks_pbe, 0.0]
        
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        fig3.patch.set_facecolor('none')
        ax3.set_facecolor('none')
        x = np.arange(len(methods))
        
        ax3.bar(x, dKS, color='#3B82F6', edgecolor='#1E293B', label=r'$\Delta_{KS}$ (Single-Particle)')
        ax3.bar(x, dxc, bottom=dKS, color='#EF4444', alpha=0.9, edgecolor='#1E293B', label=r'$\Delta_{xc}$ (Derivative Discontinuity)')
        ax3.axhline(1.17, color='#F8FAFC', ls='--', lw=1.5, label='Experimental Gap (1.17 eV)')
        
        ax3.set_xticks(x)
        ax3.set_xticklabels(methods, fontsize=11, fontweight='bold', color='#F8FAFC')
        ax3.set_ylabel('Band gap (eV)', fontsize=12, color='#F8FAFC')
        ax3.tick_params(axis='x', colors='#F8FAFC')
        ax3.tick_params(axis='y', colors='#F8FAFC')
        ax3.spines[['top', 'right']].set_visible(False)
        ax3.spines['left'].set_color('#F8FAFC')
        ax3.spines['bottom'].set_color('#F8FAFC')
        
        # Legend text color formatting
        legend = ax3.legend(loc='lower right', frameon=False)
        for text in legend.get_texts():
            text.set_color('#F8FAFC')
        
        for i, (k, c) in enumerate(zip(dKS, dxc)):
            if k > 0.1:
                ax3.text(i, k/2, f'{k:.3f}', ha='center', va='center', color='#F8FAFC', fontweight='bold')
            if c > 0.1:
                ax3.text(i, k + c/2, f'{c:.3f}', ha='center', va='center', color='#F8FAFC', fontweight='bold')
                
        st.pyplot(fig3, transparent=True)