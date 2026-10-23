import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Predictive Forecasting of Care Load",
    layout="wide"
)

st.title("Predictive Forecasting of Care Load")
st.write(
    "A data analytics project using historical "
    "HHS care data to explore trends and forecast care load."
)

st.sidebar.header("Project Information")
st.sidebar.write("Project: Unified Mentor")
st.sidebar.write("Tools: Excel, Python, Google Colab")
st.sidebar.write("Target: Children in HHS Care")

uploaded_file = st.file_uploader(
    "Upload the project Excel dataset",
    type=["xlsx", "csv"]
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.subheader("Dataset Preview")
        st.dataframe(data.head(10), use_container_width=True)

        st.subheader("Dataset Information")
        st.write("Number of records:", len(data))
        st.write("Number of columns:", len(data.columns))

        st.subheader("Available Columns")
        st.write(list(data.columns))

        date_column = next(
            (c for c in data.columns if c.strip().lower() == "date"),
            None
        )

        target_column = next(
            (c for c in data.columns
             if "children in hhs care" in c.strip().lower()),
            None
        )

        if date_column and target_column:
            data[date_column] = pd.to_datetime(
                data[date_column], errors="coerce"
            )
            data[target_column] = pd.to_numeric(
                data[target_column], errors="coerce"
            )

            chart_data = data[
                [date_column, target_column]
            ].dropna().sort_values(date_column)

            st.subheader("Historical HHS Care Load")

            if not chart_data.empty:
                st.line_chart(
                    chart_data.set_index(date_column)[target_column]
                )

                st.metric(
                    "Latest recorded HHS care load",
                    f"{chart_data[target_column].iloc[-1]:,.0f}"
                )
            else:
                st.warning("No valid date and care-load values found.")
        else:
            st.info(
                "The expected Date and Children in HHS Care "
                "columns were not both found."
            )

    except Exception as e:
        st.error(f"Could not read the uploaded dataset: {e}")
else:
    st.info("Upload your Excel or CSV dataset to explore the data.")

st.caption(
    "Educational project. Charts describe historical data "
    "and do not represent a validated future forecast."
)
