import dash
from dash import Input, Output, State, dcc, html, dash_table, ctx, ALL, MATCH
import dash_bootstrap_components as dbc

import function as mba_fun
import ui_component as comp_fun

run_mba_analysis = dbc.Container(
    [
        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Label("Minimum Support"),

                                        dbc.Input(
                                            id="min_support",
                                            type="number",
                                            min=0.0001, max=0.009, step=0.0001,
                                            value=0.005,
                                            class_name="dash-control-bc",
                                            persistence=True,
                                            persistence_type="memory",
                                        ),

                                        dbc.Tooltip(
                                            """
                                            Filter out items with <= the input support. Value must be between 0 and 1
                                            """,
                                            target="min_support",
                                            placement="top",
                                            delay={"hide": 100}
                                        ),

                                        html.Br(),

                                        html.Label("Maximum Length"),

                                        dbc.Input(
                                            id="max_length",
                                            type="number",
                                            min=1,
                                            class_name="dash-control-bc",
                                            persistence=True,
                                            persistence_type="memory",
                                        ),

                                        dbc.Tooltip(
                                            """
                                            Maximum length of the generated itemsets. If empty, all possible itemsets 
                                            are evaluated.
                                            """,
                                            target="max_length",
                                            placement="right",
                                            delay={"hide": 200}
                                        ),

                                        html.Br(),

                                        html.Label("Metric Rule"),

                                        dcc.Dropdown(
                                            id="rule_metric",
                                            options=[
                                                {"label": str.title(rule), "value": rule} for rule in
                                                ["support", "confidence", "lift", "leverage", "conviction"]
                                            ],
                                            value="lift",
                                            searchable=True,
                                            persistence=True,
                                            persistence_type="memory",
                                        ),

                                        dbc.Tooltip(
                                            """
                                            Metric to evaluate if a rule is of interest.
                                            """,
                                            target="rule_metric",
                                            placement="right",
                                            delay={"hide": 100}
                                        ),

                                        html.Br(),

                                        html.Label("Minimum Threshold"),

                                        dbc.Input(
                                            id="min_threshold",
                                            type="number",
                                            class_name="dash-control-bc",
                                            persistence=True,
                                            persistence_type="memory",
                                        ),

                                        dbc.Tooltip(
                                            """
                                            Minimal threshold for the evaluation metric, via the `Metric Rule` value, to  
                                            decide whether a candidate rule is of interest.
                                            """,
                                            target="min_threshold",
                                            placement="right",
                                            delay={"hide": 200}
                                        ),

                                        html.Br(),

                                        html.Label("Type Of Output"),

                                        dbc.RadioItems(
                                            id="mba_analysis_output_type",
                                            options=[
                                                {"label": "Rules", "value": "rules"},
                                                {"label": "Support Length", "value": "sup_len"},
                                            ],
                                            value="rules",
                                            input_class_name="dash-control-bc",
                                            persistence=True,
                                            persistence_type="memory",
                                        ),

                                        html.Br(),

                                        html.Div(
                                            [
                                                dbc.Button(
                                                    id="create_mba_rules",
                                                    children="Create",
                                                    n_clicks=0,
                                                    color="success",
                                                    class_name="me-1"
                                                ),
                                            ],
                                            className="d-grid gap-2",
                                        ),
                                    ]
                                )
                            ],
                            class_name="text-start border-secondary"
                        )
                    ],
                    sm=12, md=12, lg=3, xl=3
                ),

                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dcc.Loading(
                                            html.Div(id="mba_analysis_output", ),
                                            id="mba_analysis_spinner",
                                            color=mba_fun.spinner_color,
                                        ),
                                    ]
                                )
                            ],
                            class_name="border-secondary"
                        ),

                        html.Br(),

                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dcc.Markdown(
                                            id="mba_analysis_table_description"
                                        ),
                                    ]
                                )
                            ],
                            class_name="text-start border-secondary"
                        )
                    ],
                    sm=12, md=12, lg=9, xl=9
                )
            ]
        )
    ],
    fluid=True
)

mba_rules_filter_summary = dbc.Container(
    [
        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.Label("Filter rules", className="fs-5 fw-bold ps-3 text-muted"),

                                dbc.CardBody(
                                    [
                                        comp_fun.filter_div(id_type="jq"),

                                        html.Br(),

                                        html.Label("Plot rules", className="fs-5 fw-bold mb-2 text-muted"),
                                        html.Br(),

                                        html.Label("X Variable"),

                                        comp_fun.rel_dcc_dropdown(id="x_variable"),

                                        html.Br(),

                                        html.Label("Y Variable"),

                                        comp_fun.rel_dcc_dropdown(id="y_variable"),

                                        html.Br(),

                                        html.Label("Z Variable (Optional)"),

                                        comp_fun.rel_dcc_dropdown(id="z_variable"),

                                        html.Br(),

                                        html.Label("Opacity (Optional)"),

                                        dbc.Input(
                                            id="rel_plt_opacity",
                                            type="number",
                                            min=0, max=1,
                                            persistence=True,
                                            persistence_type="memory",
                                        ),

                                        html.Br(),

                                        dbc.Button(
                                            children="Create Plot",
                                            id="create_rel_plot",
                                            n_clicks=0,
                                            size="lg",
                                            color="success",
                                            class_name="me-1",
                                        )
                                    ]
                                )
                            ],
                            class_name="text-start border-secondary"
                        )
                    ],
                    sm=12, md=12, lg=3, xl=3
                ),

                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dcc.Loading(
                                            html.Div(id="mba_query_output", ),
                                            id="mba_query_spinner",
                                            color=mba_fun.spinner_color,
                                        )
                                    ]
                                )
                            ],
                            class_name="border-secondary"
                        ),

                        html.Br(),

                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dcc.Markdown(
                                            id="mba_query_table_description"
                                        )
                                    ]
                                )
                            ],
                            class_name="border-secondary text-start"
                        ),

                        html.Br(),

                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dcc.Loading(
                                            html.Div(id="metric_relationship_plot"),
                                            id="metric_rel_spinner",
                                            color=mba_fun.spinner_color,
                                        ),
                                    ]
                                )
                            ],
                            class_name="border-secondary"
                        )
                    ],
                    sm=12, md=12, lg=9, xl=9
                )
            ]
        )
    ],
    fluid=True
)

mba_analysis_layout = html.Div(
    [
        html.Div(
            [
                dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink("Home", href="/")),
                        dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard")),
                        dbc.NavItem(dbc.NavLink("Assign Products", href="/assign-products")),
                    ],
                    brand="Market Basket Analysis",
                    brand_href="/mba",
                    color="#68228B",
                    dark=True
                ),
            ]
        ),

        dbc.Tabs(
            [
                dbc.Tab(
                    run_mba_analysis,
                    label="Market Basket Analysis",
                    tab_class_name="tab-inactive-style",
                    label_class_name="label-inactive-style",
                    active_tab_class_name="tab-active-style",
                    active_label_class_name="label-active-style",
                ),

                dbc.Tab(
                    mba_rules_filter_summary,
                    label="View Rules",
                    tab_class_name="tab-inactive-style",
                    label_class_name="label-inactive-style",
                    active_tab_class_name="tab-active-style",
                    active_label_class_name="label-active-style",
                ),
            ],
            persistence=True,
            persistence_type="memory",
        ),

        html.Br(),
    ]
)
