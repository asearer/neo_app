from flask import Flask, render_template
import requests
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# NASA API Key
NASA_API_KEY = 'zOpGoqJdp9tjkydekW65khLKjcx866FQyrV9BJKB'

# NEO API endpoint
NEO_API_URL = f'https://api.nasa.gov/neo/rest/v1/feed/today?api_key={NASA_API_KEY}'

# Function to fetch NEO data
def fetch_neo_data():
    response = requests.get(NEO_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return None

# Function to parse data and generate graph
def generate_distance_graph(data):
    distances = []
    names = []
    for date in data['near_earth_objects']:
        for neo in data['near_earth_objects'][date]:
            distances.append(float(neo['close_approach_data'][0]['miss_distance']['kilometers']))
            names.append(neo['name'])
    
    plt.figure(figsize=(10, 6))
    plt.barh(names, distances, color='skyblue')
    plt.xlabel('Distance from Earth (km)')
    plt.ylabel('Near Earth Object')
    plt.title('Distance of Near Earth Objects from Earth')
    plt.gca().invert_yaxis()  # Invert y-axis to display the closest objects on top
    plt.tight_layout()

    # Convert plot to image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return img_str

# Route to display graph
@app.route('/')
def show_graph():
    neo_data = fetch_neo_data()
    if neo_data:
        img_str = generate_distance_graph(neo_data)
        return render_template('graph.html', img_str=img_str)
    else:
        return "Failed to fetch NEO data"

if __name__ == "__main__":
    app.run(debug=True)
