import socket
import time

def initialize_server(port):
    #Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))

    #listen for client connection
    server_socket.listen(5)
    client_socket, address = server_socket.accept()
    return server_socket, client_socket 

def read_coordinates_from_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        #strip tabs, store in coordinates
        coordinates = [tuple(map(float, line.strip().split("\t"))) for line in lines]
    return coordinates

def main():
    server_socket, client_socket = initialize_server(12345)
    coordinates = read_coordinates_from_file("missionwaypoints.txt")
    
    # Send coordinates to client
    for coord in coordinates:
        coord_str = f"{coord[0]},{coord[1]}"
        client_socket.send(coord_str.encode())
        time.sleep(1)

    # Close the sockets
    client_socket.close() 
    server_socket.close()

if __name__ == "__main__":
    main()
