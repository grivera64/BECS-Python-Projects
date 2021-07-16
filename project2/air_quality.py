from geopy.geocoders import Nominatim
import requests

# Create Token constant for waqi
TOKEN: str

# Format the pollutant from key to normal spelling
def format_pol(data: str):

    return data.upper().replace('0', '.0').replace('5', '.5')

# Main Function
def main():

    # Read token from token.txt (used to avoid sharing private token; could be done more securely [TODO!])
    with open("token.txt") as fp:

        TOKEN = fp.read().replace("\n", "")

    # Create a geopy object for finding a location's air data via zip code
    geo_locator = Nominatim(user_agent="PyAirQuality")

    # Start of program
    print("Welcome to PyAirQuality.")

    # Infinite loop until a correct zip code is provided
    while True:
        
        try:

            zip_code = int(input("Please enter a zip code: "))

            if len(str(zip_code)) != 5:

                raise ValueError

            break
        
        except ValueError:
            
            print("\nInvalid zip code\n")

    # Find the location using geopy 
    location = geo_locator.geocode(zip_code)

    longitude = location.longitude
    latitude = location.latitude

    # Make HTTP request to waqi api for the air information from the certain zip code area
    # and view the JSON there
    result = requests.get(f"https://api.waqi.info/feed/geo:{latitude};{longitude}/?token={TOKEN}").json()

    # Check to see if there was an error in the request
    if (result["status"] != "ok"):

        print("ERROR: Please try again later...")
        return

    # Print data from json file
    print("Current Air Quality Index:", result['data']['aqi'])

    dominant: str = ""
    print(f"\nCurrent {format_pol((dominant := result['data']['dominentpol']))} value: {result['data']['iaqi'][dominant]['v']}\n")

    print("Station Location:", result['data']['city']['name'])

    # Print the forcasts for the next few days
    print("\nForecast:")

    for forecast in result['data']['forecast']['daily'][dominant]:

        print("\n", forecast['day'], sep='')
        print(f"Average {format_pol(dominant)} value: {forecast['avg']}")

    pass

# Start of the program
if __name__ == "__main__":

    main()
