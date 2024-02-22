# Ideas Concerning Flight Path Improvements:

## Path-finding based on weather, fuel usage, plane model, and historical flight paths

- Weather:
  There is a free API called CheckWXAPI that can help us with weather. METAR is a format for reporting current weather information. Here is the link: [Metar Documentation](https://www.checkwxapi.com/documentation/metar)

  Using the METAR API, we can decode METAR codes. Here is an example METAR code, as found on the [METAR Wikipedia page](https://en.wikipedia.org/wiki/METAR):
  ``` METAR LBBG 041600Z 12012MPS 090V150 1400 R04/P1500N R22/P1500U +SN BKN022 OVC050 M04/M07 Q1020 NOSIG 8849//91= ```
  Each section of the METAR code indicates something about some weather occurring at some location. According to the aforementioned Wikipedia page, the code means that at Burgas Airport (an airport in Bulgaria) on February 4th 2005 at 16:00 UTC, there was a 12 m/s windspeed from 120 degrees and there was snow falling at a heavy rate.

  With this information, we can determine what aspects of weather we would like to consider "too dangerous" to travel through. We can reroute the flight based on whether there is snow, heavy wind, precipitation, or thunderstorms.

- Fuel usage and plane model:
  Based on the aircraft model, we can find out the fuel efficiency data and use that to our advantage so that we can make our improvements using what we already know about the aircraft. 

- Historical flight paths:
  Phoenix and Las Vegas are known for having very few cloudy days and are some of the sunniest places in our country. The flight path from Phoenix to Las Vegas is a good starting point in terms of considering weather and creating the initial flight plans. It is a comparatively short flight and there is tons of data to draw from.

  We can use FlightAware's longitude, latitude, altitude, course, and speed data to get an idea of the most commonly flown flight paths for the flight from KPHX to KLAS. We can discover whether there are certain "set" paths that pilots typically follow for this type of flight using machine learning, and from there use these paths as baselines from which to deviate in the event of poor weather conditions. We can also find out which of the paths are the best for fuel consumption depending on wind directions (whether they would aid or hinder the flight) and other metrics like distance added. 


# Regulations and Administrative Things:

## ICAO (International Civil Aviation Organization) Naming Convention 
They use four-letter airport codes for weather stations and airports around the country. Some examples are KPHX (Phoenix Sky Harbor Airport), KLAS (Harry Reid International Airport), and KLAX (Los Angeles International Airport).

## IATA (International Air Transport Association) Naming Convention
They use three-letter airport codes for airports and metropolitan areas around the world. Some examples are PHX, LAX, JFK, etc.

## Flight Tracks 
There is a system called the "North Atlantic Tracks" (NATs). It updates every day on this website:
[Update Website](https://notams.aim.faa.gov/nat.html)

[Flight Plan Database: Read More About NATs](https://flightplandatabase.com/nav/NATS)

