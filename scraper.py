import csv

rows = []

with open("main.csv", "r") as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        rows.append(row)

headers = rows[0]
planet_data_rows = rows[1:]

print(headers)
print(planet_data_rows[0])

#Find the solar system with the most number of planets!

headers[0] = "rows_num"

solar_system_planet_count = {}

for planet_data in planet_data_rows:
    if solar_system_planet_count.get(planet_data[11]):
        solar_system_planet_count[planet_data[11]]+= 1
    else:
        solar_system_planet_count[planet_data[11]] = 1
        
max_solar_system = max(solar_system_planet_count, key = solar_system_planet_count.get) 
print("solar_system {} has maximum planets {} out of all the solar systems we have discovered so far!" . format(max_solar_system, solar_system_planet_count[max_solar_system]))

#Our Next Planet Home

hd_10180_planets = []
for planet_data in planet_data_rows:
    if max_solar_system == planet_data[11]:
        hd_10180_planets.append(planet_data)

print(len(hd_10180_planets))
print(hd_10180_planets)


temp_planet_data_rows = list(planet_data_rows)
for planet_data in temp_planet_data_rows:
 planet_mass = planet_data[3]
 if planet_mass.lower() == "unknown":
   planet_data_rows.remove(planet_data)
   continue
 else:
   planet_mass_value = planet_mass.split(" ")[0]
   planet_mass_ref = planet_mass.split(" ")[1]
   if planet_mass_ref == "Jupiters":
     planet_mass_value = float(planet_mass_value) * 317.8
   planet_data[3] = planet_mass_value


 planet_radius = planet_data[7]
 if planet_radius.lower() == "unknown":
   planet_data_rows.remove(planet_data)
   continue
 else:
   planet_radius_value = planet_radius.split(" ")[0]
   planet_radius_ref = planet_radius.split(" ")[2]
   if planet_radius_ref == "Jupiter":
     planet_radius_value = float(planet_radius_value) * 11.2
   planet_data[7] = planet_radius_value
   
print(len(planet_data_rows))

import plotly.express as px
hd_10180_planets_masses = []
hd_10180_planets_names = []

for planet_data in hd_10180_planets:
    hd_10180_planets_masses.append(planet_data[3])
    hd_10180_planets_names.append(planet_data[1])

hd_10180_planets_masses.append(1)
hd_10180_planets_names.append("Earth")

fig = px.bar(x = hd_10180_planets_names, y = hd_10180_planets_masses)
fig.show()

planet_masses = []
planet_radii = []
planet_names = []
for planet_data in planet_data_rows:
    planet_masses.append(planet_data[3])
    planet_radii.append(planet_data[7])
    planet_names.append(planet_data[1])

planet_gravity = []
for index, name in enumerate(planet_names):
    gravity = (float(planet_masses[index])*5.972e+24) / (float(planet_radii[index])*float(planet_radii[index])*6371000*6371000) * 6.674e-11
    planet_gravity.append(gravity)

fig = px.scatter(x = planet_radii, y= planet_masses, size = planet_gravity, hover_data = [planet_names])
fig.show()

#From this point on, it is class 132


#Habitable Gravity Planets

low_gravity_planets = []
for index, gravity in enumerate(planet_gravity):
  if gravity < 100:
    low_gravity_planets.append(planet_data_rows[index])
print(len(low_gravity_planets))
print(headers)

#Types of planets
planet_type_values = []
for planet_data in planet_data_rows:
  planet_type_values.append(planet_data[6])
print(list(set(planet_type_values)))

#relation between type and mass of the planet
planet_masses = []
planet_radii = []


for planet_data in low_gravity_planets:
  planet_masses.append(planet_data[3])
  planet_radii.append(planet_data[7])

fig = px.scatter(x = planet_radii, y = planet_masses)
fig.show()

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns


X = []
for index, planet_mass in enumerate(planet_masses):
 temp_list = [
                 planet_radii[index],
                 planet_mass
             ]
 X.append(temp_list)


wcss = []
for i in range(1, 11):
   kmeans = KMeans(n_clusters=i, init='k-means++', random_state = 42)
   kmeans.fit(X)
   # inertia method returns wcss for that model
   wcss.append(kmeans.inertia_)


plt.figure(figsize=(10,5))
sns.lineplot(x=range(1, 11), y=wcss, marker='o', color='red')
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

#class 133 from this point onwards

planet_types=[]
for planet_data in low_gravity_planets:
  planet_types.append(planet_data[6])
fig = px.scatter(x = planet_radii, y = planet_masses, color = planet_types)
fig.show()

suitable_planets = []

for planet_data in low_gravity_planets:
  if planet_data[6].lower() == "terrestrial" or planet_data[6].lower() == "super earth":
    suitable_planets.append(planet_data)

print(len(suitable_planets))
print(headers)

temp_suitable_planets = list(suitable_planets)
for planet_data in temp_suitable_planets:
  if planet_data[8].lower() == "unknown":
    suitable_planets.remove(planet_data)

for planet_data in suitable_planets:
  if planet_data[9].split(" ")[1].lower() == "days":
    planet_data[9] = float(planet_data[9].split(" ")[0]) #Days
  else:
    planet_data[9] = float(planet_data[9].split(" ")[0])*365 #Years
  planet_data[8] = float(planet_data[8].split(" ")[0])

orbital_radii = []
orbital_periods = []
for planet_data in suitable_planets:
  orbital_radii.append(planet_data[8])
  orbital_periods.append(planet_data[9])

fig = px.scatter(x=orbital_radii, y=orbital_periods)
fig.show()


goldilock_planets = list(suitable_planets)          #We will leave suitable planet list as it is

temp_goldilock_planets = list(suitable_planets) 
for planet_data in temp_goldilock_planets:
  if planet_data[8] < 0.38 or planet_data[8] > 2:
    goldilock_planets.remove(planet_data)

print(len(suitable_planets))
print(len(goldilock_planets))

#speed of planets
planet_speeds = []
for planet_data in suitable_planets:
 distance = 2 * 3.14 * (planet_data[8] * 1.496e+9)
 time = planet_data[9] * 86400
 speed = distance / time
 planet_speeds.append(speed)


speed_supporting_planets = list(suitable_planets) #We will leave suitable planet list as it is


temp_speed_supporting_planets = list(suitable_planets)
for index, planet_data in enumerate(temp_speed_supporting_planets):
 if planet_speeds[index] > 200:
   speed_supporting_planets.remove(planet_data)


print(len(speed_supporting_planets))

 
habitable_planets = []
for planet in speed_supporting_planets:
  if planet in goldilock_planets:
    habitable_planets.append(planet)

print(len(habitable_planets))

final_dict = {}

for index, planet_data in enumerate(planet_data_rows):
  features_list = []
  gravity = (float(planet_data[3])*5.972e+24) / (float(planet_data[7])*float(planet_data[7])*6371000*6371000) * 6.674e-11
  try:
    if gravity < 100:
      features_list.append("gravity")
  except: pass
  try:
    if planet_data[6].lower() == "terrestrial" or planet_data[6].lower() == "super earth":
      features_list.append("planet_type")
  except: pass
  try:
    if planet_data[8] > 0.38 or planet_data[8] < 2:
      features_list.append("goldilock")
  except: pass
  try:
    distance = 2 * 3.14 * (planet_data[8] * 1.496e+8)
    time = planet_data[9] * 86400
    speed = distance / time
    if speed < 200:
      features_list.append("speed")
  except: pass
  final_dict[index] = features_list

print(final_dict)


goldilock_gravity_type_count = 0
for key, value in final_dict.items():
  if " goldlock" in value and "planet_type" in value and "gravity" in value:
    goldilock_gravity_type_count += 1

print(goldilock_gravity_type_count)

speed_goldilock_gravity_type_count = 0
for key, value in final_dict.items():
  if "goldilock" in value and "planet_type" in value and "gravity" in value and "speed" in value:
    speed_goldilock_gravity_type_count += 1
    
print(speed_goldilock_gravity_type_count)

final_dict = {}

for index, planet_data in enumerate(planet_data_rows):
  features_list = []
  gravity = (float(planet_data[3])*5.972e+24) / (float(planet_data[7])*float(planet_data[7])*6371000*6371000) * 6.674e-11
  try:
    if gravity < 100:
      features_list.append("gravity")
  except: pass
  try:
    if planet_data[6].lower() == "terrestrial" or planet_data[6].lower() == "super earth":
      features_list.append("planet_type")
  except: pass
  
  if float(planet_data[8].split(" ")[0]) > 0.38 and float(planet_data[8].split(" ")[0]) < 2:
    features_list.append("goldilock")
  
  try:
    distance = 2 * 3.14 * (float(planet_data[8].split(" ")[0]) * 1.496e+9)
    time, unit = planet_data[9].split(" ")[0], planet_data[9].split(" ")[1]
    if unit.lower() == "days":
      time = float(time)
    else:
      time = float(time) * 365
    time = time * 86400
    speed = distance / time
    if speed < 200:
      features_list.append("speed")
  except: pass
  final_dict[index] = features_list

print(final_dict)



final_dict = {}
headers.append("gravity")
headers.append("orbital_speed")
for index, planet_data in enumerate(planet_data_rows):
  features_list = []
  gravity = (float(planet_data[3])*5.972e+24) / (float(planet_data[7])*float(planet_data[7])*6371000*6371000) * 6.674e-11
  try:
    if gravity < 100:
      features_list.append("gravity")
      planet_data.append('gravity')
  except:   planet_data.append('unknown')
  try:
    if planet_data[6].lower() == "terrestrial" or planet_data[6].lower() == "super earth":
      features_list.append("planet_type")
  except: pass
  try:
    if float(planet_data[8].split(" ")[0]) > 0.38 and float(planet_data[8].split(" ")[0]) < 2:
      features_list.append("goldilock")
  except: 
    try:
      if planet_data[8] > 0.38 and planet_data[8] < 2:
        features_list.append("goldilock")
    except: pass
  try:
    distance = 2 * 3.14 * (planet_data[8] * 1.496e+8)
    time = planet_data[9] * 86400
    speed = distance / time
    if speed < 200:
      features_list.append("speed")
    planet_data.append('speed')
  except: planet_data.append('unknown')
  final_dict[planet_data[1]] = features_list

print(final_dict)

goldilock_planet_count = 0
for key, value in final_dict.items():
  if "goldilock" in value:
    goldilock_planet_count += 1

print(goldilock_planet_count)


goldilock_gravity_type_count = 0
for key, value in final_dict.items():
  if "goldilock" in value and "planet_type" in value and "gravity" in value:
    goldilock_gravity_type_count += 1

print(goldilock_gravity_type_count)

speed_planet_count = 0
for key, value in final_dict.items():
  if "speed" in value:
    speed_planet_count += 1

print(speed_planet_count)


print(headers)
print(planet_data_rows[6])
    