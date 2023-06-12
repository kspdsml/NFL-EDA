import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import utils

# Page Setup
st.title('NFL Data Explorer')

st.markdown("""
This app performs simple webscraping of NFL Football player stats data!
* **Python libraries:** base64, matplotlib, numpy, pandas, seaborn, streamlit
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
""")

# Sidebar - Filters
st.sidebar.header('Filters')
selected_year = st.sidebar.selectbox('Year', range(2022, 1990, -1))
selected_category = st.sidebar.selectbox('Category', ['passing', 'rushing', 'receiving'])

numerical_stats = {
    'passing': ['Age', 'Cmp', 'Att', 'Cmp%', 'Yds', 'TD', 'Int', 'Lng', 'Y/A', 'Y/G', 'Rate', 'QBR'],
    'rushing': ['Age', 'Att', 'Yds', 'TD', '1D', 'Lng', 'Y/A', 'Y/G', 'Fmb'],
    'receiving': ['Age', 'Tgt', 'Rec', 'Ctch%', 'Yds', 'Y/R', 'TD', '1D', 'Lng', 'Y/Tgt', 'R/G', 'Y/G', 'Fmb']
}
if selected_year < 2006:
    numerical_stats['passing'] = ['Age', 'Cmp', 'Att', 'Cmp%', 'Yds', 'TD', 'Int', 'Lng', 'Y/A', 'Y/G', 'Rate']

# Load and Filter Data
playerstats = utils.load_data(selected_year, selected_category)

sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

unique_pos = ['RB', 'QB', 'WR', 'FB', 'TE']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]
#numPlayers = len(playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))])
number = st.sidebar.slider("Number of Results", 1, len(df_selected_team), len(df_selected_team))



# Display Data
st.header(f'Displaying {selected_year} NFL {selected_category.capitalize()} Stats')
st.write('Data Dimension: ' + str(number) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')

st.dataframe(df_selected_team.head(number), hide_index=True)

st.markdown(utils.filedownload(df_selected_team), unsafe_allow_html=True)

# Visualization
with st.container():
    st.write('Select graph type and data to compare:')
    visualization_options = ['Bar Chart', 'Scatter Plot', 'Box Plot', 'Heatmap']
    selected_visualization = st.selectbox('Visualization', visualization_options)
    selected_x = None
    selected_y = None
    stat_options = numerical_stats[selected_category]
    
    if selected_visualization in ['Bar Chart', 'Scatter Plot', 'Box Plot']:
        selected_x = st.selectbox('x var', stat_options)
        selected_y = st.selectbox('y var', stat_options)
    

    
    if st.button('Generate'):
        utils.generate_plot(selected_x, selected_y, df_selected_team.head(number), selected_visualization)
    
    if st.button('Clear'):
        pass

# Hide Streamlit Style
hide_streamlit_style = """
<style>
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

