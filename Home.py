import streamlit as st
from utilities.plots import *
import pandas as pd
import math

st.set_page_config(page_title="Mohr", layout="wide")
st.write("Home")

with st.sidebar:
    data = st.file_uploader("Choose a file")

    if data is not None:
        df = pd.read_csv(data)
    sample_to_plot = st.selectbox("Select Sample to Plot", df["Sample ID"].unique())


if "DataFrame Out" not in st.session_state:
    df_out = pd.DataFrame(df["Sample ID"].unique(), columns=["Sample ID"])
    st.session_state["DataFrame Out"] = df_out

col1, col2 = st.columns(2)

with col1:
    cohesion_sample = st.slider("Pick a Cohesion Value", 0, 200, 1, key=0)
    friction_angle_sample = st.slider("Pick a Friction Angle", 20, 60, 1, key=1)
    with st.form("Slecter"):
        submitted = st.form_submit_button("Submit")

with col2:
    if submitted:
        index = (
            st.session_state["DataFrame Out"]
            .index[st.session_state["DataFrame Out"]["Sample ID"] == sample_to_plot]
            .tolist()[0]
        )
        st.session_state["DataFrame Out"].at[index, "Cohesion"] = cohesion_sample
        st.session_state["DataFrame Out"].at[
            index, "Friction Angle"
        ] = friction_angle_sample
        st.write(st.session_state["DataFrame Out"])

if sample_to_plot is not None:
    fig = plot_mohr_circles(df, sample_to_plot)
    fig = add_cohesion_and_friction_angle_to_mohr_circle(
        fig, cohesion_sample, friction_angle_sample
    )

else:
    fig = plot_empty_mohr_circle()

st.plotly_chart(fig)


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


csv = convert_df(st.session_state["DataFrame Out"])
with st.sidebar:
    st.download_button("Download results", csv, "MohrResults.csv", key="download-csv")
