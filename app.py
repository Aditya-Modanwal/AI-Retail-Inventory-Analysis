import matplotlib.pyplot as plt
import os
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

data = pd.read_csv("SuperMarket Sales Dataset.csv")


data['Date'] = pd.to_datetime(data['Date'])

daily_sales = data.groupby(["Date","Product line"])["Quantity"].sum().reset_index()

avg_daily_sales = daily_sales.groupby("Product line")["Quantity"].mean()

current_stock = {
    "Electronic accessories":120,
    "Fashion accessories":40,
    "Food and beverages":200,
    "Health and beauty":60,
    "Home and lifestyle":80,
    "Sports and travel":50
}

results = []

for product in avg_daily_sales.index:

    stock = current_stock[product]
    daily = avg_daily_sales[product]

    coverage = stock / daily

    if coverage > 60:
        status = "Overstock Risk"
    elif coverage < 15:
        status = "Stockout Risk"
    else:
        status = "Healthy"

    results.append({
        "product":product,
        "stock":stock,
        "daily_sales":round(daily,2),
        "coverage":round(coverage,1),
        "status":status
    })



# generate sales trend chart

sales_trend = data.groupby("Date")["Quantity"].sum()

plt.figure(figsize=(8,4))
plt.plot(sales_trend.index, sales_trend.values)

plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Units Sold")

chart_path = "static/sales_chart.png"

os.makedirs("static", exist_ok=True)

plt.savefig(chart_path)
plt.close()
@app.route("/")
def dashboard():
    return render_template("index.html",
                           results=results,
                           chart="static/sales_chart.png")

if __name__ == "__main__":
    app.run(debug=True)