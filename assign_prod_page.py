import dash
from dash import Input, Output, State, dcc, html, dash_table, ctx, ALL, MATCH
import dash_bootstrap_components as dbc

import ui_component as comp_fun

get_likely_products = dbc.Container(
    [
        html.Div(
            [
                dbc.NavbarSimple(
                    [
                        dbc.NavItem(dbc.NavLink("Home", href="/")),
                        dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard")),
                        dbc.NavItem(dbc.NavLink("Market Basket Analysis", href="/mba")),
                    ],
                    brand="Assign Products",
                    brand_href="/assign-products",
                    color="#68228B",
                    dark=True
                )
            ]
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.Label("Select Itemsets", className="fs-5 fw-bold ps-3 pt-2 text-muted"),

                                dbc.CardBody(
                                    [
                                        comp_fun.filter_div(id_type="gl"),

                                        html.Br(), html.Br(),

                                        dbc.InputGroup(
                                            [
                                                dbc.InputGroupText("Number of Rules",
                                                                   class_name="bg-primary",
                                                                   style={"color": "#FFFFFF"}),
                                                dbc.Input(
                                                    id="rule_range",
                                                    type="number",
                                                    min=1, max=10, step=1,
                                                    value=1,
                                                    persistence=True,
                                                    persistence_type="memory",
                                                ),
                                            ],
                                        ),

                                        dbc.Tooltip(
                                            """
                                            Maximum number of rows to extract rules from.
                                            """,
                                            target="rule_range",
                                            placement="top",
                                            delay={"hide": 100}
                                        ),

                                        html.Br(),

                                        html.Label("Extraction Arrangement"),

                                        dbc.RadioItems(
                                            id="rule_arrangement",
                                            options=[
                                                {"label": "Combine Itemset", "value": False},
                                                {"label": "Distinct Itemset", "value": True},
                                            ],
                                            value=False,
                                            input_class_name="dash-control-bc",
                                            persistence=True,
                                            persistence_type="memory",
                                        ),

                                        dbc.Tooltip(
                                            """
                                            Whether to treat each itemset as one or treat each itemset as a unique
                                            value.
                                            """,
                                            target="rule_arrangement",
                                            placement="top",
                                            delay={"hide": 100}
                                        ),

                                        html.Br(),

                                        html.Label("Create"),

                                        dbc.RadioButton(
                                            id="just_customer_id",
                                            label="Just Customer IDs"
                                        ),

                                        html.Br(),
                                        html.Br(),

                                        html.Div(
                                            [
                                                dbc.Button(
                                                    id="create_likely_purchase_products",
                                                    children="Assign",
                                                    n_clicks=0,
                                                    size="lg",
                                                    color="success",
                                                    class_name="me-1",
                                                ),
                                            ],
                                            className="d-grid gap-2",
                                        )
                                    ]
                                )
                            ],
                            class_name="border-secondary"
                        )
                    ],
                    sm=12, md=12, lg=3, xl=3,
                    class_name="text-start"
                ),

                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Div(id="filtered_rules_for_extraction"),
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
                                            id="mba_filtered_rules_table_description"
                                        ),
                                    ]
                                )
                            ],
                            class_name="border-secondary"
                        ),

                        html.Br(),
                        html.Br(),

                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Div(id="likely_product_purchase_output"),
                                    ]
                                )
                            ],
                            class_name="border-secondary"
                        ),
                    ],
                    sm=12, md=12, lg=9, xl=9
                )
            ]
        )
    ],
    fluid=True
)
