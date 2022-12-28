import streamlit as st
import plotly.graph_objects as go
from weyl_groups import *
from helper import *




## DISPLAY HIGHEST WEIGHT IN NICE LATEX

def pretty(lamlist):
    string='Highest weight:  $\lambda = '
    first = True
    i = 0
    N = len(lamlist)
    while i<N:
        addin=''
        if lamlist[i]>0:
            if not first:
                addin+='+'
            else:
                first = False          
            if lamlist[i]==1:
                cf=''
            else:
                cf=str(lamlist[i])
            addin+=cf+'\omega_'+str(i+1)
        string+=addin
        i+=1
    if first:
        string+='0'
    string+='$'
    return string



## CHOOSE A LIE TYPE FROM DROPDOWN MENU

st.sidebar.write("Lie Type")

lie_type = st.sidebar.selectbox(label="",
                      options=['A1','A2','A3','B2','B3','C3','G2',
                                'A1 x A2','A1 x B2','A1 x G2','A1 x A1','A1 x A1 x A1'],
                      index=2,
                      label_visibility="collapsed",
                      #help='hi'
                      )
LS = LieSys(lie_type)

## USE SLIDERS TO CONTROL THE HIGHEST WEIGHT

header = st.sidebar.container() # holds the header, but gets updated later

lam1 = st.sidebar.slider(label="",min_value=0,value=3,max_value=10,label_visibility = "collapsed")
if LS.ran>1:
    lam2 = st.sidebar.slider(label="",min_value=0,value=2,max_value=10,label_visibility = "collapsed")
else:
    [lam2, lam3]=[0,0]
if LS.ran>2:
    lam3 = st.sidebar.slider(label="",min_value=0,value=1,max_value=10,label_visibility = "collapsed")
else:
    lam3=0
lam = Vector([lam1,lam2,lam3][:LS.ran])

header.write(pretty(lam.lst))

## USE THE TEXT ENTRY OR DROPDOWN TO INDICATE WEYL GROUP ELEMENT


st.sidebar.write("Weyl group element")
word = st.sidebar.text_input(label="",label_visibility="collapsed")
lastindex = LS.match(word)
thew = st.sidebar.selectbox(label="",
                            options=LS.wordlist,
                            index=lastindex,
                            label_visibility="collapsed")

w = LS.Wlist[thew]

## OPTIONALLY CHOOSE SOME COLORS

st.sidebar.write("Colors")

[column1, column2, column3] = st.sidebar.columns(3)

col1 = column1.color_picker(label="",value='#C4C58E',label_visibility="collapsed")
if LS.ran>2:
    col2 = column2.color_picker(label="",value='#BF3C6A',label_visibility="collapsed")
else:
    col2 = 'grey'
if LS.ran>2:
    col3 = column3.color_picker(label="",value='#00b4cc',label_visibility="collapsed")
else:
    col3 = 'grey'

## CREATE THE DemPoly OBJECT AND COMPUTE FACES

DP = DemPoly(LS,thew,lam)

if LS.ran<3:
    DP.get_face()
else:
    DP.get_faces()

[x,y,z,ilist,jlist,klist,cols] = DP.get_plotly_input([col1,col2,col3])


## CREATE THE FIGURE

if len(ilist)>0:

    fig = go.Figure(data=[
        go.Mesh3d(
            x=x,
            y=y,
            z=z,
            i=ilist,
            j=jlist,
            k=klist)
        ])
                           


    ## ADJUST SOME SETTINGS

    fig.update_traces(facecolor=cols,
                      flatshading=True,
                      lighting_diffuse=0.7,
                      hoverinfo="none"
                      )



    fig.update_layout(autosize=False,
                      height=500,
                      scene=dict(
                          aspectmode='data',
                          xaxis=dict(
                              tickvals=[],
                              gridcolor="white",
                              zerolinecolor="white"),
                          yaxis=dict(
                              tickvals=[],
                              gridcolor="white",
                              zerolinecolor="white"),
                          zaxis=dict(
                              tickvals=[],
                              gridcolor="white",
                              zerolinecolor="white"),
                          
                          xaxis_showspikes=False,
                          yaxis_showspikes=False,
                          zaxis_showspikes=False,
                          
                          xaxis_title='',
                          yaxis_title='',
                          zaxis_title=''
                          )
                      )

    ## PLACE THE FIGURE

    st.plotly_chart(fig, theme=None, use_container_width=True, equal_axes=True)




## TO-DO

## > 2d plots instead of 3d when relevant
## >>> is that based on LS.ran or on DP.eff_dim?
## > help mouseovers for info on the controls?
## >>> but what would these say?
## >>> the collapsed labels make these not show. 
## > generate random button
## > names of Levi types next to the colors
## > 

## WISH-LIST

## > mouseover vertices for ``s1s2lambda'' etc ?
## >>> how much can you do with mouseover?
## >>> some root system vectors appear also? would be super cool
## > w's text box autofill with corrected input
## > edges of any kind
## > affine types (eventual goal)
## > 
    



