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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
import webbrowser 

Builder.load_file(filename='main.kv')

class Wp(BoxLayout):
    pass

class ProfileScreen(Screen):
    pass

class GpsStopRecordingScreen2(Screen):
    pass

class SavedTrail(Wp):
    name = StringProperty("")
    description = StringProperty("")

class PublicTrail(Wp):
    trail_name = StringProperty("")
    username = StringProperty("")
    date = StringProperty("")
    distance = StringProperty("")
    description = StringProperty("")
    trail_id = StringProperty("")

class UserTime(Wp):
    username = StringProperty("")
    run_time = StringProperty("")
    trail_id = StringProperty("")

class UserRuntime(Wp):
    trail_name = StringProperty("")
    run_time = StringProperty("")
    trail_id = StringProperty("")

class TrailInfoScreen(Screen):
    trail_name = StringProperty("")
    username = StringProperty("")
    date = StringProperty("")
    distance = StringProperty("")
    description = StringProperty("")
    trail_id = StringProperty("")


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

class TrailMapScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

MainFileManager = FileManager()
MainScreenManager = ScreenManager(transition=NoTransition())
MainServerManager = ServerManager()

class Trailz(App):
    preview_mode = False  # false - true connection
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._GPSJsonDict = {'GPSData':{}}
        self._jsonTrailPath = "saved_trails/"
        self._MinDistancePar = 1
        self._config = {}
        self.current_trail_id = ""
        self.preview_mode = False
        
    def login(self) -> None:
        if self.preview_mode:
            print("PREVIEW MODE")
            self._config = {
                "email": "preview@example.com",
                "password": "preview",
                "username": "PreviewUser"
            }
            MainFileManager.configure(email=self._config["email"], 
                                    password=self._config["password"])
            self.switch_toSTR("MenuScreen")
            return
            
        email = MainScreenManager.get_screen("LoginScreen").ids.email.text
        password = MainScreenManager.get_screen("LoginScreen").ids.password.text
        if str(MainServerManager.login(email=email,password=password)) == "False":
            pass    
        else:
            self.switch_toSTR("MenuScreen")
            MainFileManager.configure(email=email,password=password)
    
    def sign_up(self):
        if self.preview_mode:
            print("PREVIEW MODE")
            email = MainScreenManager.get_screen("SignUpScreen").ids.email.text
            username = MainScreenManager.get_screen("SignUpScreen").ids.username.text
            
            self._config = {
                "email": email if email else "preview@example.com",
                "password": "preview",
                "username": username if username else "PreviewUser"
            }
            MainFileManager.configure(email=self._config["email"], 
                                    password=self._config["password"])
            self.switch_toSTR("MenuScreen")
            return
            
        email = MainScreenManager.get_screen("SignUpScreen").ids.email.text
        password = MainScreenManager.get_screen("SignUpScreen").ids.password.text
        username = MainScreenManager.get_screen("SignUpScreen").ids.username.text
        if str(MainServerManager.sign_up(email=email,password=password,username=username)) != "success":
            pass
        else:
            self.switch_toSTR("MenuScreen")
            MainFileManager.configure(email=email,password=password)
            
    def send_own_trail(self,trail_name):
        MainFileManager.load_own_trail(trail_name, self._config["email"],self._config["password"])    
          
    def create_own_saved_trails_screen(self):
        MainScreenManager.get_screen('SavedTrailsScreen').ids.MainLayout.clear_widgets()
        saved_trails = MainFileManager.get_own_saved_trails_info()
        MainScreen = MainScreenManager.get_screen('SavedTrailsScreen')
        for i in range(len(saved_trails)):
            trail = SavedTrail()
            MainScreen.ids.MainLayout.add_widget(trail)
            trail.name = saved_trails[i]["name"]
            trail.description = saved_trails[i]["description"]
        
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
        from kivy.core.window import Window
        global MainScreenManager
        MainScreenManager.add_widget(LoginSignUpScreen(name="LoginSignUpScreen"))
        MainScreenManager.add_widget(LoginScreen(name="LoginScreen"))
        MainScreenManager.add_widget(SignUpScreen(name="SignUpScreen"))
        MainScreenManager.add_widget(TrailInfoScreen(name="TrailInfoScreen"))
        MainScreenManager.add_widget(MenuScreen(name='MenuScreen'))
        MainScreenManager.add_widget(GpsInfoScreen(name='GpsInfoScreen'))
        MainScreenManager.add_widget(SavedTrailsScreen(name='SavedTrailsScreen'))
        MainScreenManager.add_widget(StopGpsScreen(name='StopGpsScreen'))
        MainScreenManager.add_widget(GpsStopRecordingScreen2(name="GpsStopRecordingScreen2"))
        self.create_own_saved_trails_screen()
        self.create_public_trails_screen()
        MainScreenManager.add_widget(GpsStartRecordingScreen(name='GpsStartRecordingScreen'))
        MainScreenManager.add_widget(GpsStopRecordingScreen(name='GpsStopRecordingScreen'))
        MainScreenManager.add_widget(TestScreen(name='TestScreen'))
        MainScreenManager.add_widget(ProfileScreen(name="ProfileScreen"))
        MainScreenManager.add_widget(TrailMapScreen(name='TrailMapScreen'))
        
        self._config = MainFileManager.load_config()
        if not self._config:
            self.switch_toSTR("LoginSignUpScreen")
        else:
            self.switch_toSTR('MenuScreen')
        
        if platform == "android":
            from plyer import gps
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
            print("")

    @staticmethod
    def start_gps():
        if platform == "android":
            from plyer import gps
            gps.start(0,1)
        
    @staticmethod
    def stop_gps():
        if platform == "android":
            from plyer import gps
            gps.stop()
    
    def open_gps_recording(self) -> None:
        if platform == "ios" or platform == "android":
            MainScreenManager.current = 'GpsStartRecordingScreen'
        else:
            # не открывается и может выводить ошибку
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
            self.create_own_saved_trails_screen()
            MainScreenManager.current = 'MenuScreen'
            self._GPSJsonDict = {'GPSData':{}}
            
    def open_trail_info_screen(self, trail_name, username, start_date, distance, description, trail_id, **kwargs):
        MainScreen = MainScreenManager.get_screen("TrailInfoScreen")
        MainScreen.trail_name = trail_name
        MainScreen.username = username
        MainScreen.date = start_date
        MainScreen.distance = str(distance)
        MainScreen.description = description
        MainScreen.trail_id = trail_id
        
        self.create_leaderboard_screen()
        MainScreenManager.current = "TrailInfoScreen"
    
    def preview_trail_map(self, trail_id):
        gps_data = MainServerManager.get_trail_file(trail_id)["data"]
        html_path = MainFileManager.save_trail_html(gps_data, f"trail_{trail_id}_preview.html")
        if html_path:
            self.show_html_map(html_path)
        else:
            print("Failed to generate HTML map")
            try:
                trail_screen = MainScreenManager.get_screen('TrailInfoScreen')
                error_label = Label(
                    text='Failed to load trail map',
                    color=(1, 0, 0, 1),
                    size_hint_y=None,
                    height='30dp'
                )
                if hasattr(trail_screen.ids, 'map_container'):
                    trail_screen.ids.map_container.add_widget(error_label)
            except:
                pass

    def show_html_map(self, html_file_path):
        try:
            file_url = f"file://{html_file_path}"

            webbrowser.open(file_url)
            
            try:
                trail_screen = MainScreenManager.get_screen('TrailInfoScreen')
                success_label = Label(
                    text='Map opened in browser',
                    color=(0.2, 0.6, 0.2, 1),
                    size_hint_y=None,
                    height='30dp'
                )
                if hasattr(trail_screen.ids, 'map_container'):
                    for child in trail_screen.ids.map_container.children[:]:
                        if isinstance(child, Label) and child.text in ['Map opened in browser', 'Failed to load trail map', 'Error opening map']:
                            trail_screen.ids.map_container.remove_widget(child)
                    
                    trail_screen.ids.map_container.add_widget(success_label)
            except:
                pass
                
        except Exception as e:
            print(f"Error opening map in browser: {e}")
            
            try:
                trail_screen = MainScreenManager.get_screen('TrailInfoScreen')
                error_label = Label(
                    text=f'Error: Could not open map',
                    color=(1, 0, 0, 1),
                    size_hint_y=None,
                    height='30dp'
                )
                if hasattr(trail_screen.ids, 'map_container'):
                    trail_screen.ids.map_container.add_widget(error_label)
            except:
                pass

    def preview_current_gps_map(self):
        if self._GPSJsonDict.get('GPSData'):
            try:
                html_path = MainFileManager.save_trail_html(
                    self._GPSJsonDict, 
                    "current_trail_preview.html"
                )
                if html_path:
                    self.show_gps_info_map(html_path)
                else:
                    print("Failed to generate map from GPS data")

                    if hasattr(MainScreenManager.get_screen('GpsInfoScreen').ids, 'gps_map_container'):
                        from kivy.uix.label import Label
                        error_label = Label(
                            text='Failed to generate map preview',
                            color=(1, 0, 0, 1),
                            size_hint_y=None,
                            height='30dp'
                        )
                        MainScreenManager.get_screen('GpsInfoScreen').ids.gps_map_container.add_widget(error_label)
            except Exception as e:
                print(f"Error previewing GPS map: {e}")
        else:
            print("No GPS data recorded yet")

            if hasattr(MainScreenManager.get_screen('GpsInfoScreen').ids, 'gps_map_container'):
                from kivy.uix.label import Label
                info_label = Label(
                    text='Start recording to see trail preview',
                    color=(0.8, 0.5, 0, 1),
                    size_hint_y=None,
                    height='30dp'
                )
                MainScreenManager.get_screen('GpsInfoScreen').ids.gps_map_container.add_widget(info_label)

    def show_gps_info_map(self, html_file_path):
        try:
            file_url = f"file://{html_file_path}"
            webbrowser.open(file_url)
            
            if hasattr(MainScreenManager.get_screen('GpsInfoScreen').ids, 'gps_map_container'):
                from kivy.uix.label import Label
                success_label = Label(
                    text='Map opened in browser',
                    color=(0.2, 0.6, 0.2, 1),
                    size_hint_y=None,
                    height='30dp'
                )
                
                gps_screen = MainScreenManager.get_screen('GpsInfoScreen')
                for child in gps_screen.ids.gps_map_container.children[:]:
                    if isinstance(child, Label) and child.text in ['Map opened in browser', 'Start recording to see trail preview', 'Failed to generate map preview']:
                        gps_screen.ids.gps_map_container.remove_widget(child)
                
                gps_screen.ids.gps_map_container.add_widget(success_label)
                    
        except Exception as e:
            print(f"Error opening GPS map in browser: {e}")
            
            if hasattr(MainScreenManager.get_screen('GpsInfoScreen').ids, 'gps_map_container'):
                from kivy.uix.label import Label
                error_label = Label(
                    text='Error opening map in browser',
                    color=(1, 0, 0, 1),
                    size_hint_y=None,
                    height='30dp'
                )
                MainScreenManager.get_screen('GpsInfoScreen').ids.gps_map_container.add_widget(error_label)

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
                runtime_widget = UserRuntime()
                ProfileScreen.ids.SecondLayout.add_widget(runtime_widget)
                runtime_widget.trail_name = str(runtime)
                runtime_widget.run_time = str(data[runtime])
            MainScreenManager.current = "ProfileScreen"
        
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