'''
Solution unibrow.py
'''
import pandas as pd
import streamlit as st
import pandaslib as pl

st.title("UniBrow")
st.caption("The Universal data browser")

file = st.file_uploader("Upload a file:", type=["csv", "xlsx", "json"])
if file is not None:
    ext = pl.get_file_extension(file.name)
    df = pl.load_file(file, ext)

    st.write("## Original DataFrame")
    st.write(df.head())

    all_columns = pl.get_column_names(df)
    selected_columns = st.multiselect('Select columns to display', all_columns, default=all_columns)
    filtered_df = df[selected_columns]

    apply_filter = st.checkbox('Apply a filter to rows', value=False)
    if apply_filter:
        # Get object-type columns for filtering
        object_columns = pl.get_columns_of_type(filtered_df, 'object')
        if object_columns:
            filter_column = st.selectbox('Select column for filtering', object_columns)
            unique_values = pl.get_unique_values(filtered_df, filter_column)
            selected_value = st.selectbox('Select value to filter by', unique_values)
            filtered_df = filtered_df[filtered_df[filter_column] == selected_value]
        else:
            st.warning('No columns with categorical values available for filtering.')

    # Display filtered DataFrame
    st.write('### Filtered DataFrame')
    st.dataframe(filtered_df)

    # Display DataFrame description
    st.write('### DataFrame Description')
    st.write(filtered_df.describe(include='all'))