from SPARQLWrapper import SPARQLWrapper, JSON

class Anzo:
    def __init__(self):
        # Endpointurl is AnzoGraph server port
        self.endpoint_url = "http://localhost:80/sparql"

        self.username = "admin"
        self.password = "Passw0rd1"

        self.anzograph = SPARQLWrapper(self.endpoint_url)
        self.anzograph.setCredentials(self.username, self.password)
        self.connection = self.connect()

    def connect(self):
        try:
            self.anzograph.setQuery("SELECT * WHERE { ?s ?p ?o } LIMIT 1")  # Attempt to connect by fetching the AnzoGraph service description
            self.anzograph.setReturnFormat(JSON)
            results = self.anzograph.query().convert()

            if results and "results" in results:
                print("Connected to AnzoGraph successfully!")
                return True
            else:
                print("Failed to connect to AnzoGraph. Check the server URL and credentials.")
                return False
        except Exception as e:
            print(f"An error occurred: {e}")