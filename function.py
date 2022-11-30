from pandas import DataFrame, concat
from numpy import nan
from collections import Counter
import warnings
from plotly.express import bar, scatter
from mlxtend.frequent_patterns import apriori, association_rules

from ui_component import seq_selected_color as seq_selected_color
from ui_component import plot_bg_color as plot_bg_color
from ui_component import ft_color as ft_color
from ui_component import grid_color as g_color
from ui_component import spinner_color as spinner_color
from ui_component import pal as pal


def match_arg(x: str, valid_arg: list):
    """
    parameter
    ---------
    x:          An argument.
    valid_arg:  A list of valid values to match.
    """
    if not isinstance(valid_arg, list):
        raise TypeError(f"Expected a list from argument `valid_arg` but got {type(valid_arg)}")

    if isinstance(x, list):
        if not all([arg in valid_arg for arg in x]):
            raise ValueError(f"'{x}' is not a valid value. use any of : {', '.join(valid_arg)}")
    else:
        if x not in valid_arg:
            raise ValueError(f"'{x}' is not a valid value. use any of : {', '.join(valid_arg)}")


def create_data_info(df: DataFrame, info_type: str, round_val: int = 2):
    """
    parameter
    ---------
    df:        Transaction dataframe.
    info_type: The type of info to return. any of "no_transaction", "no_unique_customers",
               "total_sales", "average_sales", "unique_products".
    round_val: Round output value.

    return
    ------
    An Integer or a float value.
    """

    match_arg(info_type, ["no_transaction", "no_unique_customers", "total_sales", "average_sales", "unique_products"])

    if info_type == "no_transaction":
        output = df.shape[0]
    elif info_type == "no_unique_customers":
        output = df["Customer_ID"].nunique()
    elif info_type == "total_sales":
        output = df["Sales_Amount"].sum()
    elif info_type == "average_sales":
        output = df["Sales_Amount"].mean()
    elif info_type == "unique_products":
        if "Unique_Product" in df.columns.to_list():
            output = df["Product_Taxonomy"].nunique()
        else:
            output = df["Product"].nunique()

    if round_val is not None:
        output = round(output, round_val)

    return f"{output:,}"


def get_product_variable(df: DataFrame):
    if "Product_Taxonomy" in df.columns.to_list():
        return "Product_Taxonomy"
    else:
        return "Product"


def most_purchased_products(df: DataFrame, output_type: str = None,
                            max_unique_value: int = 10,
                            seq_color: list = seq_selected_color,
                            bg_color: str = plot_bg_color,
                            font_color: str = ft_color,
                            grid_color: str = g_color):
    """
    parameter
    ---------
    df: product data.
    output_type: The type of output to return. Either a 'table' or a 'plot'.
    max_unique_value: The number of unique product values to display.
    p_color: Bar color.
    grid_color: color of the x-axis grid line.

    value
    -----
    A pandas dataframe or a plotly.graph_objects.Figure.
    """
    match_arg(output_type, ["plot", "table"])

    product = get_product_variable(df)

    f_tbl = (
        df[product]
            .value_counts()
            .reset_index()
            .rename(columns={"index": product, product: "Count"})
            .sort_values("Count", ascending=False)
    )

    f_tbl["Proportion"] = round(f_tbl["Count"] / f_tbl["Count"].sum() * 100, 3)

    if output_type == "plot":
        f_ptbl = f_tbl.sort_values("Count", ascending=True).tail(max_unique_value)

        f_fig = bar(
            data_frame=f_ptbl,
            x="Count",
            y=product,
            color_discrete_sequence=[seq_color],
            # labels={product: str.replace(product, "_", " ").title()},
            labels={"Count": "", product: ""},
            hover_data={product: False, "Proportion": ":.2f", "Count": True},
            title=f"Top {max_unique_value} Products Purchased By Customers Using Number Of Transactions",
            template="plotly_white",
            height=467,
        )
        f_fig.update_layout(plot_bgcolor=bg_color, paper_bgcolor=bg_color, title_font_color=font_color)
        f_fig.update_yaxes(color=font_color, showgrid=False)
        f_fig.update_xaxes(color=font_color, showgrid=True, gridwidth=1, gridcolor=grid_color)
        f_fig.update_traces(
            hovertemplate=f"{product}: %{{label}}: <br>count : %{{value:,.0f}} </br>proportion : %{{customdata:.2f}}%"
        )

        return f_fig

    elif output_type == "table":
        return f_tbl


def most_profitable_product(df: DataFrame,
                            agg_function: str = "sum",
                            output_type: str = None,
                            max_unique_value: int = 10,
                            seq_color: list = seq_selected_color,
                            bg_color: str = plot_bg_color,
                            font_color: str = ft_color,
                            grid_color: str = g_color):
    """
    parameter
    ---------
    df: Product data.
    agg_function: Aggregate function.
    output_type: The type of output to return. Either a 'table' or a 'plot'.
    max_unique_value: The number of unique product values to display.
    seq_color: bar colors.
    bg_color: plot background color.
    font_color: plot font color.
    grid_color: color of the x-axis grid line.

    value
    -----
    A pandas dataframe or a plotly.graph_objects.Figure.
    """

    match_arg(output_type, ["plot", "table"])
    match_arg(agg_function, ["sum", "mean", "median", "min", "max"])

    product = get_product_variable(df)

    agg_fun_name = {"sum": "Total", "mean": "Average", "median": "Median", "min": "Minimum", "max": "Maximum"}

    summary_variable = f"{agg_fun_name[agg_function]}_Sales_Amount"

    f_tbl = (
        df
            .groupby(product)["Sales_Amount"]
            .agg(agg_function)
            .reset_index()
            .rename(columns={"Sales_Amount": summary_variable})
            .sort_values(summary_variable, ascending=False)
    )

    f_tbl["Proportion"] = round(f_tbl[summary_variable] / f_tbl[summary_variable].sum() * 100, 3)

    if output_type == "plot":
        f_ptbl = f_tbl.sort_values(summary_variable, ascending=True).tail(max_unique_value)
        summary_label = str.replace(summary_variable, "_", " ")

        f_fig = bar(
            data_frame=f_ptbl,
            x=summary_variable,
            y=product,
            hover_data=[product, summary_variable, "Proportion"],
            color_discrete_sequence=[seq_color],
            # labels={summary_variable: summary_label, product: str.replace(product, "_", " ").title()},
            labels={summary_variable: "", product: ""},
            title=f"Top {max_unique_value} Products By {agg_fun_name[agg_function]} Amount Of Sales",
            template="plotly_white"
        )
        f_fig.update_layout(plot_bgcolor=bg_color, paper_bgcolor=bg_color, title_font_color=font_color)
        f_fig.update_yaxes(color=font_color, showgrid=False)
        f_fig.update_xaxes(color=font_color, showgrid=True, gridwidth=1, gridcolor=grid_color)
        f_fig.update_traces(
            hovertemplate=f"{product} : %{{label}}: <br>{summary_label} : %{{value:,.2f}} </br>Proportion: %{{customdata:.2f}}%"
        )

        return f_fig

    elif output_type == "table":
        return f_tbl


def product_quantity(df: DataFrame,
                     agg_function: str = "mean",
                     output_type: str = None,
                     max_unique_value: int = 10,
                     seq_color: list = seq_selected_color,
                     bg_color: str = plot_bg_color,
                     font_color: str = ft_color,
                     grid_color: str = g_color):
    """
    parameter
    ---------
    df: product data.
    agg_function: The type of aggregate function. any of "sum", "mean", "median", "min", "max".
    output_type: The type of output to return. Either a 'table' or a 'plot'.
    max_unique_value: The number of unique product values to display.
    seq_color: bar colors.
    bg_color: plot background color.
    font_color: plot font color.
    grid_color: color of the x-axis grid line.

    value
    -----
    A pandas dataframe or a plotly.graph_objects.Figure.
    """

    match_arg(output_type, ["plot", "table"])
    match_arg(agg_function, ["sum", "mean", "median", "min", "max"])

    product = get_product_variable(df)

    agg_fun_name = {"sum": "Total", "mean": "Average", "median": "Median", "min": "Minimum", "max": "Maximum"}

    summary_variable = f"{agg_fun_name[agg_function]}_Quantity"

    f_tbl = (
        df
            .groupby(product)[["Quantity"]]
            .agg(agg_function)
            .reset_index()
            .sort_values(by="Quantity", ascending=False)
            .rename(columns={"Quantity": summary_variable})
    )

    f_tbl["Proportion"] = round(f_tbl[summary_variable] / f_tbl[summary_variable].sum() * 100, 3)

    if output_type == "plot":
        f_ptbl = f_tbl.sort_values(summary_variable, ascending=True).tail(max_unique_value)
        quantity_summary = str.replace(summary_variable, "_", " ")

        f_fig = bar(
            data_frame=f_ptbl,
            x=summary_variable,
            y=product,
            color_discrete_sequence=[seq_color],
            hover_data={product: False, "Proportion": ":.2f"},
            # labels={summary_variable: quantity_summary, product: str.replace(product, "_", " ").title()},
            labels={summary_variable: "", product: ""},
            title=f"Top {max_unique_value} {agg_fun_name[agg_function]} Quantity Ordered For Each Product",
            template="plotly_white",
            height=467,
        )
        f_fig.update_layout(plot_bgcolor=bg_color, paper_bgcolor=bg_color, title_font_color=font_color)
        f_fig.update_yaxes(color=font_color, showgrid=False)
        f_fig.update_xaxes(color=font_color, showgrid=True, gridwidth=1, gridcolor=grid_color)
        f_fig.update_traces(hovertemplate="Quantity : %{value:,.2f} <br>Proportion : %{customdata:.2f}% </br>")

        return f_fig

    elif output_type == "table":
        return f_tbl


def create_association_rule(df: DataFrame,
                            min_support: float = 0.005,
                            max_length: int = None,
                            rule_metric: str = "lift",
                            min_threshold: float = 0.7,
                            output_type: str = "rules"):
    """
    parameter
    ---------
    min_support: The minimum support.
    max_length: Maximum length of the item-sets generated. passed to apriori.
    rule_metric: Metric to evaluate if a rule is of interest. can be any of "support", "confidence", "lift",
                 "leverage", "conviction".
    min_threshold: Minimal threshold for the evaluation metric.
    output_type: The type of table to return. either "rules" table or "sup_len"(support length) table.

    return
    ------
    A pandas dataframe.
    """

    match_arg(rule_metric, ["support", "confidence", "lift", "leverage", "conviction"])
    match_arg(output_type, ["rules", "sup_len"])

    product = get_product_variable(df)

    baskets = df[["Customer_ID", product, "Quantity"]].copy()

    baskets["Quantity"] = baskets["Quantity"].astype("int")

    baskets = baskets.pivot_table(
        index="Customer_ID",
        columns=product,
        values="Quantity",
        aggfunc="sum",
        fill_value=0
    )

    def encode_units(x):
        if x <= 0:
            return False
        if x >= 1:
            return True

    # min_support = 0.005 if min_support > 0.005 else min_support

    baskets = baskets.applymap(encode_units)

    itemsets = apriori(df=baskets, use_colnames=True, max_len=max_length, min_support=min_support, low_memory=True)

    if output_type == "sup_len":
        itemsets["length"] = itemsets["itemsets"].apply(lambda x: len(x))
        return itemsets

    elif output_type == "rules":
        try:
            rules = association_rules(df=itemsets, metric=rule_metric, min_threshold=min_threshold)

        except:
            warnings.warn("Minimum support value is too large.")
            rules = DataFrame(columns=["antecedents", "consequents", "antecedent support", "consequent support",
                                       "support", "confidence", "lift", "leverage", "conviction"])

        return rules


def filter_products_contain(df: DataFrame,
                            search_type: str = "any",
                            f_rule_type: str = None,
                            f_product_type: str = None,
                            s_rule_type: str = None,
                            s_product_type: str = None,
                            bitwise_opt: str = None):
    """
    parameter
    ---------
    df Product association Rule data frame.
    search_type: The way to search if value is 'any' then any row with any of the values supplied will be returned
                 else if value is "all" then only rows that have all supplied values will be returned
    f_rule_type,s_rule_type: Either 'antecedents' or 'consequents'.
    f_product_type,s_product_type [list|string] The type of product(s) to search for.
    bitwise_opt: A bitwise operator. Either '|' or '&'.

    return
    ------
    A filtered pandas dataframe with only selected products by the type of rule.
    """

    if (s_rule_type is None or s_product_type is None) and bitwise_opt is not None:
        bitwise_opt = None

    if s_rule_type is not None and (s_product_type is None or bitwise_opt is None):
        s_rule_type = None

    if s_product_type is not None and (s_rule_type is None or bitwise_opt is None):
        s_product_type = None

    empty_tbl = DataFrame(
        columns=["Antecedents", "Consequents",
                 "Antecedent Support", "Consequent Support",
                 "Support", "Confidence", "Lift", "Leverage", "Conviction"],
        index=[0]
    )

    if search_type == "any":
        def valid_products(product_type):
            if isinstance(product_type, list):
                return "|".join(product_type)
            else:
                return "|".join([product_type])

        f_selected_product_types = valid_products(f_product_type)

        if s_rule_type is None and s_product_type is None and bitwise_opt is None:
            return df.loc[df[f_rule_type].astype("str").str.contains(f_selected_product_types)]

        elif s_rule_type is not None and s_product_type is not None and bitwise_opt is not None:
            match_arg(bitwise_opt, ["&", "|"])

            s_selected_product_types = valid_products(s_product_type)

            if bitwise_opt == "|":
                return df.loc[(df[f_rule_type].astype("str").str.contains(f_selected_product_types)) |
                              (df[s_rule_type].astype("str").str.contains(s_selected_product_types))]
            elif bitwise_opt == "&":
                return df.loc[(df[f_rule_type].astype("str").str.contains(f_selected_product_types)) &
                              (df[s_rule_type].astype("str").str.contains(s_selected_product_types))]
        else:
            return empty_tbl

    elif search_type == "all":
        def set_products(product_type):
            if not isinstance(product_type, list):
                return [product_type]
            else:
                return product_type

        f_selected_product_types = set(set_products(f_product_type))

        if s_rule_type is None and s_product_type is None and bitwise_opt is None:
            return df.loc[df[f_rule_type] == frozenset(f_selected_product_types)]

        elif s_rule_type is not None and s_product_type is not None and bitwise_opt is not None:
            match_arg(bitwise_opt, ["&", "|"])

            s_selected_product_types = set(set_products(s_product_type))

            if bitwise_opt == "|":
                return df.loc[(df[f_rule_type] == frozenset(f_selected_product_types)) |
                              (df[s_rule_type] == frozenset(s_selected_product_types))]
            elif bitwise_opt == "&":
                return df.loc[(df[f_rule_type] == frozenset(f_selected_product_types)) &
                              (df[s_rule_type] == frozenset(s_selected_product_types))]
        else:
            return empty_tbl


def within_range_values(df: DataFrame, var_dict: dict):
    """
    df: Product association rule data.
    var_dict: A dictionary with ... variables.
    """

    valid_range = []

    for var in var_dict.keys():
        valid_range.append(list(df[var].agg(["min", "max"]).values))

    for key, value, index in zip(var_dict.keys(), var_dict.values(), range(len(var_dict))):
        if value < valid_range[index][0] or value > valid_range[index][1]:
            raise ValueError(
                f"{key} values ({value}) is out of range. valid range is {valid_range[index][0]} - {valid_range[index][1]}"
            )


def get_query_values(metric: list, metric_value: list, comp_op: list, bitw_op: list = None):
    """
    parameter
    ---------
    metric [list[string]] A list of metric names.
    metric_value [list[float]] A list of metric values.
    comp_op: A list of comparison operators.
    bitw_op: A list of bitwise operators.

    value
    -----
    A list with 2 or 3 items.
    """

    # Helper Functions ------------------------------------------------------------------------------------------------:
    def get_invalid_index(lst: list):
        invalid_index = []

        for i, v in enumerate(lst):
            if v is None:
                invalid_index.append(i)

        return invalid_index

    def remove_value(none_index: list, pop_list: list):
        if len(none_index) == 1:
            invalid_indx = int(" ".join([str(indx) for indx in none_index]))

            pop_list_c = pop_list.copy()
            pop_list_c.pop(invalid_indx)

        elif len(none_index) > 1:
            pop_list_c = [valid_vals for indx, valid_vals in enumerate(pop_list) if indx not in none_index]

        return pop_list_c

    def get_selected_duplicate_index(dup_value: int, metrics: list):
        invalid_value_index = []

        for indx, value in enumerate(metrics):
            if value == dup_value:
                invalid_value_index.append(indx)

        return min(invalid_value_index)

    def in_index(supplied_index, list_value: list):
        list_index = []

        for i, v in enumerate(list_value):
            list_index.append(i)

        if len(supplied_index) == 1:
            indx = int(" ".join([str(x) for x in supplied_index]))

            return indx in list_index
        else:
            return all([x in list_index for x in supplied_index])

    # Dropping Duplicate metrics --------------------------------------------------------------------------------------:
    metric = [str.lower(m) for m in metric]

    if bitw_op == [None]:
        bitw_op = None

    check_dup = Counter(metric)
    dup_value = [indx for indx, val in check_dup.items() if val > 1]

    if dup_value:  # change dup_value != []:
        if len(dup_value) == 1:
            dup_value = " ".join(dup_value)
            invalid_index = get_selected_duplicate_index(dup_value, metric)
            invalid_index = [invalid_index]
        else:
            invalid_index = []
            for multi_value in dup_value:
                res = get_selected_duplicate_index(multi_value, metric)
                invalid_index.append(res)

        metric = remove_value(invalid_index, metric)
        metric_value = remove_value(invalid_index, metric_value)
        comp_op = remove_value(invalid_index, comp_op)

        if bitw_op is not None:
            invalid_index = [x - 1 for x in invalid_index]
            bitw_op = remove_value(invalid_index, bitw_op)

    # Drop initial None from the bitwise operator ---------------------------------------------------------------------:
    if bitw_op is not None:
        bitw_op = bitw_op[0:len(bitw_op) - 1]

    # Remove all none values from the metric values -------------------------------------------------------------------:
    metric_value_c = [mv for mv in metric_value if mv is not None]

    def get_valid_values(metric_c, metric_value_c: list, comp_op, bitw_op=bitw_op):
        # Checking if comparison operator have the same length as the query dict -------------:
        comp_op_c = [cp for cp in comp_op if cp is not None]

        if len(comp_op_c) != len(metric_c):
            none_cp_index = get_invalid_index(comp_op)
            if none_cp_index != []:
                metric_c = remove_value(none_cp_index, metric_c)
                metric_value_c = remove_value(none_cp_index, metric_value_c)

            if bitw_op is not None and none_cp_index != []:
                if in_index(none_cp_index, bitw_op):
                    bitw_op = remove_value(none_cp_index, bitw_op)

        # Checking if bitwise operator have 1-length of quary metric -------------------------:
        if bitw_op is not None:
            bitw_op_c = [bt for bt in bitw_op if bt is not None]

            if len(metric_c) == 1:
                bitw_op_c = []

            elif len(bitw_op_c) != len(metric_c) - 1:
                none_bt_index = get_invalid_index(bitw_op)

                if none_bt_index:  # change none_bt_index != []:
                    metric_c = remove_value(none_bt_index, metric_c)
                    metric_value_c = remove_value(none_bt_index, metric_value_c)
                    comp_op_c = remove_value(none_bt_index, comp_op_c)

        if bitw_op is None:
            return [metric_c, metric_value_c, comp_op_c]
        else:
            return [metric_c, metric_value_c, comp_op_c, bitw_op_c]

    # When no metric value is None ------------------------------------------------------------------------------------:
    if len(metric) == len(metric_value_c):
        metric_c = metric.copy()

        res_values = get_valid_values(metric_c, metric_value_c, comp_op, bitw_op)
        query_values = dict(zip(res_values[0], res_values[1]))
    # When metric value have None values ------------------------------------------------------------------------------:
    else:
        none_index = get_invalid_index(metric_value)
        metric_c = remove_value(none_index, metric)
        comp_op = remove_value(none_index, comp_op)

        if bitw_op is not None:
            if in_index(none_index, bitw_op):
                bitw_op = remove_value(none_index, bitw_op)

        res_values = get_valid_values(metric_c, metric_value_c, comp_op, bitw_op)
        query_values = dict(zip(res_values[0], res_values[1]))

    if bitw_op is None:
        return [query_values, res_values[2], []]
    else:
        return [query_values, res_values[2], res_values[3]]


def filter_rules_values(df: DataFrame, query_values: dict, comp_op: list, bitw_op: list):
    """
    parameter
    ---------
    df Product association rule data.
    query_values [dict] A dictionary with ... variable from `df` and their respective values.
    comp_op [list[string]] A list of comparison operators with same length as the length of query_values.
    bitw_op [list[string]] A list of bitwise operators with length(query_values)-1 .

    value
    -----
    A pandas dataframe with subset of the data `df` if condition is True.
    """

    if not isinstance(comp_op, list) or not isinstance(bitw_op, list):
        raise TypeError("argument `comp_op` and `bitw_op` must be a list.")

    if not isinstance(query_values, dict):
        raise TypeError("argument `query_values` must be a dictionary with variable names and the values to filter.")

    if len(comp_op) != len(query_values):
        raise ValueError("argument `comp_op` and `query_values` must be the same length.")

    if len(bitw_op) != len(query_values) - 1:
        raise ValueError(f"argument `bitw_op` must have {len(query_values) - 1} values.")

    within_range_values(df=df, var_dict=query_values)

    match_arg(comp_op, ["<", ">", ">=", "<=", "==", "!="])
    match_arg(bitw_op, ["&", "|"])

    bitw_op = [''] + bitw_op

    filter_queries = ""

    for c_key, c_value, comp, bitw in zip(query_values.keys(), query_values.values(), comp_op, bitw_op):
        filter_query = f"{bitw} ({c_key} {comp} {c_value})"
        filter_queries = filter_queries + " " + filter_query

    filter_queries = str.strip(filter_queries)

    return df.query(filter_queries)


def filter_rules_length(df: DataFrame, rule_type: str, comp_op: str, length: int):
    """
    parameter
    ---------
    df: Product association rule data.
    rule_type: The type of ...., can either 'antecedents' or 'consequents'.
    comp_op: A comparison operators.
    length: The amount of products.

    value
    -----
    A pandas dataframe with subset of the data `df` if condition is True.
    """

    match_arg(comp_op, ["<", ">", ">=", "<=", "==", "!="])

    f_tbl = df.copy()

    rule_var_name = f"{rule_type}_len"

    f_tbl[rule_var_name] = f_tbl[rule_type].apply(lambda x: len(x))

    filter_queries = f"{rule_var_name} {comp_op} {length}"

    return f_tbl.query(filter_queries)


def str_frozenset(df: DataFrame, df_type: str = "with_rules"):
    """
    parameter
    ---------
    df: product data.
    df_type: How to convert forzenset to string. either 'with_rules' or 'sup_len'

    return
    ------
    A pandas data with each value in antecedents and consequents as a string.
    """
    f_tbl = df.copy()

    if df_type == "with_rules":
        for rule in ["antecedents", "consequents"]:
            f_tbl[rule] = f_tbl[rule].apply(lambda x: f"({', '.join(x)})")

    elif df_type == "sup_len":
        f_tbl["itemsets"] = f_tbl["itemsets"].apply(lambda x: f"({', '.join(x)})")

    return f_tbl


def freeze_set(df: DataFrame):
    """
    parameter
    ---------
    df product data.

    return
    ------
    A pandas data with each value in antecedents and consequents as a frozenset.
    """

    # def as_frozenset(x):
    #     # out_x = x.strip("][").split(", ")
    #     return frozenset(x)

    f_tbl = df.copy()

    for rule in ["antecedents", "consequents"]:
        f_tbl[rule] = f_tbl[rule].apply(lambda x: frozenset(x))

    return f_tbl


def unfreez_set(df: DataFrame):
    """
    parameter
    ---------
    df product data.

    return
    ------
    A pandas data with each value in antecedents and consequents as a list.
    """
    f_tbl = df.copy()
    for rule in ["antecedents", "consequents"]:
        f_tbl[rule] = f_tbl[rule].apply(lambda x: list(x))

    return f_tbl


def extract_product_rules(df: DataFrame, rule_type: str, rule_range: int = None, by_row: bool = False):
    """
    parameters
    ----------
    df: product data.
    rule_type: The type of ...., can either 'antecedents' or 'consequents'.
    rule_range: A number to use as the maximum range of rows.
    by_row: Whether to extract products by row or by combining them.

    return
    ------
    A string or a list of products.
    """

    n_row = df.shape[0]

    if n_row > 0:
        if rule_range is None:
            selected_rule = df[rule_type][df.index[0]]

            if len(selected_rule) == 1:
                out_product = selected_rule[0]
            else:
                out_product = selected_rule

            return out_product
        else:
            c_df = df.copy()
            c_df = c_df.reset_index(drop=True)

            if n_row < rule_range:
                selected_products = df[rule_type][0:n_row]
            else:
                selected_products = df[rule_type][0:rule_range]

            if by_row:
                get_product_list = list(selected_products.values)

                out_product = []
                for prod in get_product_list:
                    if len(prod) == 1:
                        out_product.append(" ".join(prod))
                    else:
                        out_product.append(prod)
            else:
                out_product = list(set([prod for subProds in selected_products for prod in subProds]))
                out_product = out_product[0] if len(out_product) == 1 else out_product

            return out_product
    else:
        return []


def get_protential_customer_product(df: DataFrame,  # +++++++++++++++++++++
                                    ant_products: list = None,
                                    con_products: list = None,
                                    just_customer_id: bool = False):
    """
    df product data.
    ant_products: [list|string] Selected product(s) from the antecedents column.
    con_products: [list|string] Selected product(s) from the consequents column.
    just_customer_id: Whether to return just the customer id that meet all conditions.

    return
    ------
    A pandas dataframe with a new column of likely product the customer can purchase.
    """

    if ant_products == [] or con_products == []:
        rule_name = "antecedents" if ant_products == [] else "consequents"

        return DataFrame(
            {"Problem": [f"{rule_name} returned empty products, make sure all avaliable options have valid inputs"]}
        )

    c_df = df.copy()

    likely_purchase = ", ".join(con_products) if isinstance(con_products, list) else con_products

    product = get_product_variable(df=df)

    if not isinstance(ant_products, list):
        c_df = c_df.loc[c_df[product].str.contains(ant_products)]

        c_df["Likely_Product_Purchase"] = likely_purchase

    else:
        c_df = c_df.loc[c_df[product].str.contains("|".join(ant_products))]

        more_products = c_df["Customer_ID"].value_counts() > 1
        valid_customers = more_products[more_products == True].index

        valid_customer_df = c_df.loc[c_df["Customer_ID"].isin(valid_customers)]

        made_same_purchase = []

        for cus_id in list(valid_customer_df["Customer_ID"].unique()):
            get_customer_products = list(
                valid_customer_df.loc[valid_customer_df["Customer_ID"] == cus_id][product].values)

            if not Counter(get_customer_products) - Counter(ant_products):
                made_same_purchase.append(cus_id)

        c_df = valid_customer_df.loc[valid_customer_df["Customer_ID"].isin(made_same_purchase)].copy()

        c_df["Likely_Product_Purchase"] = likely_purchase

    if just_customer_id:
        return c_df.drop_duplicates(subset="Customer_ID").reset_index()[["Customer_ID"]]
    else:
        return c_df


def protential_customer_product(df: DataFrame,  # +++++++++++++++++++++
                                ant_products: list = None,
                                con_products: list = None,
                                just_customer_id: bool = False,
                                distinct_product_group: bool = False):
    """
    parameter
    ---------
    df product data.
    ant_products [list|string] Selected product(s) from the antecedents column.
    con_products [list|string] Selected product(s) from the consequents column.
    just_customer_id: Whether to return just the customer id that meet all conditions.
    distinct_product_group: If True, each product will be treated as a single potential product.

    return
    ------
    A pandas dataframe with a new column of likely product the customer can purchase.
    """

    if distinct_product_group:
        lpp_tbl = DataFrame()

        for ant_product, con_product in zip(ant_products, con_products):
            lpp_tbl = concat([lpp_tbl, get_protential_customer_product(df=df,
                                                                       ant_products=ant_product,
                                                                       con_products=con_product,
                                                                       just_customer_id=just_customer_id)])
    else:
        lpp_tbl = get_protential_customer_product(df=df,
                                                  ant_products=ant_products,
                                                  con_products=con_products,
                                                  just_customer_id=just_customer_id)

    return lpp_tbl


def lump_product_data(df: DataFrame, threshold: int = 60):
    """
    parameter
    ---------
    df: product association rules data.
    threshold: Every unique product sku count that fall below the threshold will be lumped together as 'Others'.

    return
    -------
    A pandas data frame with a lumped product and SKU category.
    """

    f_tbl = df.copy()

    f_tbl["Unique_Product"] = f_tbl[["Product", "SKU"]].apply("_".join, axis=1)

    f_tbl["Product_Taxonomy"] = nan

    for product in f_tbl["Product"].unique():
        ff = f_tbl.loc[f_tbl["Product"] == product]["Unique_Product"].value_counts() < threshold

        if len(ff.unique()) == 2:
            invalid_products = ff[ff == True].index.to_list()
            valid_products = ff[ff == False].index.to_list()

            f_tbl.loc[f_tbl["Unique_Product"].isin(invalid_products), "Product_Taxonomy"] = f"{product}_Others"
            f_tbl.loc[f_tbl["Unique_Product"].isin(valid_products), "Product_Taxonomy"] = \
                f_tbl.loc[f_tbl["Unique_Product"].isin(valid_products)]["Unique_Product"]

        else:
            true_len = ff[ff == True].shape[0]
            false_len = ff[ff == False].shape[0]

            if true_len > 0 and false_len == 0:
                invalid_products = ff[ff == True].index.to_list()

                f_tbl.loc[f_tbl["Unique_Product"].isin(invalid_products), "Product_Taxonomy"] = product

            elif true_len == 0 and false_len > 0:
                valid_products = ff[ff == False].index.to_list()

                f_tbl.loc[f_tbl["Unique_Product"].isin(valid_products), "Product_Taxonomy"] = \
                    f_tbl.loc[f_tbl["Unique_Product"].isin(valid_products)]["Unique_Product"]

            elif true_len == 1 and false_len == 1:
                same_products = ff.index.to_list()
                f_tbl.loc[f_tbl["Unique_Product"].isin(same_products), "Product_Taxonomy"] = product

            else:
                f_tbl["Product_Taxonomy"] = f_tbl["Unique_Product"]

    return f_tbl


def rules_relationship(df: DataFrame,
                       x_var: str,
                       y_var: str,
                       z_var: str = None,
                       opacity: float = None,
                       font_color: str = ft_color,
                       bg_color: str = plot_bg_color,
                       grid_color: str = g_color):
    """
    parameter
    ---------
    df: A dataframe with association rules.
    x_var,y_var,z_var: A variable from the dataframe `df`. z_var is optional.
    opacity: from 0 to 1,  the boldness of each points in the plot.
    font_color: plot font color.
    bg_color: plot background color.
    grid_color: color for the x-axis & y-axis grid.

    value
    -----
    A plotly.graph_objects.Figure object.
    """

    valid_variables = ["support", "confidence", "lift", "leverage", "conviction",
                       "antecedent support", "consequent support"]

    var_labels = []

    for lab in [x_var, y_var, z_var]:
        if lab is not None:
            var_labels.append(str.title(lab))

    # z_variable = None if z_var == "No Selection" else z_var
    def plotly_scatter(labs: str,
                       title: str,
                       hover_data: dict,
                       f_d_color: str = None,
                       f_c_color: str = None,
                       z_var: str = z_var):
        f_plt = scatter(
            data_frame=df,
            x=x_var,
            y=y_var,
            color=z_var,
            labels=labs,
            title=title,
            color_discrete_sequence=f_d_color,
            color_continuous_scale=f_c_color,
            hover_data=hover_data,
            opacity=opacity,
            template="plotly_white"
        )
        return f_plt

    if z_var is None:
        if len(set([x_var, y_var])) < 2:
            raise ValueError("argument `x_var` and `y_var` must be unique and not empty.")

        if not all([cols in valid_variables for cols in [x_var, y_var]]):
            raise ValueError("An Invalid variable argument was supplied")

        f_fig = plotly_scatter(
            f_d_color=["#FFD700"],
            labs={x_var: var_labels[0], y_var: var_labels[1]},
            title=f"Relationship between {var_labels[0]} & {var_labels[1]} For {df.shape[0]:,} Rules",
            hover_data={x_var: ":.4f", y_var: ":.4f"},
        )

    else:
        if len(set([x_var, y_var, z_var])) < 3:
            raise ValueError("argument `x_var`, `y_var` and `z_var` must be unique and not empty.")

        if not all([cols in valid_variables for cols in [x_var, y_var, z_var]]):
            raise ValueError("An Invalid variable argument was supplied")

        f_fig = plotly_scatter(
            f_c_color=["#00FA9A", "#FFD700", "#CD0000"],
            labs={x_var: var_labels[0], y_var: var_labels[1], z_var: var_labels[2]},
            title=f"Relationship between {var_labels[0]}, {var_labels[1]} & {var_labels[2]} For {df.shape[0]:,} Rules",
            hover_data={x_var: ":.4f", y_var: ":.4f", z_var: ":.4f"}
        )

    f_fig.update_layout(plot_bgcolor=bg_color, paper_bgcolor=bg_color, title_font_color=font_color)
    f_fig.update_yaxes(color=font_color, showgrid=True, gridwidth=1, gridcolor=grid_color)
    f_fig.update_xaxes(color=font_color, showgrid=True, gridwidth=1, gridcolor=grid_color)

    return f_fig


def unique_products(df: DataFrame):
    """
    parameter
    ---------
    df: With either a variable called 'Product' or 'Product_Taxonomy'.

    return
    ------
    A list of unique products.
    """
    if "Product_Taxonomy" in df.columns.to_list():
        return list(df["Product_Taxonomy"].unique())
    else:
        return list(df["Product"].unique())


def metric_description(df: DataFrame, return_type: str = "rules"):
    """
    parameter
    ---------
    df: product data.
    return_type: The type of output to return.

    value
    -----
    A Dictionary
    """

    n_rows = df.shape[0]

    if return_type == "rules":
        metric_desc = {"n_rules": n_rows}

        for m in ["support", "confidence", "lift", "leverage", "conviction"]:
            desc = list(df[m].agg(["min", "max"]).values)
            metric_desc[m] = desc

        return metric_desc
    elif return_type == "sup_len":
        values = {"n_itemsets": n_rows}

        for v in ["support", "length"]:
            val = list(df[v].agg(["min", "max"]).values)
            values[v] = val

        return values
