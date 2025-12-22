import csv
from tqdm import tqdm
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
import requests
from requests.exceptions import ConnectionError
import pickle
import os

def get_data(lat: float, lon: float, date: str, variable: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    }
    try:
        if variable != "river_discharge":
            response = requests.get(
                f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={date}&end_date={date}&hourly={variable}",
                headers=headers,
                timeout=10
            )
        else:
            response = requests.get(
                f"https://flood-api.open-meteo.com/v1/flood?latitude={lat}&longitude={lon}&daily={variable}&start_date={date}&end_date={date}",
                headers=headers,
                timeout=10
            )
    except Exception as e:
        print("An unexpected error occurred")
        raise e
    else:
        data = response.json()
        if data.get("error", False):
            raise ConnectionError(data["reason"])
        # import code; code.interact(local=locals())
        formatted = {"elevation": data["elevation"]}
        interval = "hourly" if variable != "river_discharge" else "daily"
        for time, value in zip(data[interval]["time"], data[interval][variable]):
            formatted[time] = value
        formatted["unit"] = data[f"{interval}_units"][variable]
        return formatted


variables = [
    "temperature_2m",
    "surface_pressure",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
    "river_discharge",
    "soil_moisture_0_to_7cm"
]

cities = {
    "Valencia": (39.4739, -0.3797),
    "Bangkok": (13.754, 100.5014),
    "Mumbai": (19.0728, 72.8826),
    "New Orleans": (29.9547, -90.0751),
    "Houston": (29.7633, -95.3633)
}

fieldnames = [
    "date",
    "Temp_elevation",
    "Temp_unit",
    *[f"Temp_{n:02}:00" for n in range(24)],
    "Pressure_elevation",
    "Pressure_unit",
    *[f"Pressure_{n:02}:00" for n in range(24)],
    "Humid_elevation",
    "Humid_unit",
    *[f"Humid_{n:02}:00" for n in range(24)],
    "Rain_elevation",
    "Rain_unit",
    *[f"Rain_{n:02}:00" for n in range(24)],
    "Wind_elevation",
    "Wind_unit",
    *[f"Wind_{n:02}:00" for n in range(24)],
    "River_elevation",
    "River_unit",
    "Discharge",
    "Soil_elevation",
    "Soil_unit",
    *[f"Soil_{n:02}:00" for n in range(24)],
]

@dataclass
class Progress:
    city: str = "Bangkok"
    iteration: int = 0
    date: datetime = datetime(year=2000, month=1, day=1)

    def update(self, city: str, iteration: int, date: datetime):
        self.city = city
        self.iteration = iteration
        self.date = date

    def json(self):
        return {
            "city": self.city,
            "iteration": self.iteration,
            "date": self.date
        }

    @classmethod
    def from_json(cls, data: dict):
        return cls(data["city"], data["iteration"], data["date"])


def main():
    max_date = datetime(year=2025, month=11, day=6)
    if os.path.exists("progress_bangkok.pkl"):
        print("Loading from previous run")
        with open("progress_bangkok.pkl", "rb") as pf:
            progress = Progress.from_json(pickle.load(pf))
    else:
        print("Starting new run")
        progress = Progress()
    for city, loc in cities.items():
        if city != progress.city:
            continue
        date = progress.date
        t = tqdm(total=(max_date - date).days, desc=city)
        rows = []
        i = progress.iteration
        while date.isoformat().split("t")[0] != max_date.isoformat().split("t")[0]:
            progress.update(city, i, date)
            iso = date.isoformat().split("T")[0]
            row = {"date": iso}
            for var in variables:
                try:
                    data = get_data(loc[0], loc[1], iso, var)
                except ConnectionError as e:
                    print(str(e))
                    raise e
                except Exception as e:
                    print("Saving progress")
                    with open(f"{city}.csv", "a" if os.path.exists(f"{city}.csv") else "w") as f:
                        writer = csv.DictWriter(f, fieldnames, delimiter=",")
                        if not os.path.exists("progress_bangkok.pkl"):
                            writer.writeheader()
                        writer.writerows(rows)
                    with open("progress_bangkok.pkl", "wb") as pf:
                        pickle.dump(progress.json(), pf)
                    raise e
                match (var):
                    case "temperature_2m":
                        for k, v in data.items():
                            if k == "elevation":
                                row["Temp_elevation"] = v
                            elif k == "unit":
                                row["Temp_unit"] = v
                            else:
                                row["Temp_" + k.split("T")[1]] = v
                    case "surface_pressure":
                        for k, v in data.items():
                            if k == "elevation":
                                row["Pressure_elevation"] = v
                            elif k == "unit":
                                row["Pressure_unit"] = v
                            else:
                                row["Pressure_" + k.split("T")[1]] = v
                    case "relative_humidity_2m":
                        for k, v in data.items():
                            if k == "elevation":
                                row["Humid_elevation"] = v
                            elif k == "unit":
                                row["Humid_unit"] = v
                            else:
                                row["Humid_" + k.split("T")[1]] = v
                    case "precipitation":
                        for k, v in data.items():
                            if k == "elevation":
                                row["Rain_elevation"] = v
                            elif k == "unit":
                                row["Rain_unit"] = v
                            else:
                                row["Rain_" + k.split("T")[1]] = v
                    case "wind_speed_10m":
                        for k, v in data.items():
                            if k == "elevation":
                                row["Wind_elevation"] = v
                            elif k == "unit":
                                row["Wind_unit"] = v
                            else:
                                row["Wind_" + k.split("T")[1]] = v
                    case "river_discharge":
                        for k, v in data.items():
                            if k == "elevation":
                                row["River_elevation"] = v
                            elif k == "unit":
                                row["River_unit"] = v
                            else:
                                row["Discharge"] = v
                    case "soil_moisture_0_to_7cm":
                        for k, v in data.items():
                            if k == "elevation":
                                row["Soil_elevation"] = v
                            elif k == "unit":
                                row["Soil_unit"] = v
                            else:
                                row["Soil_" + k.split("T")[1]] = v
            rows.append(row)
            t.update()
            date = date + timedelta(days=1)
            if i % 10 == 0:
                time.sleep(5)
        with open(f"{city}.csv", "a" if os.path.exists(f"{city}.csv") else "w") as f:
            writer = csv.DictWriter(f, fieldnames, delimiter=",")
            if not os.path.exists("progress_bangkok.pkl"):
                writer.writeheader()
            writer.writerows(rows)
        break


if __name__ == "__main__":
    succeeded = False
    wait_time = 300
    fails = 0
    while not succeeded:
        try:
            main()
        except ConnectionError as e:
            fails += 1
            time.sleep(wait_time * fails)
            continue
        except Exception as e:
            print(f"Program crashed by error: {e}")
            fails = 0
            continue
        else:
            succeeded = True
