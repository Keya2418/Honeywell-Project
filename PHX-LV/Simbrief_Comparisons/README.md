# File naming conventions and other information

"SB_PHX_LAS_022624_2328.pdf" means:
- SB = it was generated in simbrief. An absence of "SB" indicates flightaware data.
- PHX_LAS = it's a flight from phx to las
- 022624 = february 26th 2024. This is the date of the take off. 
- 2328 = 23:28 UTC/Zulu Time. This is the take off time. 

The latitude, longitude, and altitude are gathered from the flight log page on the SB-generated flight plan from the LAT LONG and FL (flight level) metrics. FL is measured in 100s of feet (so 280 FL indicates 28000 feet, 034 indicates 3400 feet).

MAKE SURE you divide the latitude and longitude by 100. Also, W/S are negative, N/E are positive coordinates.

# Results of 02/26/2024 23:28 UTC PHX>LAS Comparison (Green is Simbrief, Red is FlightAware):
![Comparing February 26th flights](PHX-LV/Simbrief_Comparisons/CompResult_PHX_LAS_022624_2328.PNG)
