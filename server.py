from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import popGen as p
import json

# Example URL
# http://localhost:8080/popgen?10_000&0.5

# Config

configFileRaw = open("PopGen/config.json")
configFile = json.load(configFileRaw)

hostName = configFile["hostName"]
serverPort = configFile["port"]

#Logging

path = configFile["logPath"]
logging.basicConfig(filename=path,
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    encoding="utf-8",
    level=logging.DEBUG)

#Server

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info(self.path)
        logging.info(self.client_address)
        logging.info(self.request_version)
        path = self.path
        if "?" in path:
            tokens = path.split("?")
            if len(tokens) == 2:
                logging.info("Token 1: " + str(tokens[0]))
                logging.info("Token 2: " + str(tokens[1]))
            if tokens[0] == "/popgen":
                try:
                    args = tokens[1].split("&")
                    N = int(args[0])
                    MALE_PROPORTION = float(args[1])
                    logging.info("N: " +  str(N) + "\nMALE_PROPORTION:" + str(MALE_PROPORTION))
                except Exception as e:
                    print("An exception occured.")
                    logging.info(e)

        if self.path.startswith('/popgen'):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-type", "application/json")
            self.end_headers()
            try:
                model = p.PopGen(N, MALE_PROPORTION)
                jsonRaw = model.run_simulation()
                print(jsonRaw)
                print("Simulation completed succesfully.")
                logging.info("Simulation completed succesfully.")

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(jsonRaw, "utf-8"))
                
                #self.wfile.write(bytes("Simulation Results:", "utf-8"))
                #self.wfile.write(bytes("\n\nTotal population at the bottom of the tree: %s" %pop, "utf-8"))
                #self.wfile.write(bytes("\nNumber of generations until A/E couple emerged: %s" %num_gens, "utf-8"))
                #self.wfile.write(bytes("\nNumber of ancestral couples still in gene pool at simulation end: %s" %int(num_anc_rep/2), "utf-8"))
                #self.wfile.write(bytes("\nNumber of A/E couples at simulation end: %s" %int(num_ae_couples), "utf-8"))
                #self.wfile.write(bytes("\nNumber of ancestral couples who are ancestors of 90 + percent of final generation: %s" %almost_ae, "utf-8"))

            except Exception as e:
                print("An exception occured.")
                logging.info(e)
                self.wfile.write(bytes("An exception occured.", "utf-8"))
            
        elif self.path.endswith('/'):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes("Population Geneology homepage.", "utf-8"))
        else:
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes("404 Page Not Found", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("PopGen server started http://%s:%s" % (hostName, serverPort))
    logging.info("PopGen server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")