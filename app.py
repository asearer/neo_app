from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# NASA API endpoint
NASA_API_URL = "https://api.nasa.gov/neo/rest/v1/feed"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the date submitted by the user
        date = request.form.get("date")
        
        # Make a request to the NASA NEO API
        response = requests.get(NASA_API_URL, params={"start_date": date, "end_date": date, "api_key": "DEMO_KEY"})
        
        if response.status_code == 200:
            data = response.json()
            neo_info = extract_neo_info(data)
            return render_template("index.html", neo_info=neo_info)
        else:
            error_message = f"Error fetching data: {response.status_code}"
            return render_template("index.html", error=error_message)
    
    return render_template("index.html")


def extract_neo_info(data):
    neo_info = []
    near_earth_objects = data.get("near_earth_objects", {})
    
    # Iterate over each date in near_earth_objects
    for date in near_earth_objects:
        neo_date_info = {}
        neo_date_info["date"] = date
        
        # Extract NEO information for the date
        neo_list = []
        for neo in near_earth_objects[date]:
            neo_details = {}
            neo_details["name"] = neo["name"]
            neo_details["diameter"] = neo["estimated_diameter"]["kilometers"]["estimated_diameter_max"]
            neo_details["close_approach_date"] = neo["close_approach_data"][0]["close_approach_date"]
            neo_details["miss_distance"] = neo["close_approach_data"][0]["miss_distance"]["kilometers"]
            neo_list.append(neo_details)
        
        neo_date_info["neo_list"] = neo_list
        neo_info.append(neo_date_info)
    
    return neo_info


if __name__ == "__main__":
    app.run(debug=True)
