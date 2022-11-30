import dash
from dash import Input, Output, State, dcc, html, dash_table, ctx, ALL, MATCH
import dash_bootstrap_components as dbc


home_content = html.Div(
    [
        dbc.Container(
            [
                html.Br(),

                html.Div(
                    html.H2("Market Basket Analysis"),
                    className="h1 text-center",
                    style={"color": "#551A8B"}
                ),

                html.Br(),
                html.Br(),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        html.H5("Grouped Product Data"),
                                        dbc.NavLink(
                                            [
                                                dbc.Button("USE DATA", id="use_product", n_clicks=0),
                                            ],
                                            href="/dashboard", active="exact"
                                        ),

                                        html.Br(),

                                        html.P(
                                            [
                                                """
                                                This data categorise all products with various variation into a single group,
                                                Unifying all difference. click
                                                """,
                                                html.Span("here",
                                                          id="open_grouped_modal",
                                                          n_clicks=0,
                                                          className="modal-link-style"),
                                                " for more information."
                                            ]
                                        ),

                                        dbc.Modal(
                                            [
                                                dbc.ModalHeader(dbc.ModalTitle("Grouped Product Data"),
                                                                class_name="modal-style"),
                                                dbc.ModalBody(
                                                    dcc.Markdown(
                                                        """
                                                        The products are grouped in such a way that a single description 
                                                        is used for all variations.
                                                        Example:
                                                        The different types of berries such as *Blueberry*, *blackberry*,
                                                        *strawberry*, etc, the name of the brand such as *purple berry plc*,
                                                        *fresh-berries*, etc and other distinctive features such as size,
                                                        price, quantity and so on are grouped into a unique product name
                                                        called **'Berries'**.
                                                        """
                                                    ),
                                                ),
                                            ],
                                            id="grouped_modal",
                                            is_open=False,
                                            centered=True,
                                        )
                                    ],

                                    class_name="px-3 py-5 shadow-sm rounded border-0 mt-5"
                                )
                            ],

                            sm=12, md=12, lg=5, xl=5
                        ),

                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        html.H5("Lumped Product Data"),
                                        dbc.NavLink(
                                            [
                                                dbc.Button("USE DATA", id="use_product_tax", n_clicks=0)
                                            ],
                                            href="/dashboard", active="exact"
                                        ),

                                        html.Br(),

                                        html.P(
                                            [
                                                """
                                                This data differentiate products based on their characteristics.
                                                click here for more information. click
                                                """,
                                                html.Span("here", id="open_tax_modal", n_clicks=0,
                                                          className="modal-link-style"),
                                                " for more information.",
                                            ],
                                        ),

                                        dbc.Modal(
                                            [
                                                dbc.ModalHeader(dbc.ModalTitle("Lumped Product Data"),
                                                                class_name="modal-style"),
                                                dbc.ModalBody(
                                                    dcc.Markdown(
                                                        """
                                                        Characteristics such as the product brand, price, type, size,
                                                        quantity, style, etc are used to differentiate each product
                                                        based on the stock-keeping Unit (SKU).  
                                                            Then a combination of the less frequent product is applied
                                                        all over such that each item put into the basket analysis
                                                        occurs with an almost similar level of support. This is done
                                                        to aggregating low-support items into groups and  analyzing the
                                                        group as a single item.  
  
                                                        Example:
                                                        The following list of products with their support levels:
                                                        - blueberry with 50%
                                                        - blackberry with 45%
                                                        - strawberry with 10%
                                                        - Raspberry with 15%

                                                        will be aggregated into:
                                                        - blueberry 50%
                                                        - blackberry 45%
                                                        - berries (others) 25%

                                                        Another motivation for such arrangement is majorly for 
                                                        computational purpose.
                                                        """
                                                    )
                                                ),
                                            ],
                                            id="tax_modal",
                                            is_open=False,
                                            scrollable=True,
                                            centered=True,
                                        )
                                    ],

                                    class_name="px-3 py-5 shadow-sm rounded border-0 mt-5"
                                )
                            ],

                            sm=12, md=12, lg=5, xl=5
                        )
                    ],

                    class_name="g-4",
                    justify="center"
                )
            ],
            fluid=True
        )
    ]
)
