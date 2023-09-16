import socket
import utm
import math

def calculate_current_speed(coord1, coord2, distances):
    easting1, northing1 = coord1
    easting2, northing2 = coord2
    distance = math.sqrt((easting2 - easting1)**2 + (northing2 - northing1)**2)
    distances.append(distance)
    return distance, distances

def calculate_overall_speed(distances, time_passed):
    return sum(distances) / time_passed

def main():
	#Conncet to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    time_passed = 0
    distances = []
    prev_coord = None

    try:
        while True:
            # Receive data from the server
            coord_data = client_socket.recv(1024).decode()
            
            # Break if there's no more data
            if not coord_data:
                break
            
            # Parse coordinates and convert to UTM
            lat, lon = map(float, coord_data.split(','))
            e, n, _, _ = utm.from_latlon(lat, lon)
            current_coord = (e, n)

            # Calculate current speed if a previous coordinate exists
            if prev_coord:
                current_speed, distances = calculate_current_speed(prev_coord, current_coord, distances)
                print(f"Current Speed: {current_speed}m/s")
            
            prev_coord = current_coord
            time_passed += 1

        overall_speed = calculate_overall_speed(distances, time_passed)
        print(f"Overall Speed: {overall_speed}m/s")

    except KeyboardInterrupt:
        print('Connection closed.')

    finally:
        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    main()
