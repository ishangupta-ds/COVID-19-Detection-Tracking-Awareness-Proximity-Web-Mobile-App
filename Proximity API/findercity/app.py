from city import get_idx_distance_from_query_locations, extrathings
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/trackercity', methods=['GET'])
def get_nearestcity_case():

    if 'longitude' in request.args:
        Longitude = request.args['longitude']
    if 'latitude' in request.args:
        Latitude = request.args['latitude']

    if Latitude is not None and Longitude is not None and len(Latitude) > 0 and len(Longitude) > 0:
        corona_citydb_with_latlng = extrathings()
        (mindist, cases, city, state, lats, lngs) = get_idx_distance_from_query_locations(float(Latitude), float(Longitude), corona_citydb_with_latlng)
        print("The nearest location with COVID-19 from your Location is within {} km with {} number of positive cases the nearest one at Latitude: {} and Longiude: {}".format(mindist, cases, lats, lngs))
        print("Location(City:LAT_AND_LON): {} , {}".format(city.upper(), state.upper()))

    nearbyCase = False
    if mindist <= 2:
            nearbyCase = True
    response = jsonify({
        'present_in_locality': nearbyCase,
        'minDist': str(mindist),
        'cases': str(cases),
        'city': city,
        'state': state,
        'lat': str(lats),
        'lng': str(lngs),
    })
    response.status_code = 200
    return response


if __name__ == "__main__":
    app.run(debug=True)

