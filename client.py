import socket
def main(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to localhost
    server_socket.connect(('localhost', port))
    flag = False
    # go inside a inf loop.
    while True:
        if(flag):
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect(('localhost', port))
            flag = False
        print("Enter command ('exit') to stop server and client")
        command = input("Enter command (get/upload filename): ")
        command_parts = command.split()
        # get function
        if command_parts[0] == "get":
            # exception handel
            try :
                # open file
                file = open(command_parts[1], 'rb')
            except :
                # reconnect the server
                print("File was not found please check the name")
                flag = True
            else:
                # sending file
                server_socket.send(command.encode('utf-8'))
                file = open(f"new{command_parts[1]}", 'wb')
                # send the file in chunks
                file_chunks = server_socket.recv(1024)
                while file_chunks:
                    # write files
                    file.write(file_chunks)
                    file_chunks = server_socket.recv(1024)
                file.close()
                # file is closed and thats why file is not corrupt 
                print('File Received! and new name of file is: new' +command_parts[1])
                flag = True
        # upload function
        elif command_parts[0] == "upload":
            # exception handel
            try:
                file = open(command_parts[1], 'rb')
            except:
                print("File was not found please check the name")
                flag = True
            else:
                server_socket.send(command.encode('utf-8'))
                file_chunks = file.read(1024)
                server_socket.send(file_chunks)
                while(file_chunks):
                    file_chunks = file.read(1024)
                    server_socket.send(file_chunks)
                file.close()
                 # file is closed and thats why file is not corrupt 
                print("File Sent!")
                flag = True

        # exit  for the connection to disconnect
        elif command == "exit":
            server_socket.send(command.encode('utf-8'))
            print("The connection is Ended")
            server_socket.close()
            break
        else:
            # invalid command
            print("Invalid command Enter a valid command")
            server_socket.close()
            # reconnect the server until lost
            flag = True
            # break
        server_socket.close()


if __name__ == "__main__":
    try:
        start = input("Enter the command and port number :")
        start = start.split()
        if(start[0] == 'ftpclient'):
            port = int(start[1])
            main(port)
        else:
            print("Command is not proper")
    except:
        print("No Server connected on that Port")
