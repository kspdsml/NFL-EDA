import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NFL Data Explorer')

st.markdown("""
This app performs simple webscraping of NFL Football player stats data!
* **Python libraries:** base64, matplotlib, numpy, pandas, seaborn, streamlit
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', range(2022, 1990, -1))
selected_category = st.sidebar.selectbox('Category', ['passing', 'rushing', 'receiving'])
numerical_stats = {
    'passing': ['Age', 'Cmp', 'Att', 'Cmp%', 'Yds', 'TD', 'Int', 'Lng', 'Y/A', 'Y/G', 'Rate'],
    'rushing': ['Age', 'Att', 'Yds', 'TD', '1D', 'Lng', 'Y/A', 'Y/G', 'Fmb'],
    'receiving': ['Age','Tgt', 'Rec', 'Ctch%', 'Yds', 'Y/R', 'TD', '1D', 'Lng', 'Y/Tgt', 'R/G', 'Y/G', 'Fmb']
}
# Web scraping of NFL player stats
# https://www.pro-football-reference.com/years/2019/rushing.htm
@st.cache_data
def load_data(year, category):
    if category == 'rushing':
        # Column labels for rushing category
        # column_labels = {
        #     'Age': 'Age',
        #     'G': 'Games',
        #     'GS': 'Games Started',
        #     'Att': 'Attempts',
        #     'Yds': 'Yards',
        #     'TD': 'Touchdowns',
        #     '1D': 'First Downs',
        #     'Lng': 'Longest',
        #     'Y/A': 'Yards per Attempt',
        #     'Y/G': 'Yards per Game',
        #     'Fmb': 'Fumbles'
        # }

        url = "https://www.pro-football-reference.com/years/" + str(year) + "/" + category + ".htm"
        html = pd.read_html(url, header = 1)
        df = html[0]
        raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
        raw = raw.fillna(0)
        playerstats = raw.drop(['Rk'], axis=1)
        columns_to_convert = ['Age', 'G', 'GS', 'Att', 'Yds', 'TD', '1D', 'Lng', 'Y/A', 'Y/G', 'Fmb']
        playerstats[columns_to_convert] = playerstats[columns_to_convert].apply(pd.to_numeric, errors='coerce', downcast='integer')
        # playerstats = playerstats.rename(columns=column_labels)
        return playerstats
    
    elif category == 'passing':
        # Columns labels for passing category 
        # column_labels = {
        #     'Age': 'Age',
        #     'G': 'Games',
        #     'GS': 'Games Started',
        #     'Cmp': 'Completions',
        #     'Att': 'Attempts',
        #     'Cmp%': 'Completion Percentage',
        #     'Yds': 'Yards',
        #     'TD': 'Touchdowns',
        #     'Int': 'Interceptions',
        #     'Lng': 'Longest Completion',
        #     'Y/A': 'Yards per Attempt',
        #     'Y/C': 'Yards per Completion',
        #     'Y/G': 'Yards per Game',
        #     'Rate': 'Quarterback Rating'}
        url = "https://www.pro-football-reference.com/years/" + str(year) + "/" + category + ".htm"
        html = pd.read_html(url)
        df = html[0]
        raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
        raw = raw.fillna(0)
        playerstats = raw.drop(['Rk'], axis=1)
        playerstats = playerstats.drop(['Yds.1', 'QBrec', 'TD%', 'Int%', 'AY/A', 'QBR', 'Sk%', 'NY/A', 'ANY/A', '4QC', 'GWD'], axis=1)
        columns_to_convert = ['Age', 'G', 'GS', 'Cmp', 'Att', 'Cmp%', 'Yds', 'TD', 'Int', 'Lng', 'Y/A', 'Y/G', 'Rate']
        playerstats[columns_to_convert] = playerstats[columns_to_convert].apply(pd.to_numeric, errors='coerce', downcast='integer')
        # playerstats = playerstats.rename(columns=column_labels)

        return playerstats
    
    elif category == 'receiving':
        url = "https://www.pro-football-reference.com/years/" + str(year) + "/" + category + ".htm"
        html = pd.read_html(url)
        df = html[0]
        raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
        raw = raw.fillna(0)
        playerstats = raw.drop(['Rk'], axis=1)
        columns_to_convert = ['Age', 'G', 'GS', 'Tgt', 'Rec', 'Ctch%', 'Yds', 'Y/R', 'TD', '1D', 'Lng', 'Y/Tgt', 'R/G', 'Y/G', 'Fmb']
        playerstats[columns_to_convert] = playerstats[columns_to_convert].apply(pd.to_numeric, errors='coerce', downcast='integer')
        return playerstats



playerstats = load_data(selected_year, selected_category)


# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['RB','QB','WR','FB','TE']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# # Sidebar - Stat selection
# with st.sidebar:
#     st.write('Pick stat and range')
#     selected_stat = st.selectbox("", ('Age', 'G', 'GS', 'Att', 'Yds', 'TD', '1D', 'Lng', 'Y/A', 'Y/G', 'Fmb'))
#     # Convert minimum and maximum values to integers
#     start_stat = int(playerstats[selected_stat].min())-1
#     end_stat = int(playerstats[selected_stat].max())+1
#     start_range, end_range = st.select_slider(
#         '',
#         options= [str(num) for num in range(start_stat, end_stat)],
#         value=('33', '44')
#     )
# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header(f'Displaying {selected_year} NFL {selected_category.capitalize()} Stats')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')

st.dataframe(df_selected_team,)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

def generate_plot(x, y, data, visualization):
    if visualization == 'Scatter Plot':
        sns.set_style('darkgrid')
        sns.set_color_codes("pastel")
        sns.scatterplot(x=x, y=y, data=data)
        plt.title(f'{visualization} of {y} vs {x}')
        st.pyplot()

with st.container():
    st.write('Select graph type and data to compare:')
    visualization_options = ['Bar Chart', 'Scatter Plot', 'Box Plot']
    selected_visualization = st.selectbox('Visualization', visualization_options)
    stat_options = numerical_stats[selected_category]
    selected_x = st.selectbox('x var', stat_options)
    selected_y = st.selectbox('y var', stat_options)
    if st.button('Generate'):
        generate_plot(selected_x, selected_y, df_selected_team, selected_visualization)
    if st.button('Clear'):
        pass
# Heatmap
# if st.button('Intercorrelation Heatmap'):
#     st.header('Intercorrelation Matrix Heatmap')
#     df_selected_team.to_csv('output.csv',index=False)
#     df = pd.read_csv('output.csv')

#     corr = df.corr()
#     mask = np.zeros_like(corr)
#     mask[np.triu_indices_from(mask)] = True
#     with sns.axes_style("white"):
#         f, ax = plt.subplots(figsize=(7, 5))
#         ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
#     st.pyplot()

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 