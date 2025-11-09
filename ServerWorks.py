import requests
import json

class ServerManager():
    def __init__(self, BASE_IP="https://carbordgumler.pythonanywhere.com/"):
        self.BASE_IP = BASE_IP

    def login(self,email:str,password:str) -> str:
        try:
            MainRequest = requests.get(self.BASE_IP + f"/login/{email}/{password}")
            print(MainRequest)
            return MainRequest.text
        except:
            return "False"
    
    def sign_up(self,email:str,password:str,username:str) -> str:
        try:
            return requests.get(self.BASE_IP + f"/sign_up/{email}/{password}/{username}").text
        except:
            return "False"
        
    def load_own_trail(self,trail_name,email,distance,date,start_lat,start_lon,description,password,file):
        try:
            main_req = requests.post(url=str(self.BASE_IP + f"/add_trail/{trail_name}/{distance}/{date}/{start_lat}/{start_lon}/{description}/{email}/{password}"),files={"file" : file}).text
            return main_req
        except:
            return "None"
    
    def get_all_trails(self,sort_type,location,page):
        try:
            MainRequest = requests.get(self.BASE_IP + f"/get_all_trails/{sort_type}/{location}/{page}").json()
        except:
            MainRequest = {"data" : []}
        return MainRequest["data"]

    def load_public_trail(self,trail_id,password,email,file):
        try:
            MainRequest = requests.post(url=str(self.BASE_IP + f"/load_rerun/<{trail_id}>/<{password}>/<{email}>"),files={"file":file})
        except:
            pass
        
    def get_leaderboard(self,trail_id,page):
        try:
            MainRequest = requests.get(self.BASE_IP + f"/get_leaderboard/{trail_id}/{page}").json()
        except:
            MainRequest = {"data" : []}
        return MainRequest["data"]
    
    def get_trail(self,trail_name):
        try:
            MainRequest = requests.get(self.BASE_IP + f"/get_trail/{trail_name}").json()
        except:
            MainRequest = {"data" : []}
        return MainRequest
    
    def get_trail_file(self,trail_id):
        try:
            MainRequest = requests.get(self.BASE_IP + f"/get_trail_file/{trail_id}").json()
        except:
            MainRequest = {"data" : []}
    def get_user_runtimes(self,username):
        try:
            MainRequest = requests.get(self.BASE_IP + f"/get_profile/{username}").json()
        except:
            MainRequest = {"data" : []}
        return MainRequest
    def get_trail_key_word(self,word,page):
        try:
            MainRequest = requests.get(self.BASE_IP + f"/search_key_word/{word}/{page}").json()
        except:
            MainRequest = {"data" : []}
        return MainRequest
    
TestManager = ServerManager()


    
        

