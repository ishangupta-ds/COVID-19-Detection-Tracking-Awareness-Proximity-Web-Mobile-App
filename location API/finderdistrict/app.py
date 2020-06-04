from district import get_idx_distance_from_query_locations, extrathings, fewmoreextrathings, get_distance_between_lats_lons
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/trackerdistrict', methods=['GET'])
def get_nearest_case():

    Latitude=None
    Longitude=None

    if 'longitude' in request.args:
        Longitude = request.args['longitude']
    if 'latitude' in request.args:
        Latitude = request.args['latitude']
    if 'pincode' in request.args:
        pin_code = request.args['pincode']
    
    if Latitude is not None and Longitude is not None and len(Latitude) > 0 and len(Longitude) > 0:
        corona_db_with_latlng = extrathings()
        (mindist, cases, district, state, lats, lngs) = get_idx_distance_from_query_locations(float(Latitude), float(Longitude), corona_db_with_latlng)
        print("The nearest location with COVID-19 from your Location is within {} km with {} number of positive cases the nearest one at Latitude: {} and Longiude: {}".format(mindist, cases, lats, lngs))
        print("Location(District:LAT_AND_LON): {} , {}".format(district.upper(), state.upper()))

    elif pin_code is not None:

        pin_code = int(pin_code)

        (corona_db_with_latlng, city_wise_coordinates) = fewmoreextrathings()

        if pin_code in city_wise_coordinates.PIN.values:
            
            query_info = city_wise_coordinates[city_wise_coordinates.PIN == int(pin_code)]

            if query_info.PIN.iloc[1] in corona_db_with_latlng['PIN'].values:

                mindist = 2
                lats = corona_db_with_latlng.loc[corona_db_with_latlng.PIN == query_info.PIN.iloc[1], 'Lat']
                lngs = corona_db_with_latlng.loc[corona_db_with_latlng.PIN == query_info.PIN.iloc[1], 'Lng']
                mindist = int(get_distance_between_lats_lons(query_info.Lat.iloc[1], query_info.Lng.iloc[1], lats, lngs))
                cases = corona_db_with_latlng.loc[corona_db_with_latlng.PIN == query_info.PIN.iloc[1], 'Num_Positive_cases']
                district = corona_db_with_latlng.loc[corona_db_with_latlng.PIN == query_info.PIN.iloc[1], 'District']
                state = corona_db_with_latlng.loc[corona_db_with_latlng.PIN == query_info.PIN.iloc[1], 'State']
                print("The nearest location with COVID-19 from your PIN is in your own Postal Location with {} number of positive cases".format(cases.values[0]))
                print("Location(District:PIN): {} , {}".format(district.values[0].upper(), state.values[0].upper()))
            else:
                (mindist, cases, district, state, lats, lngs) = get_idx_distance_from_query_locations(query_info.Lat.iloc[1], query_info.Lng.iloc[1], corona_db_with_latlng)
                print("The nearest location with COVID-19 from your Location is within {} km with {} number of positive cases and the nearest one at Latitude: {} and Longiude: {}".format(mindist, cases, lats, lngs))
                print("Location(District:PIN): {} , {}".format(district.upper(), state.upper()))
        else:
            print('You entered an Invalid PIN')

        

    nearbyCase = False
    if mindist <= 2:
            nearbyCase = True
    response = jsonify({
        'present_in_locality': nearbyCase,
        'minDist': str(mindist),
        'cases': str(cases),
        'district': district,
        'state': state,
        'lat': str(lats),
        'lng': str(lngs),
    })
    response.status_code = 200
    return response



if __name__ == "__main__":
    app.run(debug=True)

