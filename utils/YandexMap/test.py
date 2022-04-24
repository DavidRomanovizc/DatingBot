from loader import client


x, y = client.coordinates("Москва Льва Толстого 16")
coordinates = client.address(f"{x}", f"{y}")
coordinates = coordinates.split(",")
coordinates = ",".join(coordinates)
print(x, y)