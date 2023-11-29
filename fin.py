%%writefile app.py
import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import dash
from dash import dcc, html
from streamlit_option_menu import option_menu
from PIL import Image
from dash.dependencies import Input, Output

st.set_page_config(layout="wide")
st.write('<div id="home"> </div>', unsafe_allow_html=True)
st.header("MOTOR VEHICLE COLLISIONS IN NEW YORK")
st.write("Data extracted from the New York department of city planning")
st.write("https://www.nyc.gov/site/planning/index.page"
         "\n\n"
         "By Iker Estrada"
)

imgtaxi = "https://www.expedia.es/stories/wp-content/uploads/2021/06/200503-share-image.jpg"
st.image(imgtaxi, width=1245)
dfz = pd.read_csv("MVC_NY.csv")

menu = option_menu(None, ["General review", "Explore by borough",  "Additional Exploration"],
    icons=['dashboard', 'city', 'ambulance'], menu_icon="cast",
    default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "3!important", "background-color": "#1e1e1e"},
        "icon": {"color": "white", "font-size": "25px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin":"0px"},
        "nav-link-selected": {"background-color": "black"},
    }
)
menu

############################################################################################
#____________________________________Review General____________________________________
def pag_genrev():

  st.sidebar.markdown('''
  # Sections
  - [Home](#home)
  - [Summary](#summary)
  - [Diversity of Factors](#diversity-of-factors)
  ''', unsafe_allow_html=True)

#____________________Summary
  st.header("Summary")
  st.write('<div id="summary"> </div>', unsafe_allow_html=True)
  st.write(
      "Welcome to our comprehensive analysis of collisions in New York City, where we delve into various factors, including districts, causes, frequencies, and other key variables. This interactive platform allows you to explore and gain insights into the intricate patterns and trends associated with traffic incidents across the city's diverse boroughs."
      "\n\n"
      "New York City, with its complex network of streets, iconic landmarks, and diverse population, experiences a unique set of challenges when it comes to road safety. The bustling urban environment, coupled with a myriad of transportation modes, contributes to the complexity of understanding and addressing collisions."
      "\n\n"
      "Our platform is designed to provide you with a deeper understanding of the dynamics of crashes in this vibrant metropolis. Whether you're interested in understanding collision frequencies by district, exploring the root causes behind incidents, or examining the broader impact of variables on road safety, our platform offers a dynamic and informative experience. Navigate through the data-rich visualizations to uncover valuable information and contribute to a better understanding of traffic dynamics in the bustling streets of New York."
      "\n\n"
      "Next, we have an interactive map that shows the different types of collisions and the zones where they are registered pinned on the map "
  )
#____________________Summary
#____________________Mapa
  dfz['CRASH DATE'] = pd.to_datetime(dfz['CRASH DATE'], format='%Y-%m-%d')
  dfz['YEAR'] = dfz['CRASH DATE'].dt.year
  sorted_years = sorted(dfz['YEAR'].unique())

  fig = px.scatter_mapbox(dfz,
                          lat="LATITUDE",
                          lon="LONGITUDE",
                          color="Contributing Factor",
                          color_discrete_sequence=['red'],
                          mapbox_style="carto-positron",
                          center={'lat': 40.7128, 'lon': -74.0060},
                          zoom=9.5,
                          height=800,
                          width=1250)

  selected_factor = st.selectbox('Select a contributing factor:', dfz['Contributing Factor'].unique())
  selected_year = st.selectbox('Select a year:', sorted_years)
  filtered_df = dfz[(dfz['Contributing Factor'] == selected_factor) & (dfz['YEAR'] == selected_year)]
  updated_fig = px.scatter_mapbox(filtered_df,
                                  lat="LATITUDE",
                                  lon="LONGITUDE",
                                  color="Contributing Factor",
                                  color_discrete_sequence=['red'],
                                  mapbox_style="carto-positron",
                                  center={'lat': 40.7128, 'lon': -74.0060},
                                  zoom=9.5,
                                  height=800,
                                  width=1250)
  st.plotly_chart(updated_fig)
#____________________Mapa
  st.write('<div id="diversity-of-factors"> </div>', unsafe_allow_html=True)
  st.write("""
      Collisions in urban areas, such as New York City, are influenced by a myriad of factors that fluctuate throughout the day, contributing to distinctive patterns in collision rates. One significant factor is the city's congestion, which varies with the time of day due to factors like rush hours and increased vehicular activity during working hours. The morning and evening rush hours, coinciding with the start and end of the typical workday, often witness heightened traffic volumes, presenting a higher risk of collisions. Additionally, the type of collisions may vary, with rear-end collisions potentially increasing during congested periods.
  """)
  horas = dfz['Day Hour'].value_counts().reset_index()
  horas.columns = ['Hour', 'Frecquency']
  fig1 = px.bar(horas, x='Hour', y='Frecquency', color_discrete_sequence=['#FF0000'])
  st.title("Collisions during the day (hours)")
  st.write(fig1)
  st.write("""
  The dynamics of the city's transportation infrastructure, including public transit schedules and road maintenance, also play a role. Understanding these temporal trends is crucial for devising targeted strategies to enhance urban safety and mitigate collision risks during peak hours. The graph depicting collisions per hour provides valuable insights into the temporal dynamics of urban collisions, serving as a foundation for informed policy decisions and proactive safety measures.
  """)
#____________________________________Review General____________________________________
############################################################################################
#____________________Exploración por borough (pie y bar incidents)__________________________
def pag_expbor():
    st.sidebar.markdown('''
    # Sections
    - [Home](#home)
    - [Summary](#summary)
    - [Incidents](#incidents)
    ''', unsafe_allow_html=True)
    st.write('<div id="summary"> </div>', unsafe_allow_html=True)
    st.write('''
    Exploring collision data across different boroughs provides a nuanced understanding of the safety dynamics within a metropolitan area. Each borough, with its distinct characteristics and traffic patterns, contributes to the overall landscape of road incidents. Analyzing and visualizing collision data for individual boroughs unveils localized trends, variations in contributing factors, and potential areas for targeted safety interventions. These graphs offer a granular perspective, allowing stakeholders to identify patterns specific to each borough, assess the efficacy of safety measures, and tailor interventions to address unique challenges. Whether unveiling the bustling streets of Manhattan, the residential enclaves of Queens, or the diverse road networks of Brooklyn, these graphs encapsulate the intricate tapestry of safety considerations that define each borough's transportation landscape.
    ''')

    bor = dfz['BOROUGH'].value_counts().reset_index()
    bor.columns = ['BOROUGH', 'COUNT',]
    colores = ['#191970','#483D8B','#4682B4','#87CEEB','#ADD8E6','#40E0D0','#7FFFD4']

    fig2 = px.pie(bor, names='BOROUGH', values='COUNT', color_discrete_sequence=colores,width=600, height=600, )
    st.title("Pie chart of crashes per borough")
    st.write(fig2)

    st.write('<div id="incidents"> </div>', unsafe_allow_html=True)
    st.write("Now we have an interactive bar graph that shows the different types of incidents, depending on the level of injure and the type of persons that were affected, this provides information that can show the type of transit of the street and the magnitudev of the incidents.")
    st.title('Traffic incidents by borough')
    borough_options = dfz['BOROUGH'].unique()
    selected_borough = st.selectbox('Select a borough:', borough_options)

    if selected_borough:
        filtered_data = dfz[dfz['BOROUGH'] == selected_borough]

        sums = filtered_data[['Persons Injured', 'Persons Killed',
                              'Pedestrians Injured', 'Pedestrians Killed',
                              'Cyclists Injured', 'Cyclists Killed',
                              'Motorists Injured', 'Motorists Killed']].sum()

        fig5 = px.bar(sums, x=sums.index, y=sums.values, labels={'y': 'Incident number',"x": 'Type of incident'}, title=f'Incidents in {selected_borough}')

        st.plotly_chart(fig5)
    else:
        st.warning('Please select a borough to visualize the data.')

#____________________Exploración por borough (pie y .........)__________________________
############################################################################################
#_________________Exploración por Causas (sunburst y barras con select box)________________
def pag_expcau():
  st.sidebar.markdown('''
  # Sections
  - [Home](#home)
  - [Summary](#summary)
  - [Sunburst](#sunburst)
  ''', unsafe_allow_html=True)
  st.write('<div id="summary"> </div>', unsafe_allow_html=True)
  st.write("""
    Various measures are implemented across the different boroughs to mitigate and reduce the number of collisions. 
    However, the effectiveness of these initiatives may be influenced by various factors, such as the accuracy and reliability of data capture methods. 
    Additionally, contingent factors specific to each borough can impact the overall outcomes of these measures. 
    It underscores the complexity of addressing collision rates, emphasizing the need for comprehensive strategies that consider both borough-specific dynamics and the reliability of data sources to create impactful and sustainable improvements in road safety.
  """)
  fig7 = px.scatter(dfz.groupby(['YEAR', 'BOROUGH']).size().reset_index(name='Count'),
                  x='YEAR', y='Count', color='BOROUGH', title='Collisions Count by Borough Over Years',
                  labels={'Count': 'Collision Count'})
  fig7.update_layout(height=800, width=1245)
  st.plotly_chart(fig7)
  st.write('<div id="sunburst"> </div>', unsafe_allow_html=True)
  st.write("Additional we have a sunburst graph in which we can explore the different areas or factors that we prefer, click on the different zones to access each of them.")

  sbfiltro = ['BOROUGH', 'Contributing Factor', 'Vehicle Type']
  dfsb = dfz[sbfiltro].copy()
  dfsb = dfsb[dfsb['BOROUGH'] != 'Unspecified']
  dfsb = dfsb[dfsb['Contributing Factor'] != 'Unspecified']
  dfsb = dfsb[dfsb['Vehicle Type'] != 'Unspecified']
  colores = ['#191970','#483D8B','#4682B4','#87CEEB','#ADD8E6','#40E0D0','#7FFFD4']
  fig6 = px.sunburst(dfsb, path=['BOROUGH', 'Contributing Factor', 'Vehicle Type'], color_discrete_sequence=colores, width=1000, height=1000)
  st.title("Exploration detailed data sunburst")
  st.write(fig6)
  st.write("According to the different variables, we are able to observe the different results, by manipulating all of these we can get insights and start making our own conclusions about our areas of interest")
#_________________Exploración por Causas (mapa y barras con select box)________________
############################################################################################
if menu == "Additional Exploration":
    pag_expcau()
elif menu == "Explore by borough":
    pag_expbor()
else:
    menu == "General Review"
    pag_genrev()
