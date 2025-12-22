import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--location", type=str, default="Valencia")
parser.add_argument("-x", type=str, default="Temp")
parser.add_argument("-y", type=str, default="Pressure")
args = parser.parse_args()

floods = pd.read_csv("inundaciones.csv")
locations = {"Valencia": "Valencia_bkp", "Houston": "Houston", "Bangkok": "Bangkok", "Mumbai": "Mumbai"}
flood_years = list(set([int(d.split("-")[0]) for d in floods["date"]]))

df = pd.read_csv(locations[args.location] + ".csv")
location_floods = floods[floods["localization"] == args.location]
flood_years = list(set([int(d.split("-")[0]) for d in location_floods["date"]]))
interest_dates = np.array(location_floods["date"])
for year in sorted(flood_years):
    indeces = [i for i, v in enumerate([int(d.split("-")[0]) == year for d in interest_dates]) if v]
    days = df["date"][df["date"].apply(lambda v: v.split("-")[0] == str(year))]
    colors = np.array(["blue" if not v else "green" for v in days.apply(lambda v: v in interest_dates[indeces]).tolist()])
    if args.x in ["Rain", "Soil"]:
        x = np.array([np.sum([df[df["date"] == day][f"{args.x}_{h:02}:00"] for h in range(24)]) for day in days])
    else:
        x = np.array([np.mean([df[df["date"] == day][f"{args.x}_{h:02}:00"] for h in range(24)]) for day in days])
    if args.y in ["Rain", "Soil"]:
        y = np.array([np.sum([df[df["date"] == day][f"{args.y}_{h:02}:00"] for h in range(24)]) for day in days])
    else:
        y = np.array([np.mean([df[df["date"] == day][f"{args.y}_{h:02}:00"] for h in range(24)]) for day in days])
    reg = LinearRegression().fit(x.reshape(-1, 1), y.reshape(-1, 1))
    pred = reg.coef_.item() * x + reg.intercept_
    fit = np.polyfit(x, np.log(y + 1e-6), 1)
    # v = np.exp(fit[1]) * np.exp(fit[0] * x)
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    rel_coeff = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / np.sqrt(sum((xi - mean_x) ** 2 for xi in x) * sum((yi - mean_y) ** 2 for yi in y))
    # import code; code.interact(local=locals())
    plt.figure(figsize=(16, 8))
    plt.title(f"{args.x} vs. {args.y} @ {year} - {args.location} | Rel. Coefficient: {rel_coeff:.2f}")
    plt.scatter(x, y, c=colors, s=y + 10, alpha=0.6, edgecolors='black', linewidth=0.5)
    plt.vlines(x=1013, ymin=min(y), ymax=max(y), colors="red", label="Pressure at sea level")
    # plt.plot(x, pred, c="red", label="Linear Regression")
    # plt.plot(sorted(x), sorted(v), c="red", label="Regression curve")
    plt.xlabel(f"{args.x} ({df[args.x + '_unit'][0]})")
    plt.ylabel(f"{args.y} ({df[args.y + '_unit'][0]})")
    plt.legend()
    plt.show()
