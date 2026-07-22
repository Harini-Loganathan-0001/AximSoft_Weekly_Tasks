from flask import Flask, render_template, request, send_file
import pandas as pd
import io



app = Flask(__name__)

# Load cleaned dataset
df = pd.read_csv("data/final_clean_dataset.csv")

#Convert Date Column
df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"]
)

#Create Month Column
df["order_purchase_month"] = (
    df["order_purchase_timestamp"]
    .dt.strftime("%b")
)


@app.route("/")
def dashboard():

    # ==========================
    # KPI Cards
    # ==========================

    revenue = df["payment_value"].sum()
    revenue_display = f"₹ {revenue/10000000:.2f} Cr"

    total_orders = df["order_id"].nunique()

    total_customers = df["customer_unique_id"].nunique()

    total_sellers = df["seller_id"].nunique()

    # ==========================
    # Monthly Revenue
    # ==========================

    month_order = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    monthly_sales = (
        df.groupby("order_purchase_month")["payment_value"]
        .sum()
        .reindex(month_order, fill_value=0)
    )

    labels = monthly_sales.index.tolist()

    values = monthly_sales.values.tolist()

    # ==========================
    # Revenue by Payment Type
    # ==========================

    payment_data = (
        df.groupby("payment_type")["payment_value"]
        .sum()
        .round(2)
    )

    payment_labels = payment_data.index.tolist()

    payment_values = payment_data.values.tolist()


    # ==========================
    # Top Product Categories
    # ==========================

    category_data = (
        df.groupby("product_category_name_english")["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    category_labels = [
        label.replace("_", " ").title()
        for label in category_data.index.tolist()
    ]

    category_values = category_data.values.tolist()

    # ==========================
    # Revenue by State
    # ==========================

    state_data = (
        df.groupby("customer_state")["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    state_labels = state_data.index.tolist()

    state_values = state_data.values.tolist()

    # ==========================
    # Top 10 Sellers
    # ==========================

    seller_data = (
        df.groupby("seller_id")["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    seller_labels = [
        seller[:8] + "..."
        for seller in seller_data.index.tolist()
    ]

    seller_values = seller_data.values.tolist()

    # ==========================
    # Monthly Orders
    # ==========================

    monthly_orders = (
        df.groupby("order_purchase_month")["order_id"]
        .nunique()
        .reindex(month_order, fill_value=0)
    )

    order_labels = monthly_orders.index.tolist()

    order_values = monthly_orders.values.tolist()

    # ==========================
    # Order Status
    # ==========================

    status_data = (
        df["order_status"]
                .value_counts()
                .reset_index()
            )

    status_labels = status_data["order_status"].tolist()
    status_values = status_data["count"].tolist()


    # ==========================
    # Review Scores
    # ==========================

    review_data = (
        df.groupby("review_score")["review_score"]
        .count()
    )

    review_labels = review_data.index.astype(str).tolist()

    review_values = review_data.values.tolist()


    # Top Revenue State
    top_state = state_data.idxmax()

    # Most Used Payment Type
    top_payment = (
        df.groupby("payment_type")["payment_value"]
        .sum()
        .idxmax()
        .replace("_", " ")
        .title()
    )

    # Best Selling Category
    top_category = (
        category_data.idxmax()
        .replace("_", " ")
        .title()
    )

    # Average Review Score
    avg_review = round(df["review_score"].mean(), 2)


    

    # ==========================
    # Recent Transactions Table
    # ==========================

    recent_orders = (
        df.sort_values("order_purchase_timestamp", ascending=False)
        [[
            "customer_state",
            "payment_type",
            "order_status",
            "payment_value"
        ]]
        .head(6)
    )

    # ==========================
    # Send Data to HTML
    # ==========================

    return render_template(
        "dashboard.html",
        revenue=revenue_display,
        orders=total_orders,
        customers=total_customers,
        sellers=total_sellers,
        labels=labels,
        values=values,
        payment_labels=payment_labels,
        payment_values=payment_values,
        category_labels=category_labels,
        category_values=category_values,
        state_labels=state_labels,
        state_values=state_values,
        seller_labels=seller_labels,
        seller_values=seller_values,
        order_labels=order_labels,
        order_values=order_values,
        status_labels=status_labels,
        status_values=status_values,
        review_labels=review_labels,
        review_values=review_values,
        top_state=top_state,
        top_payment=top_payment,
        top_category=top_category,
        avg_review=avg_review,
        
        recent_orders=recent_orders.to_dict(orient="records"),
    )




# ==========================
# Sales Analytics
# ==========================

@app.route("/sales")
def sales():

    # Total Revenue
    revenue = df["payment_value"].sum()
    revenue_display = f"₹ {revenue/10000000:.2f} Cr"

    # Average Order Value
    avg_order = (
        df.groupby("order_id")["payment_value"]
        .sum()
        .mean()
    )
    avg_order_display = f"₹ {avg_order:.2f}"

    # Top Revenue State
    top_state = (
        df.groupby("customer_state")["payment_value"]
        .sum()
        .idxmax()
    )

    # Most Used Payment Type
    top_payment = (
        df["payment_type"]
        .mode()[0]
        .replace("_", " ")
        .title()
    )

    # ==========================
    # Monthly Sales Summary
    # ==========================

    month_order = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    sales_summary = (
        df.groupby("order_purchase_month")
        .agg(
            Revenue=("payment_value", "sum"),
            Orders=("order_id", "nunique")
        )
        .reindex(month_order, fill_value=0)
    )

    sales_summary["Average Order Value"] = (
        sales_summary["Revenue"] / sales_summary["Orders"]
    ).fillna(0)

    sales_summary = sales_summary.reset_index()

    return render_template(
        "sales.html",
        revenue=revenue_display,
        avg_order=avg_order_display,
        top_state=top_state,
        top_payment=top_payment,
        sales_summary=sales_summary.to_dict(orient="records"),
    )


# ==========================
# Customer Analytics
# ==========================

@app.route("/customers")
def customers():

    # ==========================
    # KPI Cards
    # ==========================

    total_customers = df["customer_unique_id"].nunique()


    # Repeat Customer Analysis

    customer_orders = (
        df.groupby("customer_unique_id")["order_id"]
        .nunique()
    )


    repeat_customers = (
        customer_orders[customer_orders > 1]
        .count()
    )


    one_time_customers = (
        customer_orders[customer_orders == 1]
        .count()
    )


    repeat_rate = (
        repeat_customers / total_customers * 100
    )


    avg_spending = (
        df.groupby("customer_unique_id")["payment_value"]
        .sum()
        .mean()
    )


    repeat_rate_display = f"{repeat_rate:.2f}%"

    avg_spending_display = f"₹ {avg_spending:.2f}"



    # ==========================
    # Top Purchasing Cities
    # ==========================

    city_data = (
        df.groupby("customer_city")["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )


    city_labels = city_data.index.tolist()

    city_values = city_data.values.tolist()



    # ==========================
    # Customer Distribution State
    # ==========================


    state_customer = (
        df.groupby("customer_state")
        ["customer_unique_id"]
        .nunique()
        .sort_values(ascending=False)
        .head(10)
    )


    state_labels = state_customer.index.tolist()

    state_values = state_customer.values.tolist()



    # ==========================
    # Customer Spending Analysis
    # ==========================


    spending_data = (
        df.groupby("customer_unique_id")
        ["payment_value"]
        .sum()
        .reset_index()
    )


    spending_data.columns = [
        "Customer_ID",
        "Total_Spending"
    ]


    spending_summary = (
        spending_data
        .sort_values(
            "Total_Spending",
            ascending=False
        )
        .head(20)
    )


    return render_template(
        "customers.html",

        total_customers=total_customers,

        repeat_customers=repeat_customers,

        one_time_customers=one_time_customers,

        repeat_rate=repeat_rate_display,

        avg_spending=avg_spending_display,


        city_labels=city_labels,
        city_values=city_values,


        state_labels=state_labels,
        state_values=state_values,


        spending_summary=
        spending_summary.to_dict(
            orient="records"
        )
    )



@app.route("/dataset")
def dataset():

    filtered_df = df.copy()

    # ==========================
    # Pagination
    # ==========================

    page = request.args.get("page", 1, type=int)

    per_page = request.args.get("per_page", 25, type=int)

    # ==========================
    # Filters
    # ==========================

    search = request.args.get("search", "").strip()
    order_status = request.args.get("order_status", "")
    payment_type = request.args.get("payment_type", "")
    customer_state = request.args.get("customer_state", "")
    seller_state = request.args.get("seller_state", "")
    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")

    # Search
    if search:

        filtered_df = filtered_df[
            filtered_df["order_id"].astype(str).str.contains(search, case=False, na=False)
            | filtered_df["customer_unique_id"].astype(str).str.contains(search, case=False, na=False)
            | filtered_df["customer_city"].astype(str).str.contains(search, case=False, na=False)
            | filtered_df["customer_state"].astype(str).str.contains(search, case=False, na=False)
            | filtered_df["payment_type"].astype(str).str.contains(search, case=False, na=False)
            | filtered_df["order_status"].astype(str).str.contains(search, case=False, na=False)
        ]

    # Order Status
    if order_status:

        filtered_df = filtered_df[
            filtered_df["order_status"] == order_status
        ]

    # Payment Type
    if payment_type:

        filtered_df = filtered_df[
            filtered_df["payment_type"] == payment_type
        ]

    # Customer State
    if customer_state:

        filtered_df = filtered_df[
            filtered_df["customer_state"] == customer_state
        ]

    # Seller State
    if seller_state:

        filtered_df = filtered_df[
            filtered_df["seller_state"] == seller_state
        ]

    if from_date:
        from_date = pd.to_datetime(from_date)
        filtered_df = filtered_df[
            filtered_df["order_purchase_timestamp"] >= from_date
        ]

    if to_date:
        to_date = pd.to_datetime(to_date) + pd.Timedelta(days=1)
        filtered_df = filtered_df[
            filtered_df["order_purchase_timestamp"] < to_date
        ]


    # ==========================
    # KPI Cards
    # ==========================

    total_tables = 9
    total_records = len(filtered_df)
    total_columns = len(df.columns)

    last_updated = (
        df["order_purchase_timestamp"]
        .max()
        .strftime("%d %b %Y")
    )

    # ==========================
    # Filter Dropdown Values
    # ==========================

    order_statuses = sorted(
        df["order_status"].dropna().unique().tolist()
    )

    payment_types = sorted(
        df["payment_type"].dropna().unique().tolist()
    )

    customer_states = sorted(
        df["customer_state"].dropna().unique().tolist()
    )

    seller_states = sorted(
        df["seller_state"].dropna().unique().tolist()
    )

    # ==========================
    # Dataset Preview
    # ==========================

    table_columns = df.columns.tolist()

   # Total Records After Filtering

    total_records = len(filtered_df)

    # Total Pages

    total_pages = (total_records + per_page - 1) // per_page

    # Starting Row

    start = (page - 1) * per_page

    # Ending Row

    end = start + per_page

    # Current Page Data

    table_data = (
        filtered_df
        .iloc[start:end]
        .to_dict(orient="records")
    )

    preview = filtered_df.head(25).to_dict(orient="records")


    return render_template(

        "dataset.html",

        total_tables=total_tables,
        total_records=total_records,
        total_columns=total_columns,
        last_updated=last_updated,

        order_statuses=order_statuses,
        payment_types=payment_types,
        customer_states=customer_states,
        seller_states=seller_states,

        table_columns=table_columns,
        table_data=table_data,
        preview=preview,

        page=page,
        per_page=per_page,
        total_pages=total_pages,

    )


@app.route("/export")
def export():

    export_df = df.copy()

    # Search
    search = request.args.get("search", "").strip()

    if search:

        export_df = export_df[
            export_df.astype(str)
            .apply(lambda col: col.str.contains(search, case=False, na=False))
            .any(axis=1)
        ]

    # Order Status
    order_status = request.args.get("order_status")

    if order_status:
        export_df = export_df[
            export_df["order_status"] == order_status
        ]

    # Payment Type
    payment_type = request.args.get("payment_type")

    if payment_type:
        export_df = export_df[
            export_df["payment_type"] == payment_type
        ]

    # Customer State
    customer_state = request.args.get("customer_state")

    if customer_state:
        export_df = export_df[
            export_df["customer_state"] == customer_state
        ]

    # Seller State
    seller_state = request.args.get("seller_state")

    if seller_state:
        export_df = export_df[
            export_df["seller_state"] == seller_state
        ]

    # Date Filter
    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")

    if from_date:
        from_date = pd.to_datetime(from_date)
        export_df = export_df[
            export_df["order_purchase_timestamp"] >= from_date
        ]

    if to_date:
        to_date = pd.to_datetime(to_date) + pd.Timedelta(days=1)
        export_df = export_df[
            export_df["order_purchase_timestamp"] < to_date
    ]


    output = io.BytesIO()

    export_df.to_csv(output, index=False)

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="filtered_dataset.csv",
        mimetype="text/csv"
    )


@app.route("/products")
def products():

    # ==========================
    # KPI CARDS
    # ==========================

    total_products = df["product_id"].nunique()

    total_categories = (
        df["product_category_name_english"]
        .nunique()
    )

    avg_product_price = (
        df["price"]
        .mean()
    )

    avg_review_score = (
        df["review_score"]
        .mean()
    )

    # ==========================
    # TOP PRODUCTS TABLE
    # ==========================

    product_summary = (

        df.groupby("product_category_name_english")["price"]

        .sum()

        .reset_index()

        .sort_values(
            by="price",
            ascending=False
        )

        .head(10)

    )

    return render_template(

        "products.html",

        total_products=total_products,

        total_categories=total_categories,

        avg_product_price=avg_product_price,

        avg_review_score=avg_review_score,

        product_summary=product_summary.itertuples(index=False)

    )


@app.route("/sellers")
def sellers():

    # ==========================
    # KPI CARDS
    # ==========================

    total_sellers = df["seller_id"].nunique()

    seller_states = df["seller_state"].nunique()

    avg_seller_revenue = (
        df.groupby("seller_id")["seller_revenue"]
        .max()
        .mean()
    )

    avg_performance_score = (
        df["seller_performance_score"]
        .mean()
    )

    # ==========================
    # TOP SELLERS TABLE
    # ==========================

    seller_summary = (

        df.groupby("seller_id")
        .agg(
            Revenue=("seller_revenue", "max"),
            Performance=("seller_performance_score", "mean")
        )
        .sort_values(
            by="Revenue",
            ascending=False
        )
        .head(10)
        .reset_index()

    )

    return render_template(

        "sellers.html",

        total_sellers=total_sellers,

        seller_states=seller_states,

        avg_seller_revenue=avg_seller_revenue,

        avg_performance_score=avg_performance_score,

        seller_summary=seller_summary.itertuples(index=False)

    )


@app.route("/delivery")
def delivery():

    # ==========================
    # KPI CARDS
    # ==========================

    avg_delivery_time = df["delivery_time"].mean()

    avg_shipping_days = df["shipping_duration"].mean()

    avg_processing_time = df["processing_time"].mean()

    on_time_rate = (
        (df["delivery_status"] == "On Time").mean()
    ) * 100

    # ==========================
    # TABLE
    # ==========================

    delivery_summary = (

        df.groupby("seller_state")

        .agg(

            Avg_Delivery=("delivery_time","mean"),

            Avg_Shipping=("shipping_duration","mean"),

            Orders=("order_id","count")

        )

        .sort_values(

            by="Orders",

            ascending=False

        )

        .head(10)

        .reset_index()

    )

    return render_template(

        "delivery.html",

        avg_delivery_time=avg_delivery_time,

        avg_shipping_days=avg_shipping_days,

        avg_processing_time=avg_processing_time,

        on_time_rate=on_time_rate,

        delivery_summary=delivery_summary.itertuples(index=False)

    )


@app.route("/payments")
def payments():

    total_transactions = len(df)

    total_payment = df["payment_value"].sum()

    avg_payment = df["payment_value"].mean()

    avg_review = df["review_score"].mean()

    payment_summary = (

        df.groupby("payment_type")

        .agg(

            Transactions=("payment_value","count"),

            Total_Payment=("payment_value","sum"),

            Average_Payment=("payment_value","mean")

        )

        .sort_values(

            by="Total_Payment",

            ascending=False

        )

        .reset_index()

    )

    return render_template(

        "payments.html",

        total_transactions=total_transactions,

        total_payment=total_payment,

        avg_payment=avg_payment,

        avg_review=avg_review,

        payment_summary=payment_summary.itertuples(index=False)

    )





if __name__ == "__main__":
    app.run(debug=True)



