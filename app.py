import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(
    page_title = "Dados Meteorológicos da Cidade do Recife",
    layout = "wide",
    menu_items = {
        'About': "Em construção"
    }
)


st.title('Dados Meteorológicos da Região Metropolitana do Recife')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("By Kennedy Lins")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Volume de chuva por mês (mm)')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=12, range=(1,12))[1]
st.bar_chart(hist_values)


hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Mapa das estações de monitoramento')
st.map(filtered_data)