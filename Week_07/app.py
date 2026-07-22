from flask import Flask, render_template, make_response
import pandas as pd
import numpy as np

from flask import request, send_file
import io

from reports import reports


app = Flask(__name__)
app.register_blueprint(reports)

# Load dataset 
from reports import df

# Helper function to format numbers compactly
def format_number(num):
    if num >= 1_000_000:
        return f"${num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"${num/1_000:.2f}K"
    else:
        return f"${num:.2f}"

@app.route("/")
def home():
    kpis = {
        "total_bookings": f"{len(df):,}",
        "cancellation_rate": f"{round(df['is_canceled'].mean() * 100, 2)}%",
        "avg_daily_rate": f"${round(df['adr'].mean(), 2)}",
        "avg_stay_duration": f"{round((df['stays_in_weekend_nights'] + df['stays_in_week_nights']).mean(), 1)} Nights"
    }

    # Month Order

    month_order = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]

    # Monthly Bookings

    monthly_booking = (
        df["arrival_date_month"]
        .value_counts()
        .reindex(month_order)
        .fillna(0)
    )

    monthly_labels = monthly_booking.index.tolist()
    monthly_values = monthly_booking.astype(int).tolist()

    # Monthly Revenue

    monthly_revenue = (
        df.groupby("arrival_date_month")["estimated_booking_revenue"]
        .sum()
        .reindex(month_order)
        .fillna(0)
    )

    revenue_labels = monthly_revenue.index.tolist()
    revenue_values = monthly_revenue.round(0).tolist()

    # Booking Season

    season = (
        df["booking_season"]
        .value_counts()
    )

    season_labels = season.index.tolist()
    season_values = season.astype(int).tolist()

    # Highest Booking Month

    highest_month = monthly_booking.idxmax()
    highest_booking = int(monthly_booking.max())

    # Highest Revenue Month

    highest_revenue_month = monthly_revenue.idxmax()
    highest_revenue = round(monthly_revenue.max(),2)

    # Top Hotel
    

    # Count bookings by hotel
    hotel_counts = df["hotel"].value_counts()

    # Get the most booked hotel code (0 or 1)
    top_hotel_id = hotel_counts.idxmax()

    # Convert code to hotel name
    hotel_map = {
        0: "City Hotel",
        1: "Resort Hotel"
    }

    top_hotel = hotel_map.get(top_hotel_id, "Unknown")

    # Total bookings for the top hotel
    top_hotel_bookings = hotel_counts.max()

    # Percentage of bookings
    top_hotel_percent = round(
        (top_hotel_bookings / len(df)) * 100,
        1
    )

    # Top Country

    country = df["country"].value_counts()

    top_country = country.idxmax()
    top_country_bookings = int(country.max())

    # Average Lead Time

    avg_lead = round(df["lead_time"].mean(),1)

    booking_success_rate = round((1 - df["is_canceled"].mean()) * 100, 2)

    avg_special_requests = round(df["total_of_special_requests"].mean(), 2)

    booking_success_rate = round(
        (1 - df["is_canceled"].mean()) * 100,
        2
    )

    repeat_guest_rate = round(
        df["is_repeated_guest"].mean() * 100,
        2
    )

    max_lead_time = int(df["lead_time"].max())
    

    # Booking Source Analysis

    booking_source = (
        df.filter(like="distribution_channel_")
        .sum()
        .sort_values(ascending=False)
    )

    source_labels = (
        booking_source.index
        .str.replace("distribution_channel_","")
        .tolist()
    )

    source_values = booking_source.astype(int).tolist()


    deposit = df["deposit_type"].value_counts()

    deposit_labels = deposit.index.tolist()
    deposit_values = deposit.tolist()

    total_cancelled = int(df["is_canceled"].sum())

    avg_stay = round(
        (df["stays_in_weekend_nights"] +
        df["stays_in_week_nights"]).mean(), 1
    )

    avg_adr = round(df["adr"].mean(), 2)

    # Hotel Type Distribution

    hotel_type = df["hotel"].value_counts()

    hotel_type_labels = hotel_type.index.tolist()
    hotel_type_values = hotel_type.astype(int).tolist()

    # Booking Value Segment

    booking_segment = (
        df["booking_value_segment"]
        .value_counts()
    )

    booking_segment_labels = booking_segment.index.tolist()
    booking_segment_values = booking_segment.astype(int).tolist()

    # Average ADR by Hotel

    adr_hotel = (
        df.groupby("hotel")["adr"]
        .mean()
        .round(2)
    )

    adr_hotel_labels = adr_hotel.index.tolist()
    adr_hotel_values = adr_hotel.tolist()


    scatter_df = df.sample(500, random_state=42)

    scatter_data = [
        {
            "x": int(row["lead_time"]),
            "y": float(row["adr"])
        }
        for _, row in scatter_df.iterrows()
    ]

    # booking status distributuion

    status = df["reservation_status"].value_counts()

    status_labels = status.index.tolist()
    status_values = status.astype(int).tolist()

    # Monthly Cancellation Trend

    cancel_df = df[df["is_canceled"]==1]

    cancel_month = (
    cancel_df.groupby("arrival_date_month")
    .size()
    .reindex(month_order)
    .fillna(0)
    )

    cancel_labels = cancel_month.index.tolist()
    cancel_values = cancel_month.astype(int).tolist()

    # top countries

    guest_country = df["country"].value_counts().head(8)

    guest_country_labels = guest_country.index.tolist()
    guest_country_values = guest_country.astype(int).tolist()

    booking_changes = (
        df.groupby("customer_type")["booking_changes"]
        .mean()
        .round(2)
    )

    

    booking_change_labels = booking_changes.index.tolist()

    booking_change_values = booking_changes.tolist()

    lead_category = df["lead_time_category"].value_counts()

    lead_category_labels = lead_category.index.tolist()
    lead_category_values = lead_category.tolist()


    total_revenue = round(df["adr"].sum(), 2)

    top_country = df["country"].value_counts().idxmax()

    top_hotel = df["hotel"].value_counts().idxmax()


    return render_template("index.html",
                           kpis=kpis,
                           monthly_labels=monthly_labels,
                            monthly_values=monthly_values,

                            revenue_labels=revenue_labels,
                            revenue_values=revenue_values,

                            season_labels=season_labels,
                            season_values=season_values,

                            highest_month=highest_month,
                            highest_booking=highest_booking,

                            highest_revenue_month=highest_revenue_month,
                            highest_revenue=highest_revenue,

                            top_hotel=top_hotel,
                            top_hotel_percent=top_hotel_percent,

                            top_country=top_country,
                            top_country_bookings=top_country_bookings,

                            avg_lead=avg_lead,

                            source_labels=source_labels,
                            source_values=source_values,

                            deposit_labels=deposit_labels,
                            deposit_values=deposit_values,

                            total_cancelled=total_cancelled,
                            avg_stay=avg_stay,
                            avg_adr=avg_adr,

                            hotel_type_labels=hotel_type_labels,
                            hotel_type_values=hotel_type_values,

                            booking_segment_labels=booking_segment_labels,
                            booking_segment_values=booking_segment_values,

                            adr_hotel_labels=adr_hotel_labels,
                            adr_hotel_values=adr_hotel_values, 

                            scatter_data=scatter_data,
                            status_labels=status_labels,                           
                            status_values=status_values,

                            cancel_labels=cancel_labels,
                            cancel_values=cancel_values,

                            guest_country_labels=guest_country_labels,
                            guest_country_values=guest_country_values,

                            booking_change_labels=booking_change_labels,
                            booking_change_values=booking_change_values,

                            lead_category_labels=lead_category_labels,
                            lead_category_values=lead_category_values,

                            total_revenue=total_revenue,

                            booking_success_rate=booking_success_rate,
                            avg_special_requests=avg_special_requests,
                            repeat_guest_rate=repeat_guest_rate,
                            max_lead_time=max_lead_time

                        )


@app.route("/booking-analytics")
def booking_analytics():
    kpis = {
        "total_bookings": f"{len(df):,}",
        "cancellation_rate": f"{round(df['is_canceled'].mean() * 100, 2)}%",
        "avg_daily_rate": f"${round(df['adr'].mean(), 2)}",
        "avg_stay_duration": f"{round((df['stays_in_weekend_nights'] + df['stays_in_week_nights']).mean(), 1)} Nights"
    }
    
    # 1 Monthly Bookings


    month_order = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]

    monthly = (
        df["arrival_date_month"]
        .value_counts()
        .reindex(month_order)
        .fillna(0)
    )

    monthly_labels = monthly.index.tolist()
    monthly_values = monthly.astype(int).tolist()

    # 2 Hotel Type

    hotel = df["hotel"].value_counts()

    hotel_labels = hotel.index.tolist()
    hotel_values = hotel.tolist()

    # 3 Country Wise Bookings

    country = (
        df["country"]
        .value_counts()
        .head(10)
    )

    country_labels = country.index.tolist()
    country_values = country.tolist()

    # 4 Market Segment Analysis

    market_cols = [
        "market_segment_Complementary",
        "market_segment_Corporate",
        "market_segment_Direct",
        "market_segment_Groups",
        "market_segment_Offline TA/TO",
        "market_segment_Online TA",
        "market_segment_Undefined"
    ]

    market = df[market_cols].sum()

    market_labels = [
        col.replace("market_segment_", "")
        for col in market.index
    ]

    market_values = market.astype(int).tolist()

    # 5 Lead Time Distribution

    lead = (
        df.groupby(
            pd.cut(
                df["lead_time"],
                bins=[0,30,60,90,180,365,800]
            )
        )
        .size()
    )

    lead_labels = [
        "0-30",
        "31-60",
        "61-90",
        "91-180",
        "181-365",
        "365+"
    ]

    lead_values = lead.tolist()

    # 6 Reservation Status

    status = (
        df["reservation_status"]
        .replace({
            0: "Canceled",
            1: "Check-Out",
            2: "No-Show"
        })
        .value_counts()
    )

    reservation_labels = status.index.tolist()
    reservation_values = status.tolist()

    # 7 Lead Time Histogram

    lead_bins = [0, 30, 60, 90, 180, 365, 800]

    lead_hist = (
        df.groupby(
            pd.cut(df["lead_time"], bins=lead_bins)
        )
        .size()
    )

    lead_hist_labels = [
        "0-30",
        "31-60",
        "61-90",
        "91-180",
        "181-365",
        "365+"
    ]

    lead_hist_values = lead_hist.tolist()

    # stay duration

    stay_duration = (
        (df["stays_in_weekend_nights"] + df["stays_in_week_nights"])
    )

    stay_labels = [
        "Short Stay",
        "Medium Stay",
        "Long Stay"
    ]

    stay_values = [
        int((stay_duration <= 2).sum()),
        int(((stay_duration >= 3) & (stay_duration <= 5)).sum()),
        int((stay_duration >= 6).sum())
    ]

    # 8 Booking Value Segment

    booking_segment = (
        df["booking_value_segment"]
        .value_counts()
    )

    booking_segment_labels = booking_segment.index.tolist()
    booking_segment_values = booking_segment.tolist()

    booking_summary = [

    {
        "metric":"Total Bookings",
        "value":f"{len(df):,}",
        "finding":"High booking volume indicates strong customer demand."
    },

    {
        "metric":"Cancellation Rate",
        "value":f"{round(df['is_canceled'].mean()*100,2)}%",
        "finding":"Cancellation percentage suggests opportunities to improve booking retention."
    },

    {
        "metric":"Average Daily Rate",
        "value":f"${round(df['adr'].mean(),2)}",
        "finding":"Average room pricing remains stable across reservations."
    },

    {
        "metric":"Average Stay Duration",
        "value":f"{round(df['total_stay_duration'].mean(),1)} Nights",
        "finding":"Guests generally prefer short-to-medium stays."
    },

    {
        "metric":"Most Preferred Hotel",
        "value":df["hotel"].value_counts().idxmax(),
        "finding":"This hotel type attracts the highest number of bookings."
    },

    {
        "metric":"Top Booking Country",
        "value":country.index[0],
        "finding":"Largest share of customers originates from this country."
    },

    {
        "metric":"Peak Booking Month",
        "value":monthly.idxmax(),
        "finding":"Booking demand reaches its maximum during this month."
    },

    {
        "metric":"Most Common Customer Type",
        "value":df["customer_type"].value_counts().idxmax(),
        "finding":"This customer category dominates hotel reservations."
    },

    {
        "metric":"Booking Value Segment",
        "value":df["booking_value_segment"].value_counts().idxmax(),
        "finding":"Most bookings belong to this spending segment."
    },

    {
        "metric":"Reservation Status",
        "value":df["reservation_status"].value_counts().idxmax(),
        "finding":"Most reservations successfully complete their stay."
    }

    ]
    return render_template("booking_analytics.html",
                            kpis=kpis,

                            monthly_labels=monthly_labels,
                            monthly_values=monthly_values,

                            hotel_labels=hotel_labels,
                            hotel_values=hotel_values,

                            country_labels=country_labels,
                            country_values=country_values,

                            market_labels=market_labels,
                            market_values=market_values,

                            lead_labels=lead_labels,
                            lead_values=lead_values,

                            reservation_labels=reservation_labels,
                            reservation_values=reservation_values,

                            lead_hist_labels=lead_hist_labels,
                            lead_hist_values=lead_hist_values,

                            booking_segment_labels=booking_segment_labels,
                            booking_segment_values=booking_segment_values,
                            booking_summary=booking_summary,

                            stay_labels=stay_labels,
                            stay_values=stay_values,
 )


@app.route("/customer-analytics")
def customer_analytics():
    kpis = {
        "total_customers": f"{df['customer_id'].nunique():,}" if 'customer_id' in df else f"{len(df):,}",
        "unique_countries": df['country'].nunique() if 'country' in df else "N/A",
        "repeat_guests": round(df['is_repeated_guest'].mean() * 100, 2) if 'is_repeated_guest' in df else 0,
        "total_requests": df['total_of_special_requests'].sum() if 'total_of_special_requests' in df else "N/A"
    }

    # Customer Type Distribution

    customer_type = (
        df["customer_type"]
        .value_counts()
    )

    customer_type_labels = customer_type.index.tolist()
    customer_type_values = customer_type.tolist()

    # Repeat Guest Analysis

    repeat_guest = (
        df["is_repeated_guest"]
        .replace({
            0: "New Guest",
            1: "Repeat Guest"
        })
        .value_counts()
    )

    repeat_labels = repeat_guest.index.tolist()
    repeat_values = repeat_guest.tolist()

    # Guest Demographics

    guest_labels = ["Adults", "Children", "Babies"]

    guest_values = [
        int(df["adults"].sum()),
        int(df["children"].fillna(0).sum()),
        int(df["babies"].sum())
    ]

    # Special Requests

    special = (
        df["total_of_special_requests"]
        .value_counts()
        .sort_index()
    )

    special_labels = special.index.astype(str).tolist()
    special_values = special.tolist()

    # Customer Nationality

    country = (
        df["country"]
        .value_counts()
        .head(10)
    )

    country_labels = country.index.tolist()
    country_values = country.tolist()

    # Booking Value Segment

    value_segment = (
        df["booking_value_segment"]
        .value_counts()
    )

    value_labels = value_segment.index.tolist()
    value_values = value_segment.tolist()


    top_customer_type = df["customer_type"].mode()[0]

    top_country = df["country"].value_counts().idxmax()

    avg_special_requests = round(df["total_of_special_requests"].mean(), 2)

    top_booking_segment = df["booking_value_segment"].value_counts().idxmax() 

    repeat_guest_count = int(df["is_repeated_guest"].sum())

    repeat_guest_rate = round(df["is_repeated_guest"].mean() * 100, 2)

    # Customer Loyalty Status

    new_guest = int((df["is_repeated_guest"] == 0).sum())
    repeat_guest = int((df["is_repeated_guest"] == 1).sum())

    loyalty_labels = ["Guests"]

    new_guest_values = [new_guest]
    repeat_guest_values = [repeat_guest]


    return render_template("customer_analytics.html", 
                            kpis=kpis,

                            customer_type_labels=customer_type_labels,
                            customer_type_values=customer_type_values,

                            repeat_labels=repeat_labels,
                            repeat_values=repeat_values,

                            guest_labels=guest_labels,
                            guest_values=guest_values,

                            special_labels=special_labels,
                            special_values=special_values,

                            country_labels=country_labels,
                            country_values=country_values,

                            value_labels=value_labels,
                            value_values=value_values,

                            top_customer_type=top_customer_type,
                            top_country=top_country,

                            avg_special_requests=avg_special_requests,
                            top_booking_segment=top_booking_segment,

                            repeat_guest_count=repeat_guest_count,
                            repeat_guest_rate=repeat_guest_rate,

                            loyalty_labels=loyalty_labels,
                            new_guest_values=new_guest_values,
                            repeat_guest_values=repeat_guest_values,                                                                               
)


@app.route("/revenue-analytics")
def revenue_analytics():

    total_revenue = (df['adr'] * (df['stays_in_weekend_nights'] + df['stays_in_week_nights'])).sum()
    avg_revenue_booking = total_revenue / len(df) if len(df) > 0 else 0

    half = len(df) // 2
    first_half = (df.iloc[:half]['adr'] * (df.iloc[:half]['stays_in_weekend_nights'] + df.iloc[:half]['stays_in_week_nights'])).sum()
    second_half = (df.iloc[half:]['adr'] * (df.iloc[half:]['stays_in_weekend_nights'] + df.iloc[half:]['stays_in_week_nights'])).sum()
    revenue_growth = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0

    if 'country' in df:
        country_revenue = df.groupby('country').apply(lambda x: (x['adr'] * (x['stays_in_weekend_nights'] + x['stays_in_week_nights'])).sum())
        top_country = country_revenue.idxmax()
        top_country_value = country_revenue.max()
        top_country_revenue = f"{top_country}: {format_number(top_country_value)}"
    else:
        top_country_revenue = "N/A"

    kpis = {
        "total_revenue": format_number(total_revenue),
        "avg_revenue_booking": format_number(avg_revenue_booking),
        "revenue_growth": f"{revenue_growth:+.2f}%",
        "top_country_revenue": top_country_revenue
    }

    # Monthly Revenue Trend
    monthly_revenue = (
        df.groupby("arrival_date_month")
        .apply(lambda x: (x["adr"] *
                            (x["stays_in_weekend_nights"] +
                            x["stays_in_week_nights"])).sum())
    )

    month_order = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    monthly_revenue = monthly_revenue.reindex(month_order, fill_value=0)

    revenue_labels = monthly_revenue.index.tolist()

    revenue_values = monthly_revenue.round(2).tolist()


    adr_analysis = df.groupby("hotel")["adr"].mean().round(2)

    hotel_map = {
        0: "Resort Hotel",
        1: "City Hotel"
    }

    adr_labels = [hotel_map.get(i, i) for i in adr_analysis.index]

    adr_values = adr_analysis.values.tolist()


    season_map = {
        "December": "Winter",
        "January": "Winter",
        "February": "Winter",

        "March": "Spring",
        "April": "Spring",
        "May": "Spring",

        "June": "Summer",
        "July": "Summer",
        "August": "Summer",

        "September": "Autumn",
        "October": "Autumn",
        "November": "Autumn"
    }

    df["season"] = df["arrival_date_month"].map(season_map)


    season_revenue = df.groupby("season").apply(

        lambda x:(

            x["adr"]*

            (x["stays_in_week_nights"]+

            x["stays_in_weekend_nights"])

        ).sum()

    )

    season_labels=season_revenue.index.tolist()

    season_values=season_revenue.round(2).tolist()

    stay_labels = ["Weekend", "Weekday"]

    stay_values = [
        round(df["stays_in_weekend_nights"].mean(),2),
        round(df["stays_in_week_nights"].mean(),2)
    ]


    market_columns = [

        "market_segment_Complementary",

        "market_segment_Corporate",

        "market_segment_Direct",

        "market_segment_Groups",

        "market_segment_Offline TA/TO",

        "market_segment_Online TA",

        "market_segment_Undefined"

    ]

    market_revenue = {}

    for col in market_columns:

        revenue = (

            df.loc[df[col] == 1, "estimated_booking_revenue"]

            .sum()

        )

        market_revenue[col.replace("market_segment_", "")] = revenue

    market_labels = list(market_revenue.keys())

    market_values = list(market_revenue.values())

    hotel_revenue = (
        df.groupby("hotel")
        .apply(lambda x:
                (x["adr"] *
                (x["stays_in_week_nights"] +
                x["stays_in_weekend_nights"])).sum())
    )

    hotel_map = {
        0:"Resort Hotel",
        1:"City Hotel"
    }

    hotel_labels=[hotel_map.get(i,i) for i in hotel_revenue.index]

    hotel_values=hotel_revenue.round(2).tolist()


    revenue_summary = [

    {
        "metric": "Total Revenue",
        "value": kpis["total_revenue"],
        "insight": "Overall revenue generated from all bookings."
    },

    {
        "metric": "Average Revenue / Booking",
        "value": kpis["avg_revenue_booking"],
        "insight": "Average revenue earned from each booking."
    },

    {
        "metric": "Highest Revenue Hotel",
        "value": "City Hotel",
        "insight": "Generated the highest overall revenue."
    },

    {
        "metric": "Highest Revenue Season",
        "value": "Summer",
        "insight": "Peak revenue observed during summer."
    },

    {
        "metric": "Average Stay",
        "value": f"{round((df['stays_in_week_nights'] + df['stays_in_weekend_nights']).mean(),1)} Nights",
        "insight": "Average guest stay duration."
    },

    {
        "metric": "Top Booking Value Segment",
        "value": "High Value",
        "insight": "Largest contribution to total revenue."
    }

    ]






    return render_template("revenue_analytics.html", 
                            kpis=kpis,
                            revenue_labels=revenue_labels,
                            revenue_values=revenue_values,

                            season_labels=season_labels,
                            season_values=season_values,
                           
                            adr_labels=adr_labels,
                            adr_values=adr_values,

                            stay_labels=stay_labels,
                            stay_values=stay_values,

                            market_labels=market_labels,
                            market_values=market_values,

                            hotel_labels=hotel_labels,
                            hotel_values=hotel_values,

                            revenue_summary=revenue_summary
)

@app.route("/statistical-analysis")
def statistical_analysis():

    # Example placeholder values (replace with actual stats later)
    normality_test_p = 0.03
    correlation_r = 0.62
    anova_p = 0.04
    ci_low, ci_high = 350, 400

    kpis = {
        "normality_test": f"p={normality_test_p:.2f}",          # p=0.03
        "correlation": f"r={correlation_r:.2f}",                # r=0.62
        "hypothesis_tests": f"p<{anova_p:.2f}",                 # p<0.05
        "confidence_interval": f"[{ci_low}, {ci_high}]"         # [350, 400]
    }


    assumption_labels = ["Normality", "Homogeneity", "Correlation", "Multicollinearity"]

    assumption_status = [0, 0, 1, 0]
  

    # Histogram data for ADR
    counts, bins = np.histogram(df["adr"], bins=20)

    distribution_labels = []

    for i in range(len(bins)-1):
        distribution_labels.append(f"{bins[i]:.0f}-{bins[i+1]:.0f}")

    hypothesis_labels = ["t-Test", "ANOVA", "Chi-Square", "Mann-Whitney", "Kruskal-Wallis"]

    hypothesis_values = [55.8138, 1857.6878, 551.9297, 1108.985, 3938.9729]

    confidence_labels = ["Lower CI", "Mean ADR", "Upper CI"]

    confidence_values = [99.10, 101.83, 104.56]

    decision_labels = ["Significant", "Not Significant"]

    decision_values = [7, 0]

    statistical_summary = [

    {"test":"Shapiro-Wilk","statistic":"0.9735","p_value":"0.0000","result":"Failed"},

    {"test":"t-Test","statistic":"55.8138","p_value":"0.0000","result":"Significant"},

    {"test":"ANOVA","statistic":"1857.6878","p_value":"0.0000","result":" Significant"},

    {"test":"Chi-Square","statistic":"551.9297","p_value":"0.0000","result":"Significant"},

    {"test":"Mann-Whitney","statistic":"1108985000","p_value":"0.0000","result":" Significant"},

    {"test":"Kruskal-Wallis","statistic":"3938.9729","p_value":"0.0000","result":" Significant"},

    {"test":"Pearson","statistic":"0.0383","p_value":"0.0000","result":"Weak (+)"},

    {"test":"Spearman","statistic":"0.1109","p_value":"4.83E-230","result":"Weak (+)"}

    ]
       
    distribution_counts = counts.tolist()
    return render_template("statistical_analysis.html", 
                           kpis=kpis,

                           assumption_labels=assumption_labels,
                           assumption_status=assumption_status,

                            distribution_labels=distribution_labels,
                            distribution_counts=distribution_counts,

                            hypothesis_labels=hypothesis_labels,
                            hypothesis_values=hypothesis_values,

                            confidence_labels=confidence_labels,
                            confidence_values=confidence_values,

                            decision_labels=decision_labels,
                            decision_values=decision_values,

                            statistical_summary=statistical_summary

)

@app.route("/data-explorer")
def data_explorer():

    # KPI Cards

    kpis = {
        "total_records": f"{len(df):,}",
        "total_features": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_records": int(df.duplicated().sum())
    }

    # Dropdown Values

    countries = sorted(df["country"].dropna().unique())

    customer_groups = sorted(df["customer_group"].dropna().unique())

    booking_seasons = sorted(df["booking_season"].dropna().unique())

    booking_values = sorted(df["booking_value_segment"].dropna().unique())

    stay_types = sorted(df["stay_type"].dropna().unique())

    lead_categories = sorted(df["lead_time_category"].dropna().unique())

    reservation_status = sorted(df["reservation_status"].dropna().unique())

    # Copy Dataset

    filtered_df = df.copy()

    # Search

    search = request.args.get("search", "").strip()

    if search:

        filtered_df = filtered_df[
            filtered_df.astype(str)
            .apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
        ]

    # Filters

    country = request.args.get("country")

    if country:
        filtered_df = filtered_df[
            filtered_df["country"] == country
        ]


    customer_group = request.args.get("customer_group")

    if customer_group:
        filtered_df = filtered_df[
            filtered_df["customer_group"] == customer_group
        ]


    booking_season = request.args.get("booking_season")

    if booking_season:
        filtered_df = filtered_df[
            filtered_df["booking_season"] == booking_season
        ]


    booking_value = request.args.get("booking_value_segment")

    if booking_value:
        filtered_df = filtered_df[
            filtered_df["booking_value_segment"] == booking_value
        ]


    stay_type = request.args.get("stay_type")

    if stay_type:
        filtered_df = filtered_df[
            filtered_df["stay_type"] == stay_type
        ]


    lead_time = request.args.get("lead_time_category")

    if lead_time:
        filtered_df = filtered_df[
            filtered_df["lead_time_category"] == lead_time
        ]


    reservation = request.args.get("reservation_status")

    # Reservation Status

    if reservation is not None and reservation != "":
        filtered_df = filtered_df[
            filtered_df["reservation_status"] == int(reservation)
        ]

    # Pagination

    page = int(request.args.get("page", 1))

    per_page = int(request.args.get("per_page", 20))

    start = (page - 1) * per_page

    end = start + per_page

    rows = filtered_df.iloc[start:end].to_dict(orient="records")

    columns = filtered_df.columns.tolist()

    total_rows = len(filtered_df)

    has_next = end < total_rows

    return render_template("data_explorer.html", 
                           kpis=kpis,

                            rows=rows,
                            columns=columns,
                            page=page,
                            has_next=has_next,

                            total_rows=total_rows,

                            countries=countries,

                            customer_groups=customer_groups,

                            booking_seasons=booking_seasons,

                            booking_values=booking_values,

                            stay_types=stay_types,

                            lead_categories=lead_categories,

                            reservation_status=reservation_status,
                            
                            per_page=per_page,

    )


@app.route("/export-csv")
def export_csv():

    filtered_df = df.copy()

    # Search
    search = request.args.get("search", "").strip()

    if search:
        filtered_df = filtered_df[
            filtered_df.astype(str)
            .apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
        ]

    # Country
    country = request.args.get("country")
    if country:
        filtered_df = filtered_df[filtered_df["country"] == country]

    # Customer Group
    customer_group = request.args.get("customer_group")
    if customer_group:
        filtered_df = filtered_df[
            filtered_df["customer_group"] == customer_group
        ]

    # Booking Season
    booking_season = request.args.get("booking_season")
    if booking_season:
        filtered_df = filtered_df[
            filtered_df["booking_season"] == booking_season
        ]

    # Booking Value
    booking_value = request.args.get("booking_value_segment")
    if booking_value:
        filtered_df = filtered_df[
            filtered_df["booking_value_segment"] == booking_value
        ]

    # Stay Type
    stay_type = request.args.get("stay_type")
    if stay_type:
        filtered_df = filtered_df[
            filtered_df["stay_type"] == stay_type
        ]

    # Lead Time
    lead_time = request.args.get("lead_time_category")
    if lead_time:
        filtered_df = filtered_df[
            filtered_df["lead_time_category"] == lead_time
        ]

    reservation = request.args.get("reservation_status")

    if reservation != "":
        filtered_df = filtered_df[
            filtered_df["reservation_status"] == int(reservation)
        ]

    output = io.StringIO()

    filtered_df.to_csv(output, index=False)

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="filtered_hotel_booking_data.csv"
    )
 
@app.route("/reports")
def reports():

    kpis = {"total_reports": 6, "modules": 6, "formats": "PDF / CSV", "updated": "Today"}

    summary = {

        "total_records": f"{len(df):,}",

        "total_features": df.shape[1],

        "missing": int(df.isnull().sum().sum()),

        "duplicates": int(df.duplicated().sum())

    }

    return render_template("reports.html", kpis=kpis, summary=summary

)


if __name__ == "__main__":
    app.run(debug=True)
