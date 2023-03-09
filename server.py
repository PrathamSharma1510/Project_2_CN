import socket
def start_server(port, BUFFER_SIZE):
    # connecting the server
    print("--------- Server is starting please wait ---------")
    # socket connect
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", port)) 
    # listening the server 
    server.listen()
    print("Server started. Listening on port : ", port)
    print("Waiting for the client to get connect.")

    # connected server
    # going into the loop
    while True:
        try:
            conn, add = server.accept()
            print("--------- New client connected at :", add, "---------")
            data =conn.recv(1024)
            # data fetched
            command =data.decode("utf-8")
            print("Recieved command "+ command)
            # splited into two parts command + filename
            data_split = command.split()
            # upload function
            if data_split[0] == 'upload':
                # open the file 
                file = open('new' +data_split[1],'wb')
                file_chunks = conn.recv(1024)
                # write the file which we recieves from the client
                while file_chunks:
                    file.write(file_chunks)
                    file_chunks = conn.recv(1024)
                file.close()
                # file is closed and thats why file is not corrupt 
                print('File Received! and new name of file is: new' +data_split[1])
            # get function
            elif data_split[0] == 'get':
                # file is openend
                file = open(data_split[1], 'rb')
                file_chunks =file.read (1024)
                # chunks are send in the set of 1024
                while(file_chunks):
                    conn.send(file_chunks)
                    file_chunks = file.read(1024)
                file.close()
                print("File Sent!")
                # file is closed and thats why file is not corrupt 

                # invalid function
            elif data_split[0]=='exit':
                print('Connection Close')
                conn.close()
                break
            else :
                print('Invalid Command')
                conn.closed()
                break 
                # connection is closed 
            conn.close()
        except:
            # handel any error
            print("Something went wrong ")
            conn.close()
        else:
            continue

if __name__ == "__main__":
    # added a port to connect in the main server
    port = 5108
    start_server(port, 1024)
