import pandas as pd
from PIL import Image
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt



def show_description(species):
    @st.cache(suppress_st_warning=True)
    def _read_descriptions(species: str) -> str:
        with open(f'./descriptions/{species.lower()}_descriptions.txt', 'r') as f:
            return f.read()

    @st.cache(suppress_st_warning=True)
    def _load_images():
        st.write('Cache miss')
        images = {
            'Setosa': Image.open('./imgs/setosa.jpeg'),
            'Versicolor': Image.open('./imgs/versicolor.jpeg'),
            'Virginica': Image.open('./imgs/virginica.jpeg'),
        }
        return images

    col1, col2 = st.columns(2)
    description = _read_descriptions(species)
    images = _load_images()
    col1.header(species)
    col1.image(images[species], use_column_width=True)
    col2.header('Description')
    col2.write(description, unsafe_allow_html=True)


def home_page():
    st.title('Looking into Iris Dataset')
    st.image('./imgs/all_three.jpeg', caption='Three types of Iris flowers.')
    with st.expander('Show raw data'):
        st.write(df)
    st.header('General Information')
    selected_sepecies = st.radio('Select species', ['Setosa', 'Versicolor', 'Virginica'])
    show_description(selected_sepecies)


def dataset_page():
    st.title('Dataset')
    st.header('Statistics')
    stats_df = pd.concat([df.mean(), df.std()], axis=1, names=['mean', 'std']).rename(columns={0: 'mean', 1: 'std'})
    st.write(stats_df)


def graphs_page():
    st.title('Graphs')

    st.header('Seaborn (Matplotlib)')
    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=df, x='petal_width', y='petal_length', hue='species')
    st.pyplot(fig)

    st.header('*Can also support Altair, Plotly, and Bokeh')


if __name__ == '__main__':
    df = sns.load_dataset('iris')

    selected_page = st.sidebar.selectbox(
        'Select Page',
        ('Home', 'Dataset', 'Graphs')
    )

    if selected_page == 'Home':
        home_page()
    elif selected_page == 'Dataset':
        dataset_page()
    else:
        graphs_page()