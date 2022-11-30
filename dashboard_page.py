import dash
from dash import Input, Output, State, dcc, html, dash_table, ctx, ALL, MATCH
import dash_bootstrap_components as dbc

import ui_component as comp_fun
import function as mba_fun

dashboard_layout = html.Div(
    [
        dbc.Container(
            [
                html.Div(
                    [
                        dbc.NavbarSimple(
                            [
                                dbc.NavItem(dbc.NavLink("Home", href="/")),
                                dbc.NavItem(dbc.NavLink("Market Basket Analysis", href="/mba"))
                            ],
                            brand="Dashboard",
                            brand_href="/dashboard",
                            color="#68228B",
                            dark=True
                        ),
                    ]
                ),

                html.Br(),

                dbc.Row(
                    [
                        dbc.Col(
                            [],
                            id="n_transactions",
                            sm=12, md=6, lg=2, xl=2
                        ),

                        dbc.Col(
                            [],
                            id="n_unique_customers",
                            sm=12, md=6, lg=2, xl=2
                        ),

                        dbc.Col(
                            [],
                            id="total_sales",
                            sm=12, md=6, lg=2, xl=2
                        ),

                        dbc.Col(
                            [],
                            id="average_sales",
                            sm=12, md=6, lg=2, xl=2
                        ),

                        dbc.Col(
                            [],
                            id="n_unique_products",
                            sm=12, md=6, lg=2, xl=2
                        )
                    ],

                    class_name="g-1",
                    justify="between"
                ),

                html.Br(),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        comp_fun.db_setting_button(id="collapse_product_quantity_settings"),

                                        html.Br(),
                                        html.Br(),

                                        html.Div(
                                            [
                                                dbc.Collapse(
                                                    [
                                                        dbc.Card(
                                                            [
                                                                dbc.CardBody(
                                                                    [
                                                                        html.Label("Aggregate Type"),
                                                                        comp_fun.db_dcc_dropdown(
                                                                            id="product_quantity_agg"
                                                                        ),

                                                                        html.Br(),

                                                                        html.Label("Type Of Output"),
                                                                        comp_fun.db_dbc_radioitems(
                                                                            id="product_quantity_output_type"
                                                                        ),

                                                                        html.Br(),

                                                                        html.Label("Number Of Unique values"),
                                                                        comp_fun.db_dbc_num_input(
                                                                            id="product_quantity_nunique"
                                                                        ),
                                                                    ]
                                                                )
                                                            ],
                                                            class_name="""
                                                            float-sm-none float-md-none float-lg-end text-start
                                                            shadow-sm border-0
                                                            """,
                                                        )
                                                    ],

                                                    id="collapse_product_quantity_content",
                                                    is_open=False,
                                                )
                                            ],
                                        ),

                                        html.Br(),

                                        html.Div(id="product_quantity_output"),
                                    ],
                                    class_name="shadow-sm p-1 border-0"
                                )
                            ],
                            sm=12, md=12, lg=6, xl=6
                        ),

                        dbc.Col( # Most purchase products -------------------------------------------------------------|
                            [
                                dbc.Card(
                                    [
                                        comp_fun.db_setting_button(id="collapse_purchase_product_settings"),

                                        html.Br(),
                                        html.Br(),

                                        html.Div(
                                            [
                                                dbc.Collapse(
                                                    [
                                                        dbc.Card(
                                                            [
                                                                dbc.CardBody(
                                                                    [
                                                                        html.Label("Type Of Output"),
                                                                        comp_fun.db_dbc_radioitems(
                                                                            id="purchase_product_output_type"
                                                                        ),

                                                                        html.Br(),

                                                                        html.Label("Number Of Unique values"),
                                                                        comp_fun.db_dbc_num_input(
                                                                            id="purchase_product_nunique"
                                                                        ),
                                                                    ]
                                                                )
                                                            ],
                                                            class_name="""
                                                            float-sm-none float-md-none float-lg-end text-start
                                                            shadow-sm border-0
                                                            """,
                                                        )
                                                    ],

                                                    id="collapse_purchase_product_content",
                                                    is_open=False,
                                                )
                                            ],
                                        ),

                                        html.Br(),

                                        html.Div(id="product_purchase_output"),
                                    ],
                                    class_name="shadow-sm p-1 border-0"
                                )
                            ],
                            sm=12, md=12, lg=6, xl=6
                        )
                    ],
                    class_name="g-2",
                    justify="between"
                ),

                html.Br(),

                dbc.Row(
                    [
                        dbc.Col( # Most Profitable Product. -----------------------------------------------------------|
                            [
                                dbc.Card(
                                    [
                                        comp_fun.db_setting_button(id="collapse_profitable_product_settings"),

                                        html.Br(),
                                        html.Br(),

                                        html.Div(
                                            [
                                                dbc.Collapse(
                                                    [
                                                        dbc.Card(
                                                            [
                                                                dbc.CardBody(
                                                                    [
                                                                        html.Label("Aggregate Type"),
                                                                        comp_fun.db_dcc_dropdown(
                                                                            id="profitable_product_agg"
                                                                        ),

                                                                        html.Br(),

                                                                        html.Label("Type Of Output"),
                                                                        comp_fun.db_dbc_radioitems(
                                                                            id="profitable_product_output_type"
                                                                        ),

                                                                        html.Br(),

                                                                        html.Label("Number Of Unique values"),
                                                                        comp_fun.db_dbc_num_input(
                                                                            id="profitable_product_nunique"
                                                                        ),
                                                                    ]
                                                                )
                                                            ],
                                                            class_name="""
                                                                float-sm-none float-md-none float-lg-end text-start
                                                                shadow-sm border-0
                                                                """,
                                                        )
                                                    ],

                                                    id="collapse_profitable_product_content",
                                                    is_open=False,
                                                )
                                            ],
                                        ),

                                        html.Br(),

                                        dcc.Loading(
                                            html.Div(id="product_profitability_output"),
                                            id="product_profitability_spinner",
                                            color=comp_fun.spinner_color,
                                        ),
                                    ],
                                    class_name="shadow-sm p-1 border-0"
                                )
                            ],
                            sm=12, md=12, lg=10, xl=11
                        )
                    ],
                    class_name="g-1",
                    justify="center"
                )
            ],

            fluid=True
        )
    ]
)
