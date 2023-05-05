import streamlit as st
from utilities.plots import *
import pandas as pd
import math

st.set_page_config(page_title="Mohr", layout="wide")

st.header("Determine C and Phi")
st.markdown(
    """1. Upload a csv file in the sidebar to the left. The table should be formatted with the following columns headings:

     |Sample ID|Test Number|Minor Principal Stress|Major Principal Stress|

2. Select a sample to plot from the menu below the file download button.
3. Use the sliders below to select an appropriate cohesion $$C$$ and friction angle $$\phi$$.
4. When you have made your selection, click the 'Record C and Phi' button to write the selections to a new table.
5. Continue steps 2 thru 4 until you have recorded all the values you want (you can redo any value at any time by simply selecting it again from the sample drop down menu).
6. Once you have made all your selections, click the 'Download results' button to the left to download the tabulated data to a csv."""
)

with st.sidebar:
    data = st.file_uploader("Choose a file")

    if data is not None:
        df = pd.read_csv(data)
    else:
        df = pd.read_csv("data\test.csv")

    sample_to_plot = st.selectbox("Select Sample to Plot", df["Sample ID"].unique())


if "Results" not in st.session_state:
    df_out = pd.DataFrame(df["Sample ID"].unique(), columns=["Sample ID"])
    st.session_state["Results"] = df_out

col1, col2 = st.columns(2)

with col1:
    cohesion_sample = st.slider("Pick a Cohesion Value", 0, 200, 1, key=0)
    friction_angle_sample = st.slider("Pick a Friction Angle", 20, 60, 1, key=1)
    with st.form("Slecter"):
        submitted = st.form_submit_button("Record C and Phi")

with col2:
    if submitted:
        index = (
            st.session_state["Results"]
            .index[st.session_state["Results"]["Sample ID"] == sample_to_plot]
            .tolist()[0]
        )
        st.session_state["Results"].at[index, "Cohesion"] = cohesion_sample
        st.session_state["Results"].at[index, "Friction Angle"] = friction_angle_sample
        st.write(st.session_state["Results"])

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


csv = convert_df(st.session_state["Results"])
with st.sidebar:
    st.download_button("Download results", csv, "MohrResults.csv", key="download-csv")
