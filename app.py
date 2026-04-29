import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Flavor Match", page_icon="🍽", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #0f0e0d !important; color: #f5f0e8 !important; }
.stApp { background-color: #0f0e0d !important; }
.block-container { padding: 2rem 1.5rem 4rem !important; max-width: 720px !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.hero { text-align: center; padding: 3rem 1rem 2rem; }
.hero-eyebrow { font-size: 0.75rem; font-weight: 500; letter-spacing: 0.25em; text-transform: uppercase; color: #c9a84c; margin-bottom: 0.75rem; }
.hero-title { font-family: 'Playfair Display', serif; font-size: 3.8rem; font-weight: 900; line-height: 1.05; color: #f5f0e8; margin-bottom: 1rem; }
.hero-title span { color: #c9a84c; }
.hero-sub { font-size: 1rem; color: #9e9689; max-width: 400px; margin: 0 auto 2rem; line-height: 1.6; }
.section-label { font-size: 0.7rem; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; color: #c9a84c; margin-top: 2.5rem; margin-bottom: 0.3rem; }
.section-title { font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 700; color: #f5f0e8; margin-bottom: 1.2rem; }
.fancy-divider { border: none; border-top: 1px solid #2a2825; margin: 2rem 0; }
.stRadio > div { flex-direction: row !important; flex-wrap: wrap !important; gap: 8px !important; }
.stRadio > div > label { background: #1a1916 !important; border: 1px solid #2a2825 !important; border-radius: 100px !important; padding: 6px 16px !important; font-size: 0.85rem !important; color: #f5f0e8 !important; cursor: pointer !important; white-space: nowrap !important; }
.stRadio > div > label:hover { border-color: #c9a84c !important; color: #c9a84c !important; }
.stSelectbox > div > div { background: #1a1916 !important; border: 1px solid #2a2825 !important; border-radius: 12px !important; color: #f5f0e8 !important; }
.stTextInput > div > div > input { background: #1a1916 !important; border: 1px solid #2a2825 !important; border-radius: 12px !important; color: #f5f0e8 !important; font-size: 1.1rem !important; padding: 12px 16px !important; }
.stFormSubmitButton > button { background: #c9a84c !important; color: #0f0e0d !important; border: none !important; border-radius: 100px !important; padding: 14px 40px !important; font-family: 'DM Sans', sans-serif !important; font-size: 1rem !important; font-weight: 600 !important; width: 100% !important; margin-top: 1.5rem !important; }
.stFormSubmitButton > button:hover { background: #e8c55a !important; }
.result-hero { background: linear-gradient(135deg, #1a1916 0%, #221f1a 100%); border: 1px solid #c9a84c; border-radius: 24px; padding: 2.5rem 2rem; text-align: center; margin: 1.5rem 0; }
.result-eyebrow { font-size: 0.7rem; letter-spacing: 0.25em; text-transform: uppercase; color: #9e9689; margin-bottom: 0.5rem; }
.result-name { font-family: 'Playfair Display', serif; font-size: 2.8rem; font-weight: 900; color: #c9a84c; margin-bottom: 0.25rem; }
.result-score { font-family: 'Playfair Display', serif; font-size: 5rem; font-weight: 900; color: #f5f0e8; line-height: 1; }
.result-score-label { font-size: 0.85rem; color: #9e9689; margin-top: 0.25rem; }
.score-pill { display: inline-block; padding: 4px 14px; border-radius: 100px; font-size: 0.8rem; font-weight: 500; margin: 3px; }
.score-high { background: rgba(46,204,113,0.15); color: #2ecc71; border: 1px solid rgba(46,204,113,0.3); }
.score-mid { background: rgba(243,156,18,0.15); color: #f39c12; border: 1px solid rgba(243,156,18,0.3); }
.score-low { background: rgba(231,76,60,0.15); color: #e74c3c; border: 1px solid rgba(231,76,60,0.3); }
.food-row { display: flex; align-items: center; gap: 16px; margin-bottom: 4px; margin-top: 1.5rem; }
.food-thumb { width: 120px; height: 120px; border-radius: 16px; object-fit: cover; border: 1px solid #2a2825; }
.food-label-top { font-size: 0.7rem; color: #9e9689; letter-spacing: 0.1em; text-transform: uppercase; }
.food-label-main { font-size: 1.3rem; font-weight: 600; color: #f5f0e8; font-family: 'Playfair Display', serif; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
POLARIZER_COLS = [
    'Do you Like Cilantro','Do you Like Anchovies','Do you Like Blue Cheese',
    'Do you Like Olives','Do you Like Raw Oysters','Do you Like Mushrooms',
    'Do you Like Runny egg yolks','Do you Like Tofu',
    'Do you Like fermented / pickled foods (kimichi, sauerkraut)',
]
CUISINE_COLS = [
    'Japanese','Thai or Vietnamese','Indian (curries, biryani, dosas...)',
    'Mexican','Middle Eastern / Mediterranean (sharwarma, hummus, kebab)','Korean',
]
POLARIZER_MAP  = {'Love it':2,'Fine with it':1,'Neutral':0,'Never tried but would':0.5,"Never tried and won't":-1,'Hate it':-2}
CUISINE_MAP    = {'Love it':2,'Like it':1,'Neutral':0,'Avoid':-1,'Never tried':0}
BUDGET_MAP     = {'under $ 15':1,'$ 15 - 30':2,'$ 30 - 60':3,'$ 60+':4,'I only eat out for special occasions':0}
LATE_NIGHT_MAP = {'Nothing after dinner':1,'Occasional late snack':2,'Regular midnight snacker':3,'2 am full-meal enjoyer':4,'2am full-meal enjoyer':4}
SNACK_MAP      = {'Rarely / I stick to meals':1,'Sometimes':2,'Daily':3,'Constantly':4}
WEIGHTS        = {'polarizer':0.25,'cuisine':0.20,'eating_style':0.15,'adventurousness':0.10,'late_night':0.15,'budget':0.15}

FOOD_INFO = {
    'Do you Like Cilantro':('🌿','Cilantro','images/Cilantro.jpg'),
    'Do you Like Anchovies':('🐟','Anchovies','images/Anchoives.jpg'),
    'Do you Like Blue Cheese':('🧀','Blue Cheese','images/Blue Cheese.jpg'),
    'Do you Like Olives':('🫒','Olives','images/Olives.jpg'),
    'Do you Like Raw Oysters':('🦪','Raw Oysters','images/Raw Oysters.jpg'),
    'Do you Like Mushrooms':('🍄','Mushrooms','images/Mushrooms.jpg'),
    'Do you Like Runny egg yolks':('🍳','Runny Yolks','images/Runny egg yolks.jpg'),
    'Do you Like Tofu':('🥢','Tofu','images/Tofu.jpg'),
    'Do you Like fermented / pickled foods (kimichi, sauerkraut)':('🥒','Fermented Foods','images/Fermented.jpg'),
}
CUISINE_INFO = {
    'Japanese':('🍣','Japanese','images/Japanese food.png'),
    'Thai or Vietnamese':('🍜','Thai / Vietnamese','images/Thai or Vietnamese.jpg'),
    'Indian (curries, biryani, dosas...)':('🍛','Indian','images/Indian food.jpg'),
    'Mexican':('🌮','Mexican','images/Mexican food.jpg'),
    'Middle Eastern / Mediterranean (sharwarma, hummus, kebab)':('🥙','Middle Eastern','images/Meddateranian food.jpg'),
    'Korean':('🥘','Korean','images/Korean food.jpg'),
}

# ── Scoring ───────────────────────────────────────────────────────────────────
def cosine_sim(v1,v2):
    a,b=np.array(v1,dtype=float),np.array(v2,dtype=float)
    if np.linalg.norm(a)==0 or np.linalg.norm(b)==0: return 0.0
    return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))

def polarizer_score(p1,p2):
    v1=[POLARIZER_MAP.get(p1.get(c,'Neutral'),0) for c in POLARIZER_COLS]
    v2=[POLARIZER_MAP.get(p2.get(c,'Neutral'),0) for c in POLARIZER_COLS]
    return round((cosine_sim(v1,v2)+1)*50,1)

def cuisine_score(p1,p2):
    v1=[CUISINE_MAP.get(p1.get(c,'Neutral'),0) for c in CUISINE_COLS]
    v2=[CUISINE_MAP.get(p2.get(c,'Neutral'),0) for c in CUISINE_COLS]
    return round((cosine_sim(v1,v2)+1)*50,1)

def eating_style_score(p1,p2):
    cols=['Strongest craving type',"Texture you can't stand",'How do you like your food cooked?','Eating pace','Ordering style at a restaurant with friends',"When you're stressed, you"]
    matches=sum(str(p1.get(c,'')).strip().lower()==str(p2.get(c,'')).strip().lower() for c in cols)
    return round(100*matches/len(cols),1)

def adventurousness_score(p1,p2):
    try: a,b=float(p1.get('How adventurousness with new foods',3)),float(p2.get('How adventurousness with new foods',3))
    except: return 50.0
    return round(100*(1-abs(a-b)/4),1)

def late_night_score(p1,p2):
    a1=LATE_NIGHT_MAP.get(p1.get('Late-night eating','Occasional late snack'),2)
    a2=LATE_NIGHT_MAP.get(p2.get('Late-night eating','Occasional late snack'),2)
    b1=SNACK_MAP.get(p1.get('Snacking frequency','Sometimes'),2)
    b2=SNACK_MAP.get(p2.get('Snacking frequency','Sometimes'),2)
    return round(100*((1-abs(a1-a2)/3)+(1-abs(b1-b2)/3))/2,1)

def budget_score(p1,p2):
    a=BUDGET_MAP.get(str(p1.get('Ideal dinner budget','$ 15 - 30')).strip(),2)
    b=BUDGET_MAP.get(str(p2.get('Ideal dinner budget','$ 15 - 30')).strip(),2)
    if a==0 or b==0: return 50.0
    return round(100*(1-abs(a-b)/3),1)

def dietary_compatible(p1,p2):
    r1=str(p1.get('Dietary restrictions','None')).strip().lower()
    r2=str(p2.get('Dietary restrictions','None')).strip().lower()
    if r1 in ('nan','','none'): r1='none'
    if r2 in ('nan','','none'): r2='none'
    return r1==r2 or r1=='none' or r2=='none'

def compute_match(p1,p2):
    subs={'polarizer':polarizer_score(p1,p2),'cuisine':cuisine_score(p1,p2),'eating_style':eating_style_score(p1,p2),'adventurousness':adventurousness_score(p1,p2),'late_night':late_night_score(p1,p2),'budget':budget_score(p1,p2)}
    subs['overall']=round(sum(subs[k]*WEIGHTS[k] for k in WEIGHTS),1)
    subs['dietary_compatible']=dietary_compatible(p1,p2)
    return subs

def find_best_match(new_person,existing_df):
    results=[]
    for _,row in existing_df.iterrows():
        other=row.to_dict()
        if other.get('Your name','')==new_person.get('Your name',''): continue
        s=compute_match(new_person,other)
        if not s['dietary_compatible']: continue
        s['name']=other.get('Your name','Unknown')
        results.append(s)
    return sorted(results,key=lambda x:x['overall'],reverse=True)[0] if results else None

SHEET_ID = "1zn-sxMSw5ohyzyD7qr7ajiqYx01QuffjIoghv5l4gHw"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=921545234"

@st.cache_data(ttl=60)
def load_existing():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip().str.replace('"', '')
        nc = [c for c in df.columns if 'name' in c.lower()]
        if nc:
            df = df.rename(columns={nc[0]: 'Your name'})
        df = df.dropna(subset=['Your name'])
        df = df[df['Your name'].str.strip() != '']
        return df
    except Exception as e:
        st.error(f"Could not load responses: {e}")
        return None

def pill_class(v): return 'score-high' if v>=70 else 'score-mid' if v>=40 else 'score-low'

def make_chart(scores,na,nb):
    keys=['polarizer','cuisine','eating_style','adventurousness','late_night','budget']
    labels=['Polarizers','Cuisine','Eating Style','Adventurousness','Late Night','Budget']
    vals=[scores[k] for k in keys]
    colors=['#2ecc71' if v>=70 else '#f39c12' if v>=40 else '#e74c3c' for v in vals]
    fig,ax=plt.subplots(figsize=(8,3.5))
    fig.patch.set_facecolor('#1a1916'); ax.set_facecolor('#1a1916')
    ax.barh(labels[::-1],vals[::-1],color=colors[::-1],height=0.55)
    ax.set_xlim(0,115); ax.tick_params(colors='#9e9689',labelsize=9)
    for spine in ax.spines.values(): spine.set_color('#2a2825')
    ax.axvline(50,linestyle='--',color='#2a2825',alpha=0.8,linewidth=1)
    for i,(v,l) in enumerate(zip(vals[::-1],labels[::-1])):
        ax.text(v+2,i,f'{v:.0f}',va='center',color='#f5f0e8',fontsize=9,fontweight='bold')
    ax.set_title(f'{na} ↔ {nb}',color='#f5f0e8',fontsize=11,fontweight='bold',pad=12)
    plt.tight_layout(); return fig

# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ the food compatibility quiz ✦</div>
    <div class="hero-title">Find your<br><span>flavor</span> match</div>
    <div class="hero-sub">Answer a few questions about what you eat, crave, and avoid — we'll find who you belong at the table with.</div>
</div>
""", unsafe_allow_html=True)

existing_df = load_existing()
if existing_df is not None:
    st.markdown(f"<div style='text-align:center;font-size:0.8rem;color:#c9a84c;margin-bottom:1rem'>✓ {len(existing_df)} people in the pool</div>", unsafe_allow_html=True)
    with st.expander("🔧 Debug — click to see column names from your sheet"):
        for i, col in enumerate(existing_df.columns):
            st.write(f"{i}: {col}")
else:
    st.markdown("<div style='text-align:center;font-size:0.8rem;color:#9e9689;margin-bottom:0.5rem'>⚠️ Could not load responses — check your Google Sheet is public</div>", unsafe_allow_html=True)

st.markdown("<hr class='fancy-divider'>",unsafe_allow_html=True)

with st.form("survey"):
    # Name
    st.markdown('<div class="section-label">First things first</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">What\'s your name?</div>',unsafe_allow_html=True)
    name=st.text_input("",placeholder="Type your name...",label_visibility="collapsed")

    # Polarizers
    st.markdown("<hr class='fancy-divider'>",unsafe_allow_html=True)
    st.markdown('<div class="section-label">The real test</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Love it or hate it?</div>',unsafe_allow_html=True)
    st.markdown("<p style='color:#9e9689;font-size:0.9rem;margin-top:-0.5rem;margin-bottom:1.2rem'>These divisive foods reveal more about you than you think.</p>",unsafe_allow_html=True)

    pol_opts=['Love it','Fine with it','Neutral','Never tried but would',"Never tried and won't",'Hate it']
    pol_answers={}
    for col_key,(emoji,label,img) in FOOD_INFO.items():
        img_col, txt_col = st.columns([1, 4])
        with img_col:
            try:
                st.image(img, width=120)
            except Exception:
                st.markdown(f"<div style='font-size:4rem;text-align:center'>{emoji}</div>", unsafe_allow_html=True)
        with txt_col:
            st.markdown(f"""<div style="padding-top:20px">
                <div class="food-label-top">{emoji}</div>
                <div class="food-label-main">{label}</div>
            </div>""", unsafe_allow_html=True)
        pol_answers[col_key]=st.radio("",pol_opts,horizontal=True,key=f"p_{col_key}",label_visibility="collapsed")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Cuisines
    st.markdown("<hr class='fancy-divider'>",unsafe_allow_html=True)
    st.markdown('<div class="section-label">Around the world</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your cuisine passport</div>',unsafe_allow_html=True)

    cuisine_opts=['Love it','Like it','Neutral','Avoid','Never tried']
    cuisine_answers={}
    for col_key,(emoji,label,img) in CUISINE_INFO.items():
        img_col, txt_col = st.columns([1, 4])
        with img_col:
            try:
                st.image(img, width=120)
            except Exception:
                st.markdown(f"<div style='font-size:4rem;text-align:center'>{emoji}</div>", unsafe_allow_html=True)
        with txt_col:
            st.markdown(f"""<div style="padding-top:20px">
                <div class="food-label-top">{emoji}</div>
                <div class="food-label-main">{label}</div>
            </div>""", unsafe_allow_html=True)
        cuisine_answers[col_key]=st.radio("",cuisine_opts,horizontal=True,key=f"c_{col_key}",label_visibility="collapsed")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Eating style
    st.markdown("<hr class='fancy-divider'>",unsafe_allow_html=True)
    st.markdown('<div class="section-label">How you eat</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your eating personality</div>',unsafe_allow_html=True)

    c1,c2=st.columns(2)
    with c1:
        st.markdown("<div style='font-size:0.8rem;color:#9e9689;margin-bottom:4px'>Strongest craving</div>",unsafe_allow_html=True)
        craving=st.selectbox("",['Sweet','Umami / savory','Spicy','Salty','Sour / tangy','No strong preference'],key="craving",label_visibility="collapsed")
        st.markdown("<div style='font-size:0.8rem;color:#9e9689;margin-bottom:4px;margin-top:12px'>Texture you can't stand</div>",unsafe_allow_html=True)
        texture=st.selectbox("",['Mushy','Slimy','Crunchy','Chewy','Gritty','None, I am texture-tolerant'],key="texture",label_visibility="collapsed")
        st.markdown("<div style='font-size:0.8rem;color:#9e9689;margin-bottom:4px;margin-top:12px'>Eating pace</div>",unsafe_allow_html=True)
        pace=st.selectbox("",['Inhale food','Average pace','Slow and savor'],key="pace",label_visibility="collapsed")
    with c2:
        st.markdown("<div style='font-size:0.8rem;color:#9e9689;margin-bottom:4px'>Food cooked how?</div>",unsafe_allow_html=True)
        cooked=st.selectbox("",['Fresh / raw / light','Braised / tender','Crispy / fried','Charred / grilled','No preference'],key="cooked",label_visibility="collapsed")
        st.markdown("<div style='font-size:0.8rem;color:#9e9689;margin-bottom:4px;margin-top:12px'>Ordering style</div>",unsafe_allow_html=True)
        ordering=st.selectbox("",['Tapas-style always','Love sharing','Willing to share if asked','Depends on the food','I keep my plate to myself'],key="ordering",label_visibility="collapsed")
        st.markdown("<div style='font-size:0.8rem;color:#9e9689;margin-bottom:4px;margin-top:12px'>When stressed, you</div>",unsafe_allow_html=True)
        stress=st.selectbox("",['Eat more of whatever\'s around','Crave sweets / chocolates','Crave salty / savory snacks','Lose my appetite','Order comfort food delivery'],key="stress",label_visibility="collapsed")

    # Late night
    st.markdown("<hr class='fancy-divider'>",unsafe_allow_html=True)
    st.markdown('<div class="section-label">Night owl habits</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">After dark & on the go</div>',unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.8rem;color:#9e9689;margin-bottom:6px'>How adventurous are you? (1 = very picky · 5 = eat anything)</div>",unsafe_allow_html=True)
    adventurousness=st.slider("",1,5,3,key="adv",label_visibility="collapsed")
    c3,c4=st.columns(2)
    with c3:
        st.markdown("<div style='font-size:0.8rem;color:#9e9689;margin-bottom:4px'>Snacking frequency</div>",unsafe_allow_html=True)
        snacking=st.selectbox("",['Rarely / I stick to meals','Sometimes','Daily','Constantly'],key="snack",label_visibility="collapsed")
    with c4:
        st.markdown("<div style='font-size:0.8rem;color:#9e9689;margin-bottom:4px'>Late-night eating</div>",unsafe_allow_html=True)
        late_night=st.selectbox("",['Nothing after dinner','Occasional late snack','Regular midnight snacker','2 am full-meal enjoyer'],key="late",label_visibility="collapsed")

    # Budget
    st.markdown("<hr class='fancy-divider'>",unsafe_allow_html=True)
    st.markdown('<div class="section-label">The practicalities</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Budget & diet</div>',unsafe_allow_html=True)
    c5,c6=st.columns(2)
    with c5:
        st.markdown("<div style='font-size:0.8rem;color:#9e9689;margin-bottom:4px'>Ideal dinner budget (per person)</div>",unsafe_allow_html=True)
        budget=st.selectbox("",['under $ 15','$ 15 - 30','$ 30 - 60','$ 60+','I only eat out for special occasions'],key="bud",label_visibility="collapsed")
    with c6:
        st.markdown("<div style='font-size:0.8rem;color:#9e9689;margin-bottom:4px'>Dietary restrictions (leave blank if none)</div>",unsafe_allow_html=True)
        dietary=st.text_input("",placeholder="e.g. vegetarian",key="diet",label_visibility="collapsed")

    st.markdown("<div style='height:8px'></div>",unsafe_allow_html=True)
    submitted=st.form_submit_button("✦ Find my flavor match",use_container_width=True)

# Results
if submitted:
    if not name.strip():
        st.error("Please enter your name to continue.")
        st.stop()

    new_person={
        'Your name':name.strip(),**pol_answers,**cuisine_answers,
        'Strongest craving type':craving,"Texture you can't stand":texture,
        'How do you like your food cooked?':cooked,
        'How adventurousness with new foods':adventurousness,
        'Snacking frequency':snacking,'Late-night eating':late_night,
        'Eating pace':pace,'Ordering style at a restaurant with friends':ordering,
        "When you're stressed, you":stress,
        'Dietary restrictions':dietary.strip() if dietary.strip() else 'None',
        'Ideal dinner budget':budget,
    }

    st.markdown("<hr class='fancy-divider'>",unsafe_allow_html=True)

    if existing_df is None:
        st.markdown("""<div style="text-align:center;padding:2rem;background:#1a1916;border-radius:16px;border:1px solid #2a2825">
            <div style="font-size:2rem;margin-bottom:0.5rem">📂</div>
            <div style="color:#f5f0e8;font-weight:500;margin-bottom:0.5rem">Upload your responses file to find your match</div>
            <div style="color:#9e9689;font-size:0.85rem">Upload the Excel export from Google Sheets above</div>
        </div>""",unsafe_allow_html=True)
    else:
        best=find_best_match(new_person,existing_df)
        if best is None:
            st.error("No compatible matches found yet — invite more friends!")
        else:
            overall=best['overall']
            verdict="🔥 Exceptional match" if overall>=80 else "✨ Great match" if overall>=65 else "👍 Decent match"
            st.markdown(f"""<div class="result-hero">
                <div class="result-eyebrow">your flavor soulmate</div>
                <div class="result-name">{best['name']}</div>
                <div class="result-score">{overall}</div>
                <div class="result-score-label">out of 100 · {verdict}</div>
            </div>""",unsafe_allow_html=True)

            pill_labels={'polarizer':'🌿 Polarizers','cuisine':'🍜 Cuisine','eating_style':'🍽 Eating Style','adventurousness':'🗺 Adventurousness','late_night':'🌙 Late Night','budget':'💰 Budget'}
            pills="<div style='text-align:center;margin:1.2rem 0'>"
            for k,lbl in pill_labels.items():
                v=best[k]; pills+=f'<span class="score-pill {pill_class(v)}">{lbl} {v:.0f}</span>'
            pills+="</div>"
            st.markdown(pills,unsafe_allow_html=True)

            fig=make_chart(best,name.strip(),best['name'])
            st.pyplot(fig,use_container_width=True)

            with st.expander("See everyone ranked"):
                all_r=[]
                for _,row in existing_df.iterrows():
                    o=row.to_dict()
                    if o.get('Your name','')==name.strip(): continue
                    s=compute_match(new_person,o); s['Name']=o.get('Your name','?'); s['Diet']='✅' if s['dietary_compatible'] else '⚠️'
                    all_r.append(s)
                ranked=sorted(all_r,key=lambda x:x['overall'],reverse=True)
                disp=pd.DataFrame(ranked)[['Name','overall','polarizer','cuisine','eating_style','adventurousness','late_night','budget','Diet']]
                disp.columns=['Name','Overall','Polarizers','Cuisine','Eating Style','Adventurousness','Late Night','Budget','Diet']
                st.dataframe(disp,use_container_width=True,hide_index=True)

st.markdown("<div style='text-align:center;margin-top:3rem;padding-top:2rem;border-top:1px solid #2a2825'><div style='font-size:0.7rem;color:#3a3835;letter-spacing:0.15em;text-transform:uppercase'>Flavor Match · built with ♥</div></div>",unsafe_allow_html=True)
