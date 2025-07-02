from app import app, db, Booking
import plotly.graph_objs as go
from plotly.offline import plot
from collections import Counter
from sqlalchemy import func

service_prices = {
    "Grand Canyon":120,
    "Niagara Falls":140,
    "Banff National Park":160,
    "New York":100,
    "Hawaii Islands":210,
    "Machu Picchu":130,
    "Rio de Janeiro":120,
    "Patagonia":150,
    "Galapagos":180,
    "Paris":120,
    "Rome":100,
    "Barcelona":110,
    "Blue Lagoon":150,
    "Swiss Alps":170,
    "Santorini":130,
    "Fjord":160,
    "Tokyo":140,
    "Bali":110,
    "Great Wall of China":130,
    "Taj Mahal":120,
    "Phuket":115,
    "Serengeti National Park":150,
    "Cape Town":130,
    "Victoria Falls":140,
    "Madagascar":135,
    "Pyramids of Giza":200,
    "Great Barrier Reef":220,
    "Sydney":180,
    "Uluru":210,
    "Antartica Peninsula":350
}

def generate_chart(place):
    with app.app_context():
        bookings = Booking.query.filter_by(destination=place).all()

        month_counts = Counter()
        for booking in bookings:
            if booking.start_date:
                month_counts[booking.start_date.month] += 1

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        visits = [month_counts.get(i, 0) for i in range(1, 13)]

        fig = go.Figure(data=[go.Bar(x=months, y=visits, marker_color='#c66995')])
        fig.update_layout(
            title=f"Number of Visits per Month for<br>{place} from Vetravel",
            xaxis_title="Month",
            yaxis_title="Number of Visits",
            template="plotly_white"
        )
        fig.update_layout(
            autosize=True,
            height=350,
            title={
                'text': f"Number of Visits per Month for<br>{place} from VeTravel",
                'x': 0.5,
                'xanchor': 'center'
            },
            margin=dict(l=40, r=40, t=60, b=40),
        )

        chart_div = plot(fig, output_type='div', include_plotlyjs=False)
        return chart_div
    

def generate_top_destinations_chart():
    with app.app_context():
        results = db.session.query(
            Booking.destination,
            func.count().label("count")
        ).group_by(Booking.destination).all()

        count_dict = {row.destination: row.count for row in results}

        fixed_order = list(service_prices.keys())
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
    with app.app_context():
        destinations = list(service_prices.keys())
        prices = [service_prices[dest] for dest in destinations]

        fig = go.Figure(data=[go.Bar(
            x=destinations,
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
    with app.app_context():
        destinations = list(service_prices.keys())  # fixed order

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
                'text': "Total Earnings per Destination from Services (Fixed Order)",
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
                                {"title": "Total Earnings per Destination from Services (Fixed Order)"}
                            ]
                        },
                        {
                            "label": "Sort by Earnings",
                            "method": "update",
                            "args": [
                                {"x": [destinations_sorted_for_rank], "y": [earnings_sorted], "text": [ranks_for_sorted]},
                                {"title": "Total Earnings per Destination from Services (Sorted)"}
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