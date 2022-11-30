from dash import dcc, html, dash_table, ctx
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Scheme, Group
from string import punctuation

from pandas.api.types import is_numeric_dtype

# App colors ----------------------------------------------------------------------------------------------------------:
seq_selected_color = "#7FFFD4"
plot_bg_color = "#FFFFFF"
ft_color = "#828282"
spinner_color = "#9966CC"
grid_color = "#FAF0E6"
pal = {
    "russian_violet": "#10003B",
    "russian_violet2": "#240046",
    "persian_indigo": "#3C096C",
    "purple": "#5A189A",
    "french_violet": "#7B2CBF",
    "amethyst": "#9D4EDD",
    "heliotrope": "#C77DFF",
    "mauve": "#E0AAFF"
}


def dcc_dropdown(id, searchable=True, multiple=False):
    """
    :parameter
    id [string] component id
    searchable [bool] If items in the dropdown can be searched.

    :return:  dcc dropdown component with no predefined options and values
    """
    return dcc.Dropdown(
        id=id,
        searchable=searchable,
        persistence=True,
        persistence_type="memory",
        multi=multiple,
    )


# Dashboard component functions ========================================================================================
def db_setting_button(id):
    return dbc.Button(
        html.I(className="bi bi-chevron-bar-expand"),
        id=id,
        class_name="mb-3 position-s-button",
        color="primary",
    )


def db_dcc_dropdown(id):
    return dcc.Dropdown(
        id=id,
        options=[{"label": "Average", "value": "mean"},
                 {"label": "Sum", "value": "sum"},
                 {"label": "Median", "value": "median"},
                 {"label": "Minimum", "value": "min"},
                 {"label": "Maximum", "value": "max"}],
        value="sum",
        searchable=True,
        persistence=True,
        persistence_type="memory",
    )


def db_dbc_radioitems(id):
    return dbc.RadioItems(
        id=id,
        options=[{"label": "Plot", "value": "plot"},
                 {"label": "Table", "value": "table"}],
        value="plot",
        # input_class_name="dash-control-bc",
        persistence=True,
        persistence_type="memory",
    )


def db_dbc_num_input(id):
    return dbc.Input(
        id=id,
        type="number",
        min=5, step=1, value=10,
        size="sm",
        # class_name="dash-control-bc",
        persistence=True,
        persistence_type="memory",
    )


def value_box(title: str, value: float):
    return dbc.Card(
        [
            html.H5(title, className="text-start text-muted"),
            dbc.CardBody(
                [
                    html.H2(
                        value,
                        className="text-center badge bg-secondary fs-5 rounded-3"  # rounded-pill
                    )
                ]
            )
        ],
        class_name="p-2 shadow-sm border-0"
    )


# Wangle product rule component functions ==============================================================================
def contains_rule_dropdown(id):
    return dcc.Dropdown(
        id=id,
        # options = [
        #     {"label": "Antecedents", "value": "antecedents"},
        #     {"label": "Consequents", "value": "consequents"},
        # ],
        searchable=True,
        persistence=True,
        persistence_type="memory",
    )


def contains_or_and_radioitems(id):
    return dbc.RadioItems(
        id=id,
        options=[
            {"label": "OR", "value": "|"},
            {"label": "AND", "value": "&"},
        ],
        persistence=True,
        persistence_type="memory",
        input_class_name="dash-control-bc"
    )


def query_matric_input(id, input_label):
    return dbc.InputGroup(
        [
            dbc.Input(
                id=id,
                type="number",
            ),
            dbc.InputGroupText(input_label)
        ],
        size="sm",
    )


# Callback Function ====================================================================================================
def add_query_matric_setting(elm_in_div, delete_btn_id, input_id, input_label_id, input_label, dropdown_id, radio_id):
    return html.Div(
        children=[
            dbc.Button(
                "X",
                id={
                    "type": delete_btn_id, "index": elm_in_div
                },
                n_clicks=0,
                style={"display": "block"},
            ),

            html.Label(
                input_label,
                id={
                    "type": input_label_id, "index": elm_in_div
                },
                style={"textAlign": "center"},
            ),
            dcc.Dropdown(
                id={
                    "type": dropdown_id, "index": elm_in_div
                },
                options=[
                    {"label": sign, "value": sign} for sign in [">", ">=", "<", "<=", "==", "!="]
                ],
                placeholder="Comparison Operator",
            ),

            dbc.Input(
                id={
                    "type": input_id, "index": elm_in_div
                },
                type="number",
                placeholder="number",
                class_name="dash-control-bc",
            ),

            html.Br(),

            dbc.RadioItems(
                id={
                    "type": radio_id, "index": elm_in_div
                },
                options=[
                    {"label": "OR", "value": "|"},
                    {"label": "AND", "value": "&"},
                ],
                input_class_name="dash-control-bc",
            ),

            html.Br(),
        ]
    )


def disable_fs_rule_type(opt1, opt2=None, typ="single"):
    """ Disable Option v """

    if typ == "single":
        return [
            {"label": str.title(col), "value": col, "disabled": col == opt1} for col in ["consequents", "antecedents"]
        ]
    elif typ == "double":
        variables = ["support", "confidence", "lift", "leverage", "conviction", "antecedent support",
                     "consequent support"]
        return [
            {"label": str.title(col), "value": col, "disabled": col in [opt1, opt2]} for col in variables
        ]


def create_description_table(m_dict, return_type, return_name):
    # return_name >> Analysis | Filtered Data
    if return_type == "rules":
        return f"""
         {return_name} returned **{m_dict['n_rules']:,}** rules.      

        | Metric | Minimum | Maximum |
        | --- | --- | --- |
        | Support | {m_dict['support'][0]:.5f} | {m_dict['support'][1]:.5f} |
        | Confidence |  {m_dict['confidence'][0]:.5f} | {m_dict['confidence'][1]:.5f} |
        | Lift | {m_dict['lift'][0]:.5f} | {m_dict['lift'][1]:.5f} |
        | Leverage | {m_dict['leverage'][0]:.5f} | {m_dict['leverage'][1]:.5f} |
        | Conviction | {m_dict['conviction'][0]:.5f} | {m_dict['conviction'][1]:.5f} |
        """

    elif return_type == "sup_len":
        return f"""
        Analysis returned {m_dict['n_itemsets']:,} unique itemset.    

        |  | Minimum | Maximum |
        | --- | --- | --- |
        | Support | {m_dict['support'][0]:.5f} | {m_dict['support'][1]:.5f} |
        | Number of products in an itemset |  {m_dict['length'][0]} | {m_dict['length'][1]} |
        """


def clean_column_names(df):
    clean_names = []

    for col in df.columns.to_list():
        for letter in col:
            if letter in punctuation:
                col = col.replace(letter, " ")
        clean_names.append(col.title())

    df.columns = clean_names
    return df


def create_dataframe(df, page_size=10, align_text="left", precision=2, increase_col_width=None, tbl_height=None,
                     tbl_width=None, change_tbl_color=None):
    d_tbl = clean_column_names(df)

    if increase_col_width is not None:
        cell_conditional = [{"if": {"column_id": increase_col_width[0]}, "width": increase_col_width[1]}]
    else:
        cell_conditional = []

    table_style = {"overflowX": "auto", "overflowY": "auto",
                   "border": "thin solid #FFFFFF"}  # "backgroudColor": "#9400D3"

    if tbl_height is not None:
        table_style["height"] = tbl_height

    if tbl_width is not None:
        table_style["width"] = tbl_width

    if change_tbl_color is not None:
        table_colors = change_tbl_color
    else:
        table_colors = [
            # Header
            {"backgroundColor": "#FFFFFF", "color": "#551A8B", "fontWeight": "bold",
             'borderBottom': '1px solid #912CEE'},
            # data condtional style
            {"if": {"row_index": "even"},
             "backgroundColor": "#FFFFF0",
             "color": "#551A8B",
             "border-left": "#FFFFF0",
             "border-right": "#FFFFF0"},
            {"if": {"row_index": "odd"},
             "backgroundColor": "#FFFFFF",
             "color": "#551A8B",
             "border-left": "#FFFFFF",
             "border-right": "#FFFFFF"},
        ]

    return html.Div(
        [
            dash_table.DataTable(
                data=d_tbl.to_dict("records"),
                columns=[
                    {"name": col, "id": col,
                     "format": Format(nully="N/A",
                                      precision=precision,
                                      scheme=Scheme.fixed,
                                      group=Group.yes,
                                      groups=3,
                                      ), "type": "numeric" if is_numeric_dtype(d_tbl[col]) else None} for col in
                    d_tbl.columns
                ],
                # {"specifier": ".2f"},
                page_size=page_size,
                style_table=table_style,
                fixed_rows={"headers": True},
                style_cell={"minWidth": 100,
                            "maxWidth": 700,
                            "width": 100,
                            "textAlign": align_text,
                            'textOverflow': 'ellipsis',
                            "border": "thin solid #FFFFFF"},
                style_header=table_colors[0],
                style_data_conditional=[
                    table_colors[1],
                    table_colors[2],
                ],
                style_cell_conditional=cell_conditional,
            )
        ]
    )


# {"backgroundColor": "#E8E8E8", "color": "0F0F0F", "fontWeight": "blue", 'borderBottom': '1px solid #595959'},
# {"if": {"row_index": "even"}, "backgroundColor": "#FAFAFA", "color": "#000000"},


def create_graph(graph_object):
    return html.Div(
        [
            dcc.Graph(figure=graph_object,
                      config={
                          "displaylogo": False,
                          "modeBarButtonsToRemove": ["pan2d", "lasso2d", "zoomIn2d", "zoomOut2d", "zoom2d", "toImage",
                                                     "select2d", "autoScale2d"]
                      }
                      )
        ]
    )


def toggle_plot_setting(num_clicks, is_open):
    if num_clicks:
        return not is_open
    return is_open


def add_filter_div(id_type, children_div, *args):
    if ctx.triggered_id is not None:
        button_id = ctx.triggered_id

        matrics_values = ["support", "confidence", "lift", "leverage", "conviction", "ant_support", "con_support"]

        for matric in matrics_values:
            if f"{id_type}_{matric}_add" == button_id:
                new_query = add_query_matric_setting(elm_in_div=len(children_div),
                                                     delete_btn_id=f"{id_type}_{matric}_del_btn",
                                                     input_id=f"{id_type}_value",
                                                     input_label_id=f"{id_type}_input_label",
                                                     input_label=f"{str.title(matric)}",
                                                     dropdown_id=f"{id_type}_comparison_opt",
                                                     radio_id=f"{id_type}_bitwise_opt")
                children_div.append(new_query)

        if isinstance(button_id, dict):
            children_div = [div for div in children_div if
                            f"'type': '{button_id['type']}', 'index': {button_id['index']}" not in str(div)]
    else:
        children_div.append(html.Div(children=[]))

    return children_div


# UI Function ==========================================================================================================
def filter_div(id_type):  # type = 'jq', 'gl'
    return html.Div(
        [
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            html.Label("First Rule Type"),
                            contains_rule_dropdown(id=f"{id_type}_f_rule_type"),

                            html.Label("First Product Values"),
                            dcc_dropdown(id=f"{id_type}_f_product_type", multiple=True),

                            html.Br(),

                            html.Label("Logical operator (Optional)"),
                            contains_or_and_radioitems(id=f"{id_type}_contains_bitwise_opt"),

                            html.Br(),

                            html.Label("Second Rule Type (Optional)"),
                            contains_rule_dropdown(id=f"{id_type}_s_rule_type"),

                            html.Label("Second Product Values (Optional)"),
                            dcc_dropdown(id=f"{id_type}_s_product_type", multiple=True),

                            html.Br(),

                            html.Label("Search Type"),
                            dbc.RadioItems(
                                id=f"{id_type}_contains_search_type",
                                options=[
                                    {"label": "Any", "value": "any"},
                                    {"label": "All", "value": "all"},
                                ],
                                value="any",
                                input_class_name="dash-control-bc",
                                persistence=True,
                                persistence_type="memory",
                            ),

                            html.Br(),
                            filter_dbc_button(id=f"{id_type}_filter_rule_contain_products"),
                        ],
                        title="Based On Product Name",
                        class_name="text-start",
                    ),

                    dbc.AccordionItem(
                        [
                            dbc.DropdownMenu(
                                [
                                    dbc.DropdownMenuItem("Support", id=f"{id_type}_support_add", n_clicks=0),
                                    dbc.DropdownMenuItem("Confidence", id=f"{id_type}_confidence_add", n_clicks=0),
                                    dbc.DropdownMenuItem("Lift", id=f"{id_type}_lift_add", n_clicks=0),
                                    dbc.DropdownMenuItem("Leverage", id=f"{id_type}_leverage_add", n_clicks=0),
                                    dbc.DropdownMenuItem("Conviction", id=f"{id_type}_conviction_add", n_clicks=0),
                                    dbc.DropdownMenuItem("Antecedent Support",
                                                         id=f"{id_type}_ant_support_add",
                                                         n_clicks=0),
                                    dbc.DropdownMenuItem("Consequent Support",
                                                         id=f"{id_type}_con_support_add",
                                                         n_clicks=0),
                                ],
                                label="Add Query",
                                direction="up"
                            ),

                            html.Div(id=f"{id_type}_query_dynamic_divs", children=[]),

                            html.Br(),

                            filter_dbc_button(id=f"{id_type}_filter_rule_query_metrics"),
                        ],
                        title="Query Metrics",
                        class_name="text-start",
                    ),

                    dbc.AccordionItem(
                        [
                            html.Label("Type Of rule"),
                            dcc.Dropdown(
                                id=f"{id_type}_len_rule_metric_type",
                                options=[
                                    {"label": str.title(rm), "value": rm} for rm in ["antecedents", "consequents"]
                                ],
                            ),

                            html.Br(),

                            html.Label("Comparison Operator"),
                            dcc.Dropdown(
                                id=f"{id_type}_rule_length_comp_opt",
                                options=[
                                    {"label": comp_opt, "value": comp_opt} for comp_opt in
                                    [">", ">=", "<", "<=", "==", "!="]
                                ],
                                searchable=True,
                                persistence=True,
                                persistence_type="memory",
                            ),

                            html.Br(),

                            html.Label("Number Of Product"),
                            dbc.Input(
                                id=f"{id_type}_length_products",
                                type="number",
                                min=1, max=5, step=1,
                                class_name="dash-control-bc",
                                persistence=True,
                                persistence_type="memory",
                            ),

                            dbc.Tooltip(
                                """
                                Value must 1 or greater.
                                """,
                                target=f"{id_type}_length_products",
                                placement="bottom",
                                delay={"hide": 100}
                            ),

                            html.Br(),

                            filter_dbc_button(id=f"{id_type}_filter_rule_rule_length"),
                        ],
                        title="Number Of Unique Product",
                        class_name="text-start",
                    ),
                ],
                start_collapsed=True
            ),
        ]
    )


def filter_dbc_button(id):
    return html.Div(
        [
            dbc.Button(
                id=id,
                children="Filter",
                n_clicks=0,
                color="success",
                class_name="me-1"
            ),
        ],
        className="d-grid gap-2",
    )


def rel_dcc_dropdown(id):
    variables = ["support", "confidence", "lift", "leverage", "conviction", "antecedent support", "consequent support"]
    return dcc.Dropdown(
        id=id,
        options=[
            {"label": str.title(var), "value": var} for var in variables
        ],
        searchable=True,
        persistence=True,
        persistence_type="memory",

    )
