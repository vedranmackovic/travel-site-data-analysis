from models import db, Booking, Destination
import plotly.graph_objs as go
from plotly.offline import plot
from collections import Counter
from sqlalchemy import func, distinct, literal_column
from datetime import datetime

def generate_chart(place):
    bookings = Booking.query.filter_by(destination=place).all()

    month_counts = Counter()
    for booking in bookings:
        if booking.start_date:
            month_counts[booking.start_date.month] += 1

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    visits = [month_counts.get(i, 0) for i in range(1, 13)]

    fig = go.Figure(data=[go.Bar(
        x=months, 
        y=visits, 
        marker_color='#c66995'
    )])
    
    fig.update_layout(
        autosize=True,
        height=350,
        title={
            'text': f"Number of Visits per Month for<br>{place} from VeTravel",
            'x': 0.5,
            'xanchor': 'center'
        },
                    xaxis_title="Month",
        yaxis_title="Number of Visits",
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=40),
    )

    chart_div = plot(fig, output_type='div', include_plotlyjs=False)
    return chart_div
    

def generate_top_destinations_chart():
    destination_objs = Destination.query.all()
    results = db.session.query(
        Booking.destination,
        func.count().label("count")
    ).group_by(Booking.destination).all()

    count_dict = {row.destination: row.count for row in results}

    fixed_order = [d.name for d in destination_objs]
    counts_fixed = [count_dict.get(dest, 0) for dest in fixed_order]

    sorted_by_popularity = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
    destinations_pop = [dest for dest, _ in sorted_by_popularity]

    rank_dict = {dest: str(i + 1) for i, dest in enumerate(destinations_pop)}

    ranks_for_fixed_order = [rank_dict.get(dest, "") for dest in fixed_order]

    fig = go.Figure(data=[go.Bar(
        x=fixed_order,
        y=counts_fixed,
        marker_color="#69c6ba",
        text=ranks_for_fixed_order,
        textposition='auto'
    )])

    fig.update_layout(
        title={
            'text': "Top Destinations on VeTravel",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Destination",
        yaxis_title="Number of Travelers",
        height=500,
        margin=dict(l=40, r=40, t=60, b=80),
        template="plotly_white",
        updatemenus=[
            {
                "buttons": [
                    {
                        "label": "Fixed Order",
                        "method": "update",
                        "args": [
                            {"x": [fixed_order], "y": [counts_fixed], "text": [ranks_for_fixed_order]},
                            {"title": "Top Destinations on VeTravel"}
                        ],
                    },
                    {
                        "label": "Sort by Popularity",
                        "method": "update",
                        "args": [
                            {"x": [destinations_pop], "y": [list(count_dict[dest] for dest in destinations_pop)], "text": [list(str(i+1) for i in range(len(destinations_pop)))]},
                            {"title": "Top Destinations on VeTravel (by Popularity)"}
                        ],
                    }
                ],
                "direction": "down",
                "showactive": True,
                "x": 0,
                "xanchor": "left",
                "y": 1.05,
                "yanchor": "bottom"
            }
        ]
    )

    return plot(fig, output_type="div", include_plotlyjs=False)
    

def generate_service_cost_chart():
    destinations = Destination.query.all()
    dest_names = [dest.name for dest in destinations]
    prices = [dest.service_price for dest in destinations]

    fig = go.Figure(data=[go.Bar(
        x=dest_names,
        y=prices,
        marker_color="#c66995"
    )])

    fig.update_layout(
        title={
            'text': "Service Cost for Destination",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Destination",
        yaxis_title="Service Cost ($)",
        height=400,
        margin=dict(l=40, r=40, t=60, b=80),
        template="plotly_white"
    )

    return plot(fig, output_type="div", include_plotlyjs=False)
    

def generate_total_earnings_chart():
    destination_objs = Destination.query.all()
    destinations = [d.name for d in destination_objs]
    service_prices = {d.name: d.service_price for d in destination_objs}

    results = db.session.query(
        Booking.destination,
        func.count().label("count")
    ).group_by(Booking.destination).all()
    counts_dict = {row.destination: row.count for row in results}

    earnings_fixed = [
        counts_dict.get(dest, 0) * service_prices.get(dest, 0)
        for dest in destinations
    ]

    earnings_dict = {dest: counts_dict.get(dest, 0) * service_prices.get(dest, 0) for dest in destinations}

    sorted_by_earnings = sorted(earnings_dict.items(), key=lambda x: x[1], reverse=True)
    destinations_sorted_for_rank = [dest for dest, _ in sorted_by_earnings]
    earnings_sorted = [earn for _, earn in sorted_by_earnings]

    rank_dict = {dest: str(i + 1) for i, dest in enumerate(destinations_sorted_for_rank)}

    ranks_for_fixed_order = [rank_dict.get(dest, "") for dest in destinations]
    ranks_for_sorted = [str(i + 1) for i in range(len(destinations_sorted_for_rank))]

    fig = go.Figure(data=[go.Bar(
        x=destinations,
        y=earnings_fixed,
        marker_color="green",
        text=ranks_for_fixed_order,
        textposition='auto'
    )])

    fig.update_layout(
        margin=dict(l=40, r=40, t=100, b=80),
        title={
            'text': "Total Earnings per Destination from Services",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Destination",
        yaxis_title="Total Earnings ($)",
        height=400,
        template="plotly_white",
        updatemenus=[
            {
                "buttons": [
                    {
                        "label": "Fixed Order",
                        "method": "update",
                        "args": [
                            {"x": [destinations], "y": [earnings_fixed], "text": [ranks_for_fixed_order]},
                            {"title": "Total Earnings per Destination from Services"}
                        ]
                    },
                    {
                        "label": "Sort by Earnings",
                        "method": "update",
                        "args": [
                            {"x": [destinations_sorted_for_rank], "y": [earnings_sorted], "text": [ranks_for_sorted]},
                            {"title": "Total Earnings per Destination from Services (By Earnings)"}
                        ]
                    },
                ],
                "direction": "down",
                "showactive": True,
                "x": 0,
                "xanchor": "left",
                "y": 1.05,
                "yanchor": "bottom",
                "pad": {"t": 2, "b": 2, "l": 5, "r": 5},
            }
        ]
    )

    return plot(fig, output_type="div", include_plotlyjs=False)
    

def generate_age_group_chart():
    results = db.session.query(Booking.traveler_age).all()
    ages = [row.traveler_age for row in results if row.traveler_age is not None]

    bins = {}
    for age in ages:
        if age < 11:
            continue 
        lower = ((age - 1) // 10) * 10 + 1
        upper = lower + 9
        label = f"{lower}-{upper}"
        bins[label] = bins.get(label, 0) + 1

    sorted_labels = sorted(bins.keys(), key=lambda x: int(x.split('-')[0]))
    counts = [bins[label] for label in sorted_labels]

    fig = go.Figure(data=[go.Bar(
        x=sorted_labels,
        y=counts,
        marker_color="#6a9fb5"
    )])

    fig.update_layout(
        title={
            'text': "Traveler Age Groups",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Age Group",
        yaxis_title="Number of Travelers",
        height=400,
        margin=dict(l=40, r=40, t=60, b=80),
        template="plotly_white"
    )

    return plot(fig, output_type="div", include_plotlyjs=False)
    

def generate_gender_by_destination_chart():
    results = db.session.query(
        Booking.destination,
        Booking.traveler_gender,
        func.count().label("count")
    ).group_by(Booking.destination, Booking.traveler_gender).all()

    gender_data = {}
    for destination, gender, count in results:
        if destination not in gender_data:
            gender_data[destination] = {"Male": 0, "Female": 0}
        gender_data[destination][gender] = count

    destinations = [d.name for d in Destination.query.all()]
    male_counts = [gender_data.get(dest, {}).get("Male", 0) for dest in destinations]
    female_counts = [gender_data.get(dest, {}).get("Female", 0) for dest in destinations]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=destinations,
        y=male_counts,
        name='Male',
        marker_color='#4A90E2'
    ))

    fig.add_trace(go.Bar(
        x=destinations,
        y=female_counts,
        name='Female',
        marker_color='#FF6F91'
    ))

    fig.update_layout(
        barmode='group',
        title={
            'text': "Traveler Gender Distribution per Destination",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Destination",
        yaxis_title="Number of Travelers",
        height=400,
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=120),
        xaxis=dict(
            tickangle=0,
            tickfont=dict(size=10),
            tickmode='array',
            tickvals=list(range(len(destinations))),
            ticktext=[
                '<br>'.join(dest[i:i+10] for i in range(0, len(dest), 10))
                for dest in destinations
            ],
            fixedrange=False,
            range=[-0.5, 4.5]
        ),
        yaxis=dict(
            fixedrange=True
        ),
        dragmode="pan"
    )

    return plot(fig, output_type="div", include_plotlyjs=False)
    

def generate_nationality_pie_chart():
    results = db.session.query(
        Booking.traveler_nationality,
        func.count(
            distinct(
                func.concat(Booking.traveler_name, '-', Booking.traveler_nationality)
            )
        ).label("count")
    ).group_by(Booking.traveler_nationality).all()

    sorted_results = sorted(results, key=lambda x: x.count, reverse=True)

    top_n = 10
    top_labels = []
    top_values = []
    others_total = 0

    for i, row in enumerate(sorted_results):
        if i < top_n:
            top_labels.append(row.traveler_nationality or "Unknown")
            top_values.append(row.count)
        else:
            others_total += row.count

    if others_total > 0:
        top_labels.append("Others")
        top_values.append(others_total)

    fig = go.Figure(data=[go.Pie(
        labels=top_labels,
        values=top_values,
        hole=0.3,  # donut-style
        textinfo='label+percent',
        marker=dict(
            line=dict(color='white', width=1)
        )
    )])

    fig.update_layout(
        title={
            'text': "Traveler Nationalities (Top 10)",
            'x': 0.5,
            'xanchor': 'center'
        },
        height=400,
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=60),
    )

    return plot(fig, output_type="div", include_plotlyjs=False)
    

def generate_top_travelers_chart():
    results = db.session.query(
        func.concat(Booking.traveler_name, " - ", Booking.traveler_nationality).label("traveler"),
        Booking.traveler_gender,
        func.count().label("trips")
    ).group_by("traveler").order_by(func.count().desc()).limit(10).all()

    travelers = [row.traveler for row in results]
    genders = [row.traveler_gender for row in results]
    names = [traveler.split(" - ")[0] for traveler in travelers]
    trips = [row.trips for row in results]

    colors = ['steelblue' if gender == 'Male' else 'lightcoral' for gender in genders]

    fig = go.Figure(data=[go.Bar(
        x=names,
        y=trips,
        marker_color=colors
    )])

    fig.update_layout(
        title={
            'text': "Top 10 Travelers by Number of Travels",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Travelers",
        yaxis_title="Number of Travels",
        height=400,
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=80),
        xaxis=dict(tickangle=-45)
    )

    return plot(fig, output_type="div", include_plotlyjs=False)
    

def generate_accommodation_spent_chart():
    results = db.session.query(
        Booking.destination,
        func.sum(Booking.accommodation_cost).label("total")
    ).group_by(Booking.destination).all()

    filtered_results = [(dest, total) for dest, total in results if total and total > 0]

    sorted_results = sorted(filtered_results, key=lambda x: x[1], reverse=True)
    destinations = [row[0] for row in sorted_results]
    totals = [row[1] for row in sorted_results]

    fig = go.Figure(go.Bar(
        x=totals,
        y=destinations,
        orientation='h',
        marker_color="#69c6ba"
    ))

    fig.update_layout(
        title={
            'text': "Accommodation Spending per Location",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Total Spent ($)",
        yaxis_title="Destination",
        height=600,
        template="plotly_white",
        margin=dict(l=80, r=40, t=60, b=60),
    )

    return plot(fig, output_type="div", include_plotlyjs=False)


def generate_transport_spent_chart():
    results = db.session.query(
        Booking.destination,
        func.sum(Booking.transport_cost).label("total")
    ).group_by(Booking.destination).all()

    filtered_results = [(dest, total) for dest, total in results if total and total > 0]

    sorted_results = sorted(filtered_results, key=lambda x: x[1],reverse=True)
    destinations =[row[0] for row in sorted_results]
    totals = [row[1] for row in sorted_results]

    fig = go.Figure(go.Bar(
        x = totals,
        y = destinations,
        orientation = 'h',
        marker_color = "#6a9bd8"
    ))

    fig.update_layout(
        title={
            'text' : "Transport Spending per Location",
            'x' : 0.5,
            'xanchor' : 'center'
        },
        xaxis_title = "Total Spent ($)",
        yaxis_title = "Destination",
        height = 600,
        template = "plotly_white",
        margin = dict(l=80,r=40,t=60,b=60)
    )

    return plot(fig, output_type='div', include_plotlyjs=False)


def generate_total_cost_spent_chart():
    destination_objs = Destination.query.all()
    places = [d.name for d in destination_objs]
    service_prices = {d.name: d.service_price for d in destination_objs}
    results = db.session.query(
        Booking.destination,
        func.count().label("count"),
        func.sum(Booking.transport_cost).label("tcost"),
        func.sum(Booking.accommodation_cost).label("acost")
    ).group_by(Booking.destination).all()

    counts_dict = {row.destination : row.count for row in results}
    service_cost_dict = {dest: counts_dict.get(dest, 0) * service_prices.get(dest, 0) for dest in places}
    transport_dict = {row.destination: row.tcost or 0 for row in results}
    accommodation_dict = {row.destination: row.acost or 0 for row in results}

    total_cost = {dest: service_cost_dict.get(dest, 0) + transport_dict.get(dest, 0) + accommodation_dict.get(dest, 0)
                    for dest in places}

    sorted_results = sorted(total_cost.items(), key=lambda x: x[1], reverse=True)
    destinations = [item[0] for item in sorted_results]
    totals = [item[1] for item in sorted_results]

    fig = go.Figure(data=go.Bar(
        x=destinations,
        y=totals,
        marker_color="#3d6e70"
    ))

    fig.update_layout(
        title={
            'text': "Total Cost Spent per Location",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Destination",
        yaxis_title="Total Spent ($)",
        height=400,
        template="plotly_white",
        margin=dict(l=60, r=40, t=60, b=60)
    )

    return plot(fig, output_type='div', include_plotlyjs=False)


def generate_avg_total_cost_chart():
    destination_objs = Destination.query.all()
    service_prices = {d.name: d.service_price for d in destination_objs}
    
    results = db.session.query(
        Booking.destination,
        func.count().label("count"),
        func.sum(Booking.transport_cost).label("tcost"),
        func.sum(Booking.accommodation_cost).label("acost")
    ).group_by(Booking.destination).all()

    avg_costs = {}
    for row in results:
        dest = row.destination
        count = row.count
        tcost = row.tcost or 0
        acost = row.acost or 0
        service = service_prices.get(dest, 0)

        if count > 0:
            total_cost = tcost + acost + (service * count)
            avg_costs[dest] = total_cost / count

    sorted_results = sorted(avg_costs.items(), key=lambda x: x[1], reverse=True)
    destinations = [item[0] for item in sorted_results]
    averages = [round(item[1], 2) for item in sorted_results]

    fig = go.Figure(data=go.Bar(
        x=averages,
        y=destinations,
        orientation='h',
        marker_color="#f4a261"
    ))

    fig.update_layout(
        title={
            'text': "Average Total Cost per Traveler per Location",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Average Cost ($)",
        yaxis_title="Destination",
        height=600,
        template="plotly_white",
        margin=dict(l=80, r=40, t=60, b=60)
    )

    return plot(fig, output_type='div', include_plotlyjs=False)
    

def generate_min_total_cost_chart():
    results = db.session.query(
        Booking.destination,
        Booking.accommodation_cost,
        Booking.transport_cost
    ).filter(
        Booking.accommodation_cost != None,
        Booking.transport_cost != None,
        Booking.accommodation_cost > 0,
        Booking.transport_cost > 0
    ).all()
    destination_objs = Destination.query.all()
    service_prices = {d.name: d.service_price for d in destination_objs}

    min_costs = {}

    for destination, accom, trans in results:
        service_cost = service_prices.get(destination, 0)
        total = accom + trans + service_cost

        if destination not in min_costs or total < min_costs[destination]:
            min_costs[destination] = total

    sorted_results = sorted(min_costs.items(), key=lambda x: x[1], reverse=True)
    destinations = [item[0] for item in sorted_results]
    min_values = [round(item[1], 2) for item in sorted_results]

    fig = go.Figure(data=go.Bar(
        x=min_values,
        y=destinations,
        orientation='h',
        marker_color="#8ec07c"
    ))

    fig.update_layout(
        title={
            'text': "Minimum Total Cost per Location",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Minimum Total Cost ($)",
        yaxis_title="Destination",
        height=600,
        template="plotly_white",
        margin=dict(l=80, r=40, t=60, b=60)
    )

    return plot(fig, output_type='div', include_plotlyjs=False)
    

def generate_monthly_trend_chart(destination):
    results = (
        db.session.query(
            func.strftime('%Y-%m', Booking.start_date).label("month"),
            func.count().label("count")
        )
        .filter(Booking.destination == destination)
        .group_by("month")
        .order_by("month")
        .all()
    )
    
    months = [row[0] for row in results]
    counts = [row[1] for row in results]

    fig = go.Figure(data=go.Scatter(
        x=months, 
        y=counts, 
        mode='lines+markers', 
        marker_color="#3366CC"
    ))

    fig.update_layout(
        title=f"Monthly Trip Trends: {destination}",
        xaxis_title="Month",
        yaxis_title="Number of Trips",
        height=400,
        template="plotly_white"
    )

    return plot(fig, output_type='div', include_plotlyjs=False)


def generate_monthly_total_cost_chart(destination):
    results = (
        db.session.query(
            func.strftime('%Y-%m', Booking.start_date).label("month"),
            func.sum(Booking.transport_cost).label("tcost"),
            func.sum(Booking.accommodation_cost).label("acost"),
            func.count().label("count")
        )
        .filter(Booking.destination == destination)
        .group_by("month")
        .order_by("month")
        .all()
    )
    destination_objs = Destination.query.all()
    service_prices = {d.name: d.service_price for d in destination_objs}

    months = [row.month for row in results]
    service_cost = [service_prices.get(destination, 0) * row.count for row in results]
    transport_cost = [row.tcost or 0 for row in results]
    accommodation_cost = [row.acost or 0 for row in results]
    total_costs = [s + t + a for s, t, a in zip(service_cost, transport_cost, accommodation_cost)]

    fig = go.Figure(data=go.Scatter(
        x=months,
        y=total_costs,
        mode='lines+markers',
        marker_color="#cc6633"
    ))

    fig.update_layout(
        title=f"Monthly Total Cost for {destination}",
        xaxis_title="Month",
        yaxis_title="Total Cost ($)",
        height=400,
        template="plotly_white"
    )

    return plot(fig, output_type='div', include_plotlyjs=False)


def generate_yearly_trend_chart(destination):
    results = (
        db.session.query(
            func.strftime('%Y', Booking.start_date).label("year"),
            func.count().label("count")
        )
        .filter(Booking.destination == destination)
        .group_by("year")
        .order_by("year")
        .all()
    )
    
    years = [row[0] for row in results]
    counts = [row[1] for row in results]

    fig = go.Figure(data=go.Scatter(
        x=years, 
        y=counts, 
        mode='lines+markers', 
        marker_color="#FF6F91"
    ))

    fig.update_layout(
        title=f"Yearly Trip Trends: {destination}",
        xaxis_title="Years",
        yaxis_title="Number of Trips",
        height=400,
        template="plotly_white"
    )

    return plot(fig, output_type='div', include_plotlyjs=False)


def generate_yearly_total_cost_chart(destination):
    results = (
        db.session.query(
            func.strftime('%Y', Booking.start_date).label("year"),
            func.sum(Booking.transport_cost).label("tcost"),
            func.sum(Booking.accommodation_cost).label("acost"),
            func.count().label("count")
        )
        .filter(Booking.destination == destination)
        .group_by("year")
        .order_by("year")
        .all()
    )
    destination_objs = Destination.query.all()
    service_prices = {d.name: d.service_price for d in destination_objs}

    years = [row.year for row in results]
    service_cost = [service_prices.get(destination, 0) * row.count for row in results]
    transport_cost = [row.tcost or 0 for row in results]
    accommodation_cost = [row.acost or 0 for row in results]
    total_costs = [s + t + a for s, t, a in zip(service_cost, transport_cost, accommodation_cost)]

    fig = go.Figure(data=go.Scatter(
        x=years,
        y=total_costs,
        mode='lines+markers',
        marker_color="#4A90E2"
    ))

    fig.update_layout(
        title=f"Yearly Total Cost: {destination}",
        xaxis_title="Year",
        yaxis_title="Total Cost ($)",
        height=400,
        template="plotly_white"
    )

    return plot(fig, output_type='div', include_plotlyjs=False)   