from app import app, db, Booking
import plotly.graph_objs as go
from plotly.offline import plot
from collections import Counter

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