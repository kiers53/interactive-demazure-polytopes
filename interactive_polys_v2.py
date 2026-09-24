from datetime import date
import numpy.random as npr
import plotly.graph_objects as go
import streamlit as st

from helper import *
from weyl_groups import *


def concat(alist):  # input a list of integers, concatenate into string
    return "".join(map(str, alist))


def get_random():
    typi = npr.randint(0, 7)
    typ = ["A3", "B3", "C3", "A1 x A2", "A1 x B2", "A1 x G2", "A1 x A1 x A1"][typi]
    st.session_state.typ = typ

    x = npr.randint(1, 11)
    y = npr.randint(1, 11)
    z = npr.randint(1, 11)
    st.session_state.l1 = x
    st.session_state.l2 = y
    st.session_state.l3 = z

    st.session_state.lam = Vector([x, y, z])

    LS = LieSys(typ)
    nn = len(LS.wordlist)

    found = False
    while not found:
        wi = npr.randint(0, nn)
        thew = LS.wordlist[wi]
        DP = DemPoly(LS, thew, st.session_state.lam)
        if DP.eff_dim == 3:
            found = True

    w = LS.Wlist[thew]
    st.session_state.wi = wi
    st.session_state.wword = concat(w.word)
    st.session_state.wtext = thew


st.button("Generate Random", on_click=get_random)

def process_type():
    # Re-initialize for the new Lie type
    LS = LieSys(st.session_state.typ)
    st.session_state.wi = len(LS.wordlist) - 1
    w = LS.Wlist[LS.wordlist[st.session_state.wi]]
    st.session_state.wword = concat(w.word)
    st.session_state.wtext = LS.wordlist[st.session_state.wi]


def process_word():
    # Fetch current LS based on session state type dynamically
    LS = LieSys(st.session_state.typ)
    word = st.session_state.wword
    
    # Match the typed string to an index in wordlist
    st.session_state.wi = LS.match(word)
    thew = LS.wordlist[st.session_state.wi]
    
    # Keep dropdown widget selection synchronized
    st.session_state.wtext = thew
    
    # Format canonical word back into the input field
    w = LS.Wlist[thew]
    st.session_state.wword = concat(w.word)


def process_dropdown():
    LS = LieSys(st.session_state.typ)
    st.session_state.wi = LS.wordlist.index(st.session_state.wtext)
    w = LS.Wlist[st.session_state.wtext]
    st.session_state.wword = concat(w.word)

## INITIALIZE FOR THE VERY FIRST TIME

if "typ" not in st.session_state:
    get_random()
elif "l1" not in st.session_state:
    get_random()
elif "wword" not in st.session_state or "wtext" not in st.session_state:
    get_random()


## DISPLAY HIGHEST WEIGHT IN NICE LATEX


def pretty(lamlist):
    string = "Highest weight:  \n$\\lambda = "
    first = True
    i = 0
    N = len(lamlist)
    while i < N:
        addin = ""
        if lamlist[i] > 0:
            if not first:
                addin += "+"
            else:
                first = False
            if lamlist[i] == 1:
                cf = ""
            else:
                cf = str(lamlist[i])
            addin += cf + "\\omega_" + str(i + 1)
            string += addin
        i += 1
    if first:
        string += "0"
    string += "$"
    return string


## PUT THE PICTURE AT THE TOP

pic_here = st.container()


## CHOOSE A LIE TYPE FROM DROPDOWN MENU

[control1, control2, control3] = st.columns(3)

control1.write("Lie Type")


lie_type = control1.selectbox(
    label="Select Lie Type",
    options=[
        "A3",
        "B3",
        "C3",
        "A1 x A2",
        "A1 x B2",
        "A1 x G2",
        "A1 x A1 x A1",
    ],
    label_visibility="collapsed",
    key="typ",
    on_change=process_type,
)
LS = LieSys(lie_type)


## USE THE TEXT ENTRY OR DROPDOWN TO INDICATE WEYL GROUP ELEMENT

control1.write("Weyl group element")

# 1. Text Input: triggers process_word
word = control1.text_input(
    label="Weyl group element input",
    label_visibility="collapsed",
    key="wword",
    on_change=process_word,
)

# 2. Selectbox Dropdown
thew = control1.selectbox(
    label="Select Weyl group element",
    options=LS.wordlist,
    label_visibility="collapsed",
    key="wtext",
    on_change=process_dropdown,
)

w = LS.Wlist[thew]

## USE SLIDERS TO CONTROL THE HIGHEST WEIGHT

header = control2.container()

lam1 = control2.slider(
    label="Lambda 1",
    min_value=0,
    max_value=10,
    label_visibility="collapsed",
    key="l1",
)
if LS.ran > 1:
    lam2 = control2.slider(
        label="Lambda 2",
        min_value=0,
        max_value=10,
        label_visibility="collapsed",
        key="l2",
    )
else:
    [lam2, lam3] = [0, 0]

if LS.ran > 2:
    lam3 = control2.slider(
        label="Lambda 3",
        min_value=0,
        max_value=10,
        label_visibility="collapsed",
        key="l3",
    )
else:
    lam3 = 0

lam = Vector([lam1, lam2, lam3][: LS.ran])

header.write(pretty(lam.lst))


## OPTIONALLY CHOOSE SOME COLORS

with control3.expander("Colors"):
    col1 = st.color_picker(
        label="Primary Color", value="#C4C58E", label_visibility="collapsed"
    )
    if LS.ran > 2:
        col2 = st.color_picker(
            label="Secondary Color", value="#BF3C6A", label_visibility="collapsed"
        )
    else:
        col2 = "grey"
    if LS.ran > 2:
        col3 = st.color_picker(
            label="Tertiary Color", value="#00b4cc", label_visibility="collapsed"
        )
    else:
        col3 = "grey"

## CREATE THE DemPoly OBJECT AND COMPUTE FACES

DP = DemPoly(LS, thew, lam)

if LS.ran < 3:
    DP.get_face()
else:
    DP.get_faces()

[x, y, z, ilist, jlist, klist, cols] = DP.get_plotly_input([col1, col2, col3])


## CREATE THE FIGURE

if len(ilist) > 0:
    fig = go.Figure(
        data=[
            go.Mesh3d(
                x=x, y=y, z=z, i=ilist, j=jlist, k=klist
            )
        ]
    )

    ## ADJUST SOME SETTINGS
    fig.update_traces(
        facecolor=cols, flatshading=True, lighting_diffuse=0.7, hoverinfo="none"
    )

    fig.update_layout(
        autosize=False,
        height=500,
        scene=dict(
            aspectmode="data",
            xaxis=dict(
                tickvals=[], gridcolor="white", zerolinecolor="white"
            ),
            yaxis=dict(
                tickvals=[], gridcolor="white", zerolinecolor="white"
            ),
            zaxis=dict(
                tickvals=[], gridcolor="white", zerolinecolor="white"
            ),
            xaxis_showspikes=False,
            yaxis_showspikes=False,
            zaxis_showspikes=False,
            xaxis_title="",
            yaxis_title="",
            zaxis_title="",
        ),
    )

    ## PLACE THE FIGURE
    pic_here.plotly_chart(fig, theme=None, use_container_width=True)


st.write(f"Copyright {date.today().year} Joshua Kiers")

## TO-DO

## > 2d plots instead of 3d when relevant
## >>> is that based on LS.ran or on DP.eff_dim?
## 
## > help mouseovers for info on the controls?
## >>> but what would these say?
## >>> the collapsed labels make these not show.
## >>> maybe make an "about" description paragraph at the bottom. 
## 
## > names of Levi types next to the colors
##
## > remove the little grey wires behind the 3d shape when viewed on small device?
##

## WISH-LIST

## > mouseover vertices for ``s1s2lambda'' etc ?
## >>> how much can you do with mouseover?
## >>> some root system vectors appear also? would be super cool
## 
## > edges of any kind
## 
## > affine types (eventual goal)
 


