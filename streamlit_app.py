
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('oscars_data.csv')
    return df

df = load_data()

# Set up the app layout
st.title("Visualizing the Academy Awards")
st.write("Explore the history of Oscar nominations and wins.")

# Add a toggle to choose between 'Nominated' and 'Winners'
option = st.radio("Select view:", ('All Nominations', 'Winners Only'))

# Determine the text for the subheader and filter the data
if option == 'Winners Only':
    header_text = 'Top N Most Wins'
    filtered_df = df[df['winner'] == 1]
else:
    header_text = 'Top N Most Nominated'
    filtered_df = df

# Filter further by year and category
year_range = st.slider('Select Year Range', min_value=int(df['year_film'].min()), max_value=int(df['year_film'].max()), value=(1929, 2024))
category = st.selectbox('Select Category', sorted(df['category'].unique()))
top_n = st.slider('Top N most nominated', min_value=1, max_value=20, value=10)

filtered_df = filtered_df[(filtered_df['year_film'] >= year_range[0]) & 
                          (filtered_df['year_film'] <= year_range[1]) & 
                          (filtered_df['category'] == category)]

# Aggregate data for visualization
nomination_counts = filtered_df.groupby(['name', 'film']).size().reset_index(name='Count')
nomination_counts = nomination_counts.groupby('name').agg({'Count': 'sum', 'film': lambda x: ', '.join(x)}).reset_index()
nomination_counts = nomination_counts.nlargest(top_n, 'Count')

# Sort by Count in descending order (already sorted by nlargest)
nomination_counts = nomination_counts.sort_values('Count', ascending=False)

# Plotting the data with Plotly
fig = px.bar(nomination_counts, x='Count', y='name', orientation='h',
             title=f"{header_text} in {category} ({year_range[0]}-{year_range[1]})",
             hover_data={'film': True}, 
             labels={'name': 'Nominee', 'Count': 'Number of Nominations' if option == 'All Nominations' else 'Number of Wins', 'film': 'Films'})

# Update layout to ensure proper sorting
fig.update_layout(yaxis={'categoryorder':'total ascending'},
                  height=600, width=800, 
                  yaxis_title='Nominee', 
                  xaxis_title='Number of Nominations' if option == 'All Nominations' else 'Number of Wins')

st.plotly_chart(fig)

# Display the raw data if needed
if st.checkbox('Show raw data'):
    st.write(filtered_df)
