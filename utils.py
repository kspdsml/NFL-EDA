import base64
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt



# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

# Web scraping of NFL player stats
# https://www.pro-football-reference.com/years/2019/rushing.htm
@st.cache_data
def load_data(year, category):
    if category == 'rushing':
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
        url = "https://www.pro-football-reference.com/years/" + str(year) + "/" + category + ".htm"
        html = pd.read_html(url)
        df = html[0]
        raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
        raw = raw.fillna(0)
        playerstats = raw.drop(['Rk'], axis=1)
        playerstats = playerstats.drop(['Yds.1', 'QBrec', 'TD%', 'Int%', 'AY/A', 'Sk%', 'NY/A', 'ANY/A', '4QC', 'GWD'], axis=1)
        if year > 2005:
            columns_to_convert = ['Age', 'G', 'GS', 'Cmp', 'Att', 'Cmp%', 'Yds', 'TD', 'Int', 'Lng', 'Y/A', 'Y/G', 'Rate', 'QBR']
        else:
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

def preprocess_data(playerstats, selected_team, selected_pos):
    pass

# def generate_plot(x, y, data, visualization):
#     conditional_hue = None
#     # if number <= 10:
#     #     conditional_hue = 'Player'
#     sns.set_style('darkgrid')
#     sns.set_color_codes("pastel")
#     if visualization == 'Scatter Plot':
#         sns.scatterplot(x=x, y=y, data=data, hue=conditional_hue)
#     elif visualization == 'Bar Chart':
#         sns.barplot(x=x, y=y, data=data, ci=None, hue=conditional_hue)
#     elif visualization == 'Box Plot':
#         sns.boxplot(x=x, y=y, data=data, hue=conditional_hue)
#     plt.title(f'{visualization} of {y} vs {x}')
    
    

#     st.pyplot()

def generate_plot(x_var, y_var, data, plot_type):
    plt.figure(figsize=(8, 6))
    
    if plot_type == 'Bar Chart':
        ax = sns.barplot(x=x_var, y=y_var, data=data)
        
    elif plot_type == 'Scatter Plot':
        c = alt.Chart(data).mark_circle().encode(
        x=x_var, y=y_var, tooltip=[x_var, y_var, 'Player']).interactive()
        st.write(f'{plot_type} representing {y_var} versus {x_var}')
        return st.altair_chart(c, use_container_width=True)
        
    elif plot_type == 'Box Plot':
        ax = sns.boxplot(x=x_var, y=y_var, data=data)
        
    # Adjust x-axis tick positions and labels for all chart types
    x_ticks = ax.get_xticks()
    x_tick_labels = ax.get_xticklabels()
    num_labels = len(x_tick_labels)
    interval = max(1, int(num_labels / 10))  # Choose interval based on number of labels
    ax.set_xticks(x_ticks[::interval])
    ax.set_xticklabels(x_tick_labels[::interval], rotation=45, ha='right')
    
    ax.set_xlabel(x_var)
    ax.set_ylabel(y_var)
    ax.set_title(f'{y_var} vs. {x_var}')
    st.write(f'{plot_type} representing {y_var} versus {x_var}')
    st.pyplot(plt)

    