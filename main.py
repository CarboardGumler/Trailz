
import datetime
import kivy
import GpsProcess
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.utils import platform
import time
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from FileWork import FileManager
from ServerWorks import ServerManager
from GpsProcess import *
from kivy.uix.label import Label
if platform == "android":
    from plyer import gps

Builder.load_file(filename='main.kv')

class ProfileScreen(Screen):
    pass

class GpsStopRecordingScreen2(Screen):
    pass

class Wp(Widget):
    pass

class SavedTrail(Wp):
    pass

class PublicTrail(Wp):
    pass

class UserTime(Wp):
    pass

class   UserRuntime(Wp):
    pass

class TrailInfoScreen(Screen):
    pass

class StopGpsScreen(Screen):
    pass

class SavedTrailsScreen(Screen):
    pass      
    
class LoginSignUpScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class SignUpScreen(Screen):
    pass

class GpsStartRecordingScreen(Screen):
    pass

class GpsStopRecordingScreen(Screen):
    pass

class GpsInfoScreen(Screen):
    pass


class MenuScreen(Screen):
    pass


class TestScreen(Screen):
    pass


class SavedTrailzScreen0(Screen):
    pass

MainFileManager = FileManager()
MainScreenManager = ScreenManager()
MainServerManager = ServerManager()

class Trailz(App):
    
    gps_location = StringProperty()
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._GPSJsonDict = {'GPSData':{}}
        self._jsonTrailPath = "saved_trails/"
        self._MinDistancePar = 1
        self._config = {}
        self.current_trail_id = ""
    
    def login(self) -> None:
        email = MainScreenManager.get_screen("LoginScreen").ids.email.text
        password = MainScreenManager.get_screen("LoginScreen").ids.password.text
        #добавить поп ап
        if str(MainServerManager.login(email=email,password=password)) == "False":
            pass    
        else:
            self.switch_toSTR("MenuScreen")
            MainFileManager.configure(email=email,password=password)
        
    def sign_up(self):
        email = MainScreenManager.get_screen("SignUpScreen").ids.email.text
        password = MainScreenManager.get_screen("SignUpScreen").ids.password.text
        username = MainScreenManager.get_screen("SignUpScreen").ids.username.text
        #добавить поп ап
        if str(MainServerManager.sign_up(email=email,password=password,username=username)) != "success":
            pass
        else:
            self.switch_toSTR("MenuScreen")
            MainFileManager.configure(email=email,password=password)
            
    def send_own_trail(self,trail_name):
        #добавить поп ап
        #метод у файл менеджера, тк файл должен быть открыт во время загрузки
        MainFileManager.load_own_trail(trail_name, self._config["email"],self._config["password"])    
          
    def creat_own_saved_trails_screen(self):
        MainScreenManager.get_screen('SavedTrailsScreen').ids.MainLayout.clear_widgets()
        saved_trails = MainFileManager.get_own_saved_trails_info()
        MainScreen = MainScreenManager.get_screen('SavedTrailsScreen')
        for i in range(len(saved_trails)):
            trail = SavedTrail()
            MainScreen.ids.MainLayout.ids[f"trail_{i}"] = trail
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].name = saved_trails[i]["name"]
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].description = saved_trails[i]["description"]    
            MainScreen.ids.MainLayout.add_widget(trail)
        
    def create_public_trails_screen(self,page=0):
        sort_type = "default"
        location = " "
        MainScreen = MainScreenManager.get_screen('MenuScreen')
        MainScreen.ids.MainLayout.clear_widgets()
        if MainScreen.ids.TrailSearch.text == "":
            trail_list = MainServerManager.get_all_trails(sort_type,location,page)
        else:
             trail_list = MainServerManager.get_trail_key_word(MainScreen.ids.TrailSearch.text,page)["data"]
        print(trail_list)
        if page != 0 and trail_list == []:
            page -= 2
        i = 0
        for trail_data in trail_list:
            trail = PublicTrail()
            MainScreen.ids.MainLayout.ids[f"trail_{i}"] = trail
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].trail_name = str(trail_data[0])
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].username = str(trail_data[1])
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].distance = str(trail_data[2]) + " km"
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].date = str(trail_data[3])
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].trail_id = str(trail_data[6])
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].description = str(trail_data[7]) 
            MainScreen.ids.MainLayout.add_widget(trail)
            i+=1
        MainScreen.ids.MainLayout.amount = i + 1
        MainButton = Button(text="загрузить ещё",size_hint_y=None)
        MainButton.bind(on_press=lambda x:self.create_public_trails_screen(page+1))
        MainScreen.ids.MainLayout.add_widget(MainButton)
    
    def create_leaderboard_screen(self,page=0):
        MainScreen = MainScreenManager.get_screen('TrailInfoScreen')
        MainScreen.ids.MainLayout.clear_widgets()
        trail_id = MainScreen.trail_id
        data_list = MainServerManager.get_leaderboard(trail_id,page)
        if page != 0 and data_list == []:
            page -= 2
        i = 0
        for data in data_list:
            user_time = UserTime()
            MainScreen.ids.MainLayout.ids[f"user_time_{i}"] = user_time
            MainScreen.ids.MainLayout.ids[f"user_time_{i}"].username = str(data[0])
            MainScreen.ids.MainLayout.ids[f"user_time_{i}"].run_time = str(data[1])
            MainScreen.ids.MainLayout.add_widget(user_time)
            i+=1

        MainScreen.ids.MainLayout.amount = i + 1
        MainButton = Button(text="загрузить ещё",size_hint_y=None)
        MainButton.bind(on_press=lambda x:self.create_leaderboard_screen(page+1))
        MainScreen.ids.MainLayout.add_widget(MainButton)
    
    def switch_toSTR(self, screenSTR : str) -> None:
        MainScreenManager.current = screenSTR

    @mainthread   
    def on_location(self, **kwargs) -> None:
        self._GPSJsonDict['GPSData'][int(time.time()) % 2592000] = kwargs
        self.gps_location = '\n'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])   
    
    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission,check_permission
        PermissionList = [Permission.ACCESS_COARSE_LOCATION,Permission.ACCESS_FINE_LOCATION,Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]
        def callback(permissions, results):
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")
        if not all(check_permission(permission) for permission in PermissionList): 
            request_permissions(PermissionList, callback)

    def build(self):
        global MainScreenManager
        MainScreenManager.add_widget(LoginSignUpScreen(name="LoginSignUpScreen"))
        MainScreenManager.add_widget(LoginScreen(name="LoginScreen"))
        MainScreenManager.add_widget(SignUpScreen(name="SignUpScreen"))
        MainScreenManager.add_widget(TrailInfoScreen(name="TrailInfoScreen"))
        MainScreenManager.add_widget(MenuScreen(name='MenuScreen'))
        MainScreenManager.add_widget(GpsInfoScreen(name='GpsInfoScreen'))
        MainScreenManager.add_widget(SavedTrailsScreen(name='SavedTrailsScreen'))
        MainScreenManager.add_widget(StopGpsScreen(name='SavedTrailsScreen'))
        MainScreenManager.add_widget(GpsStopRecordingScreen2(name="GpsStopRecordingScreen2"))
        self.creat_own_saved_trails_screen()
        self.create_public_trails_screen()
        MainScreenManager.add_widget(GpsStartRecordingScreen(name='GpsStartRecordingScreen'))
        MainScreenManager.add_widget(GpsStopRecordingScreen(name='GpsStopRecordingScreen'))
        MainScreenManager.add_widget(TestScreen(name='TestScreen'))
        MainScreenManager.add_widget(ProfileScreen(name="ProfileScreen"))
        
        self._config = MainFileManager.load_config()
        if self._config == False:
            self.switch_toSTR("LoginSignUpScreen")
        if self._config != False:
            self.switch_toSTR('MenuScreen')
        
        if platform == "android":
            try:
                gps.configure(on_location=self.on_location)
            except NotImplementedError:
                import traceback
                traceback.print_exc()
            self.request_android_permissions()
        MainFileManager.MakeDirs()
        return MainScreenManager
    
    
    def send_public_trail(self):
        is_valid = MainFileManager.save_public_trail(self._GPSJsonDict,self.current_trail_id)
        self._GPSJsonDict = {'GPSData':{}}
        
    def start_rerun(self,trail_id):
        self._GPSJsonDict = {'GPSData':{}}
        try: 
            self.current_trail_id = trail_id
            self.start_gps()
            self.switch_toSTR("GpsStopRecordingScreen2")

        except:
            print("not implemented")

    @staticmethod
    def start_gps():
        gps.start(0,1)
        
    @staticmethod
    def stop_gps():
        gps.stop()
    
    def open_gps_recording(self) -> None:
        if platform == "ios" or platform == "android":
            MainScreenManager.current = 'GpsStartRecordingScreen'
        else:
            #не открывается и может выводить ошибку
            pass 
    
    def Save_GPS_to_json(self) -> None:
        if MainScreenManager.get_screen('GpsInfoScreen').ids.GPSNameInput.text != "" and MainScreenManager.get_screen('GpsInfoScreen').ids.GPSDescriptionInput.text != "" and MainScreenManager.get_screen('GpsInfoScreen').ids.GPSMinDistanceInput.text != "":
            if self._GPSJsonDict['GPSData'] == {}:
                MainScreenManager.current = "MenuScreen"
                return None
            self._GPSJsonDict['name'] = MainScreenManager.get_screen('GpsInfoScreen').ids.GPSNameInput.text
            self._GPSJsonDict['description'] = MainScreenManager.get_screen('GpsInfoScreen').ids.GPSDescriptionInput.text
            self._GPSJsonDict['MinDistance'] = MainScreenManager.get_screen('GpsInfoScreen').ids.GPSMinDistanceInput.text
            print(self._GPSJsonDict)
            SecDict = get_gps_info(self._GPSJsonDict)
            self._GPSJsonDict["avg_speed"] = SecDict["avg_speed"]
            self._GPSJsonDict["distance"] = SecDict["distance"]
            self._GPSJsonDict["date"] = datetime.datetime.today().strftime('%Y-%m-%d')
            MainFileManager.save_trail(FileName=self._GPSJsonDict['name'], JsonDict=self._GPSJsonDict)
            MainScreenManager.get_screen('TestScreen').ids.TestLabel.text = str(self._GPSJsonDict)
            self.creat_own_saved_trails_screen()
            MainScreenManager.current = 'MenuScreen'
            self._GPSJsonDict = {'GPSData':{}}
            
    def open_trail_info_screen(self,trail_name,username,start_date,distance,description,trail_id,**kwargs):
        MainScreen = MainScreenManager.get_screen("TrailInfoScreen")
        MainScreen.trail_name = trail_name
        MainScreen.username = username
        MainScreen.date = start_date
        MainScreen.distance = str(distance)
        MainScreen.description = description
        MainScreen.trail_id = trail_id
        self.create_leaderboard_screen()
        MainScreenManager.current = "TrailInfoScreen"
        
    def search_trail(self):
        MenuScreen = MainScreenManager.get_screen("MenuScreen")
        trail_name = MenuScreen.ids.TrailSearch.text
        if trail_name != "":
            self.create_public_trails_screen(0)
        
        
    def open_profile(self):
        MenuScreen = MainScreenManager.get_screen("MenuScreen")
        ProfileScreen = MainScreenManager.get_screen("ProfileScreen")
        username = MenuScreen.ids.UserSearch.text
        if username != "":
            ProfileScreen.ids.SecondLayout.clear_widgets()
            ProfileScreen.ids.username.text = username
            data = MainServerManager.get_user_runtimes(username)["data"]
            for runtime in data:
                runtime_wideget = UserRuntime()
                ProfileScreen.ids[f"trail_{runtime}"] = runtime_wideget
                ProfileScreen.ids[f"trail_{runtime}"].name_text = runtime
                ProfileScreen.ids[f"trail_{runtime}"].run_time = str(data[runtime])
                ProfileScreen.add_widget(runtime_wideget)
            MainScreenManager.current = ProfileScreen
        
    def log_out(self):
        MainFileManager.log_out()
        App.get_running_app().stop()
    @property
    def MinDistanceSetting(self) -> int:
        return self._MinDistancePar
    
    @property
    def GPSJsonDict(self) -> dict:
        return self._GPSJsonDict
    
    
    def Pass(self):
        pass
    


if __name__ == '__main__':
    Trailz().run()
    
