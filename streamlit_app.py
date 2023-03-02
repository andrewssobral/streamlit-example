import numpy as np
import pandas as pd
import streamlit as st

from streamlit_autorefresh import st_autorefresh
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

if 'pre_selected_rows' not in st.session_state:
    st.session_state.pre_selected_rows = []

df = pd.DataFrame(columns=['ID', 'STATUS'])
df['ID'] = [1, 2, 3]
df['STATUS'] = np.random.randint(0,100,size=(3))
st.write(df)

# get pre-selected rows from session state
pre_selected_rows = st.session_state.pre_selected_rows
st.write("pre_selected_rows: ", pre_selected_rows)

# use the pre-selected rows when building the grid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True, wrapText=True, autoHeight=True)
gb.configure_column('ID', minWidth=80, maxWidth=80, type=["numericColumn","numberColumnFilter"], sortable=True, sort='asc', headerCheckboxSelection=True)
gb.configure_column('STATUS', minWidth=100, maxWidth=100)
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=3)
gb.configure_side_bar()
gb.configure_selection('multiple', pre_selected_rows=pre_selected_rows, rowMultiSelectWithClick=False, use_checkbox=True)
gb.configure_grid_options(suppressRowHoverHighlight=True, columnHoverHighlight=False, pre_selected_rows=pre_selected_rows)
gb_grid_options = gb.build()

# render the grid and get the selected rows
grid_return = AgGrid(
    df,
    gridOptions = gb_grid_options,
    key = 'ID',
    reload_data = True,
    data_return_mode = DataReturnMode.AS_INPUT,
    update_mode = GridUpdateMode.MODEL_CHANGED,
    allow_unsafe_jscode = True,
    fit_columns_on_grid_load = False,
    enable_enterprise_modules = False,
    height = 320,
    width = '100%',
    theme = "streamlit"
)
selected_rows = grid_return["selected_rows"]

# print the selected rows
st.write("Selected rows: ", selected_rows)

# save the row indexes of the selected rows in the session state
pre_selected_rows = []
for selected_row in selected_rows:
        pre_selected_rows.append(selected_row['_selectedRowNodeInfo']['nodeRowIndex'])
st.session_state.pre_selected_rows = pre_selected_rows

# Refresh streamlit components every 1s
st_autorefresh(interval=((1*1*1000)), key="dataframerefresh")
