# clueless-project

## Setup instructions
Create virtual environment
```commandline
sudo apt-get install virtualenv
cd ~/Documents
virtualenv -p python3 clueless-env/
```
Install gRPC in the virtual environment
```commandline
source ~/Documents/clueless-env/bin/activate
python -m pip install --upgrade pip
python -m pip install grpcio
python -m pip install grpcio-tools
```

Generate gRPC output
```commandline
# change directory
cd proto

python -m grpc_tools.protoc --proto_path=. ./clueless.proto --python_out=. --grpc_python_out=.
```
Start the server
```commandline
export PYTHONPATH=$PYTHONPATH:/home/clueless-dev/Documents/clueless-project
python3 server_impl.py
```

## Development
To implement an API call you can follow the steps below:

1. Define the client request (Greetings) and the according server response (GreetingsResponse) in `proto/clueless.proto` and regenerate the gRPC output
```
message Greetings{
  string client_name = 1;
}

message GreetingsResponse {
  string message = 1;
  string status = 2;
}
```
```commandline
cd proto

python -m grpc_tools.protoc --proto_path=. ./clueless.proto --python_out=. --grpc_python_out=.
```
2. Define the service in `source/server_impl.py`
```
def ServerGreetings(self, request, context):
    client_name = request.client_name
    message = f'Hi "{client_name}". Welcome to Clueless!'
    response = {'message': message, 'status': "connected"}
    return pb2.GreetingsResponse(**response)
```
3. Define the according API call in `source/client_impl.py`
