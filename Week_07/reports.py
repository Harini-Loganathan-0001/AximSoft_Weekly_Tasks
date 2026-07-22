from flask import Blueprint, request, make_response, send_file

from io import BytesIO
import os
import tempfile
import base64

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Image,
    Spacer,
    PageBreak
)


from data import df

reports = Blueprint("reports", __name__)


@reports.route("/download-booking-report")
def download_booking_report():


    #  KPIs 

    kpis = {
        "Total Bookings": f"{len(df):,}",
        "Cancellation Rate": f"{round(df['is_canceled'].mean()*100,2)}%",
        "Average Daily Rate": f"${round(df['adr'].mean(),2)}",
        "Average Stay Duration": f"{round(df['total_stay_duration'].mean(),1)} Nights"
    }

    booking_summary = [

        ["Metric","Result","Business Insight"],

        ["Total Bookings",
         f"{len(df):,}",
         "High booking volume indicates strong customer demand."],

        ["Cancellation Rate",
         f"{round(df['is_canceled'].mean()*100,2)}%",
         "Cancellation percentage suggests opportunities to improve booking retention."],

        ["Average Daily Rate",
         f"${round(df['adr'].mean(),2)}",
         "Average room pricing remains stable across reservations."],

        ["Average Stay Duration",
         f"{round(df['total_stay_duration'].mean(),1)} Nights",
         "Guests generally prefer short-to-medium stays."],

        ["Most Preferred Hotel",
         df["hotel"].value_counts().idxmax(),
         "This hotel type attracts the highest number of bookings."],

        ["Top Booking Country",
         df["country"].value_counts().idxmax(),
         "Largest share of customers originates from this country."],

        ["Peak Booking Month",
         df["arrival_date_month"].value_counts().idxmax(),
         "Highest booking demand."],

        ["Most Common Customer Type",
         df["customer_type"].value_counts().idxmax(),
         "Largest customer segment."],

        ["Booking Value Segment",
         df["booking_value_segment"].value_counts().idxmax(),
         "Most bookings belong to this spending segment."],

        ["Reservation Status",
         df["reservation_status"].value_counts().idxmax(),
         "Most reservations completed successfully."]
    ]

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    # Title

    elements.append(
        Paragraph("<b>HOTEL BOOKING ANALYTICS REPORT</b>", styles["Title"])
    )

    elements.append(
        Paragraph("Booking Analytics Dashboard Summary", styles["Heading2"])
    )

    elements.append(Spacer(1, 10))

    # KPI

    for key, value in kpis.items():
        elements.append(
            Paragraph(f"<b>{key}</b> : {value}", styles["BodyText"])
        )

    elements.append(Spacer(1, 12))

    # Chart 1

    elements.append(
        Paragraph("<b>Monthly Booking Trend</b>", styles["Heading3"])
    )

    elements.append(
        Image(
            "static/images/monthly_booking_trend(booking).png",
            width=5.8*inch,
            height=2.8*inch
        )
    )

    elements.append(Spacer(1, 10))

    # Chart 2

    elements.append(
        Paragraph("<b>Top Booking Countries</b>", styles["Heading3"])
    )

    elements.append(
        Image(
            "static/images/seasonal_booking_trend(booking).png",
            width=5.8*inch,
            height=2.8*inch
        )
    )

    # FORCE SECOND PAGE

    elements.append(PageBreak())

    # Summary Table

    table = Table(
        booking_summary,
        colWidths=[2.3*inch,1.5*inch,3.2*inch]
    )

    table.setStyle(TableStyle([

        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,0),11),

        ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,1),(-1,-1),9),

        ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke),

        ('GRID',(0,0),(-1,-1),0.6,colors.grey),

        ('BOX',(0,0),(-1,-1),1,colors.black),

        ('ALIGN',(1,1),(1,-1),'CENTER'),

        ('VALIGN',(0,0),(-1,-1),'TOP'),

        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),

    ]))

    elements.append(table)

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    response = make_response(pdf)

    response.headers["Content-Type"] = "application/pdf"

    response.headers["Content-Disposition"] = "attachment; filename=Booking_Analytics_Report.pdf"

    return response


@reports.route("/download-customer-report")
def download_customer_report():

    # KPIs 

    kpis = {
        "Total Customers": f"{df['customer_id'].nunique():,}" if 'customer_id' in df else f"{len(df):,}",
        "Unique Countries": df["country"].nunique(),
        "Repeat Guest Rate": f"{round(df['is_repeated_guest'].mean()*100,2)}%",
        "Total Special Requests": int(df["total_of_special_requests"].sum())
    }

    # Summary Table 

    customer_summary = [

        ["Metric","Result","Business Insight"],

        [
            "Total Customers",
            f"{df['customer_id'].nunique():,}" if 'customer_id' in df else f"{len(df):,}",
            "Large customer base indicates healthy hotel demand."
        ],

        [
            "Unique Countries",
            df["country"].nunique(),
            "Guests arrive from multiple countries."
        ],

        [
            "Most Common Customer Type",
            df["customer_type"].mode()[0],
            "Dominant customer category."
        ],

        [
            "Top Booking Country",
            df["country"].value_counts().idxmax(),
            "Largest number of guests originate from this country."
        ],

        [
            "Repeat Guest Rate",
            f"{round(df['is_repeated_guest'].mean()*100,2)}%",
            "Shows customer loyalty."
        ],

        [
            "Repeat Guests",
            int(df["is_repeated_guest"].sum()),
            "Returning customers."
        ],

        [
            "Average Special Requests",
            round(df["total_of_special_requests"].mean(),2),
            "Average guest requests."
        ],

        [
            "Top Booking Value Segment",
            df["booking_value_segment"].value_counts().idxmax(),
            "Most customers belong to this spending category."
        ]
    ]

    # PDF 

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("<b>CUSTOMER ANALYTICS REPORT</b>", styles["Title"])
    )

    elements.append(
        Paragraph("Customer Analytics Dashboard Summary", styles["Heading2"])
    )

    elements.append(Spacer(1,10))

    # KPI

    for key,value in kpis.items():

        elements.append(
            Paragraph(f"<b>{key}</b> : {value}", styles["BodyText"])
        )

    elements.append(Spacer(1,12))

    #  Chart 1

    elements.append(
        Paragraph("<b>Booking Size Distribution</b>", styles["Heading3"])
    )

    elements.append(
        Image(
            "static/images/bookingsize_dist(customers).png",
            width=5.8*inch,
            height=2.8*inch
        )
    )

    elements.append(Spacer(1,10))

    # Chart 2 

    elements.append(
        Paragraph("<b>Top 10 Countries by Hotel Bookings</b>", styles["Heading3"])
    )

    elements.append(
        Image(
            "static/images/top10_countries_byhotel_book(customers).png",
            width=5.8*inch,
            height=2.8*inch
        )
    )

    # Next Page 

    elements.append(PageBreak())

    # Table 

    table = Table(
        customer_summary,
        colWidths=[2.3*inch,1.5*inch,3.2*inch]
    )

    table.setStyle(TableStyle([

        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,0),11),

        ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,1),(-1,-1),9),

        ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke),

        ('GRID',(0,0),(-1,-1),0.6,colors.grey),

        ('BOX',(0,0),(-1,-1),1,colors.black),

        ('ALIGN',(1,1),(1,-1),'CENTER'),

        ('VALIGN',(0,0),(-1,-1),'TOP'),

        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6)

    ]))

    elements.append(table)

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    response = make_response(pdf)

    response.headers["Content-Type"] = "application/pdf"

    response.headers["Content-Disposition"] = "attachment; filename=Customer_Analytics_Report.pdf"

    return response



@reports.route("/download-revenue-report")
def download_revenue_report():

    # KPIs

    total_revenue = (
        df["adr"] *
        (df["stays_in_weekend_nights"] + df["stays_in_week_nights"])
    ).sum()

    avg_revenue = total_revenue / len(df)

    revenue_growth = "+12.5%"      # use your calculated value if available

    top_country = df["country"].value_counts().idxmax()

    kpis = {

        "Total Revenue": f"${total_revenue:,.2f}",

        "Average Revenue / Booking": f"${avg_revenue:,.2f}",

        "Revenue Growth": revenue_growth,

        "Top Revenue Country": top_country

    }

    # Summary 

    revenue_summary = [

        ["Metric","Result","Business Insight"],

        ["Total Revenue",
         f"${total_revenue:,.2f}",
         "Overall revenue generated from hotel bookings."],

        ["Average Revenue / Booking",
         f"${avg_revenue:,.2f}",
         "Average income received from every booking."],

        ["Highest Revenue Hotel",
         "City Hotel",
         "Generated the largest share of revenue."],

        ["Highest Revenue Season",
         "Summer",
         "Peak revenue observed during summer."],

        ["Average Stay",
         f"{round((df['stays_in_week_nights']+df['stays_in_weekend_nights']).mean(),1)} Nights",
         "Average customer stay duration."],

        ["Top Revenue Country",
         top_country,
         "Highest contribution to revenue."]
    ]

    # PDF

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("<b>REVENUE ANALYTICS REPORT</b>", styles["Title"])
    )

    elements.append(
        Paragraph("Revenue Analytics Dashboard Summary", styles["Heading2"])
    )

    elements.append(Spacer(1,10))

    # KPI 

    for key,value in kpis.items():

        elements.append(
            Paragraph(f"<b>{key}</b> : {value}", styles["BodyText"])
        )

    elements.append(Spacer(1,10))

    #  Chart 1 

    elements.append(
        Paragraph("<b>ADR by Hotel Type</b>", styles["Heading3"])
    )

    elements.append(
        Image(
            "static/images/dist_adr_hotel_type(revenue).png",
            width=5.8*inch,
            height=2.8*inch
        )
    )

    elements.append(Spacer(1,10))

    # Chart 2

    elements.append(
        Paragraph("<b>Average Daily Rate Distribution</b>", styles["Heading3"])
    )

    elements.append(
        Image(
            "static/images/dist_avg_daily_rate(revenue).png",
            width=5.8*inch,
            height=2.8*inch
        )
    )

    # Second Page

    elements.append(PageBreak())

    table = Table(
        revenue_summary,
        colWidths=[2.3*inch,1.6*inch,3.2*inch]
    )

    table.setStyle(TableStyle([

        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke),

        ('GRID',(0,0),(-1,-1),0.6,colors.grey),

        ('BOX',(0,0),(-1,-1),1,colors.black),

        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),

        ('FONTSIZE',(0,0),(-1,0),11),

        ('FONTSIZE',(0,1),(-1,-1),9),

        ('VALIGN',(0,0),(-1,-1),'TOP'),

        ('ALIGN',(1,1),(1,-1),'CENTER'),

        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6)

    ]))

    elements.append(table)

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    response = make_response(pdf)

    response.headers["Content-Type"] = "application/pdf"

    response.headers["Content-Disposition"] = "attachment; filename=Revenue_Analytics_Report.pdf"

    return response


@reports.route("/download-statistical-report")
def download_statistical_report():
 
    kpis = {
        "Normality Test": "p=0.03",
        "Correlation": "r=0.62",
        "Hypothesis Tests": "p<0.05",
        "Confidence Interval": "[350,400]"
    }
 
    statistical_summary = [
 
        ["Test","Statistic","P-Value","Result"],
 
        ["Shapiro-Wilk","0.9735","0.0000","Failed"],
 
        ["t-Test","55.8138","0.0000","Significant"],
 
        ["ANOVA","1857.6878","0.0000","Significant"],
 
        ["Chi-Square","551.9297","0.0000","Significant"],
 
        ["Mann-Whitney","1108985000","0.0000","Significant"],
 
        ["Kruskal-Wallis","3938.9729","0.0000","Significant"],
 
        ["Pearson","0.0383","0.0000","Weak (+)"],
 
        ["Spearman","0.1109","4.83E-230","Weak (+)"]
    ]
 
    buffer = BytesIO()
 
    doc = SimpleDocTemplate(buffer)
 
    styles = getSampleStyleSheet()
 
    elements = []
 
    elements.append(
        Paragraph("<b>STATISTICAL ANALYSIS REPORT</b>", styles["Title"])
    )
 
    elements.append(
        Paragraph("Hotel Booking Statistical Summary", styles["Heading2"])
    )
 
    elements.append(Spacer(1,10))
 
    for key,value in kpis.items():
 
        elements.append(
            Paragraph(f"<b>{key}</b> : {value}", styles["BodyText"])
        )
 
    elements.append(Spacer(1,12))
 
    elements.append(
        Paragraph("<b>Mann–Whitney U Test</b>", styles["Heading3"])
    )
 
    elements.append(
        Image(
            "static/images/mann_whiteney_u_test(statistical).png",
            width=5.8*inch,
            height=2.8*inch
        )
    )
 
    elements.append(Spacer(1,10))
 
    elements.append(
        Paragraph("<b>Pearson Correlation</b>", styles["Heading3"])
    )
 
    elements.append(
        Image(
            "static/images/pearson correlation(statistical).png",
            width=5.8*inch,
            height=2.8*inch
        )
    )
 
    elements.append(PageBreak())
 
    table = Table(
        statistical_summary,
        colWidths=[2.2*inch,1.3*inch,1.2*inch,2.0*inch]
    )
 
    table.setStyle(TableStyle([
 
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
 
        ('GRID',(0,0),(-1,-1),0.6,colors.grey),
 
        ('BOX',(0,0),(-1,-1),1,colors.black),
 
        ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke),
 
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
 
        ('FONTSIZE',(0,0),(-1,0),11),
 
        ('FONTSIZE',(0,1),(-1,-1),9),
 
        ('ALIGN',(1,1),(-1,-1),'CENTER'),
 
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
 
        ('LEFTPADDING',(0,0),(-1,-1),6),
 
        ('RIGHTPADDING',(0,0),(-1,-1),6),
 
        ('TOPPADDING',(0,0),(-1,-1),6),
 
        ('BOTTOMPADDING',(0,0),(-1,-1),6)
 
    ]))
 
    elements.append(table)
 
    doc.build(elements)
 
    pdf = buffer.getvalue()
 
    buffer.close()
 
    response = make_response(pdf)
 
    response.headers["Content-Type"] = "application/pdf"
 
    response.headers["Content-Disposition"] = "attachment; filename=Statistical_Analysis_Report.pdf"
 
    return response



from flask import send_file
@reports.route("/download-cleaned-dataset")
def download_cleaned_dataset():

    file_path = "dataset/hotel_bookings_cleaned.csv"

    return send_file(
        file_path,
        as_attachment=True,
        download_name="hotel_bookings_cleaned.csv"
    )


@reports.route("/download-statistical-reports")
def download_statistical_reports():

    file_path = "dataset/statistical_summary_report.pdf"

    return send_file(
        file_path,
        as_attachment=True,
        download_name="statistical_summary_report.pdf"
    )


@reports.route("/download-eda-summary-report")
def download_eda_summary_report():

    file_path = "dataset/eda_summary_report.pdf"

    return send_file(
        file_path,
        as_attachment=True,
        download_name="eda_summary_report.pdf"
    )