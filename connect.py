from ConnectSmartAPI import ConnectSmartAPI

#example
smart_api_client = ConnectSmartAPI()

if __name__ == "__main__":
    smart_api_client.connect_session()
    smart_api_client.terminate_session()
