from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window

# Simple database structure
drug_database = {
    "Analgesics": {
        "Paracetamol": "Common pain reliever and fever reducer. Max dose: 4g/day for adults.",
        "Ibuprofen": "NSAID for pain, fever, and inflammation. Can cause stomach irritation.",
        "Aspirin": "Pain reliever, anti-inflammatory, and antiplatelet. Not for children."
    },
    "Antibiotics": {
        "Amoxicillin": "Penicillin antibiotic for bacterial infections. Common for ear/nose/throat infections.",
        "Azithromycin": "Macrolide antibiotic. Often used for respiratory infections.",
        "Ciprofloxacin": "Fluoroquinolone antibiotic. Used for UTIs and some GI infections."
    },
    "Antihistamines": {
        "Loratadine": "Non-drowsy antihistamine for allergies. Taken once daily.",
        "Diphenhydramine": "First-gen antihistamine. Causes drowsiness, also used as sleep aid.",
        "Cetirizine": "Second-gen antihistamine. Less drowsy than first-gen options."
    }
}

# Welcome Screen
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        
        title = Label(text="Ophthalmology Drugs",
                    size_hint=(1, 0.3), 
                    font_size='28sp',
                    color=(0.405, 0.007, 0.000))
                                                                                                     
        subtitle = Label(text="Your guide to common medications \n __________________________________ \n  (Put your mobile in horizontal mode \n for better browsing)", 
                        size_hint=(1, 0.2),
                        font_size='18sp',
                        color=(0.000, 0.000, 0.000))
        
        
        
        start_btn = Button(text="Get Started", 
                         size_hint=(0.6, 0.15),
                         pos_hint={'center_x': 0.5},
                         background_color=(0.2, 0.6, 0.9, 1))
        start_btn.bind(on_press=self.start_app)
        
        exit_btn = Button(text="Exit App", 
                        size_hint=(0.6, 0.15),
                        pos_hint={'center_x': 0.5},
                        background_color=(0.8, 0.2, 0.2, 1))
        exit_btn.bind(on_press=self.confirm_exit)
        
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(start_btn)
        layout.add_widget(exit_btn)
        self.add_widget(layout)
    
    def start_app(self, instance):
        self.manager.current = 'categories'
    
    def confirm_exit(self, instance):
        self.show_confirmation_dialog()
    
    def show_confirmation_dialog(self):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text="Are you sure you want to exit?"))
        
        btn_box = BoxLayout(spacing=5)
        yes_btn = Button(text="Yes", size_hint=(0.5, None), height=40)
        no_btn = Button(text="No", size_hint=(0.5, None), height=40)
        
        btn_box.add_widget(no_btn)
        btn_box.add_widget(yes_btn)
        box.add_widget(btn_box)
        
        popup = Popup(title='Exit Confirmation',
                     size_hint=(0.7, 0.3),
                     content=box)
        
        yes_btn.bind(on_press=lambda x: App.get_running_app().stop())
        no_btn.bind(on_press=popup.dismiss)
        
        popup.open()

# Screen for category selection
class CategoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Header with back and exit buttons
        header = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text="Back", size_hint=(0.2, 1))
        back_btn.bind(on_press=self.go_back)
        title = Label(text="Select Drug Category", font_size='24sp')
        exit_btn = Button(text="Exit", size_hint=(0.2, 1))
        exit_btn.bind(on_press=self.confirm_exit)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        header.add_widget(exit_btn)
        layout.add_widget(header)
        
        # Main content
        scroll = ScrollView()
        button_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        button_layout.bind(minimum_height=button_layout.setter('height'))
        
        for category in drug_database.keys():
            btn = Button(text=category, 
                       size_hint_y=None, 
                       height=100,
                       background_color=(0.2, 0.6, 0.9, 1))
            btn.bind(on_press=self.category_selected)
            button_layout.add_widget(btn)
        
        scroll.add_widget(button_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def category_selected(self, instance):
        self.manager.current = 'drugs'
        self.manager.get_screen('drugs').set_drugs(instance.text)
    
    def go_back(self, instance):
        self.manager.current = 'welcome'
    
    def confirm_exit(self, instance):
        self.show_confirmation_dialog()
    
    def show_confirmation_dialog(self):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text="Are you sure you want to exit?"))
        
        btn_box = BoxLayout(spacing=5)
        yes_btn = Button(text="Yes", size_hint=(0.5, None), height=40)
        no_btn = Button(text="No", size_hint=(0.5, None), height=40)
        
        btn_box.add_widget(no_btn)
        btn_box.add_widget(yes_btn)
        box.add_widget(btn_box)
        
        popup = Popup(title='Exit Confirmation',
                     size_hint=(0.7, 0.3),
                     content=box)
        
        yes_btn.bind(on_press=lambda x: App.get_running_app().stop())
        no_btn.bind(on_press=popup.dismiss)
        
        popup.open()

# Screen for drug selection within a category
class DrugsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.add_widget(self.layout)
        self.category = ""
    
    def set_drugs(self, category):
        self.category = category
        self.layout.clear_widgets()
        
        # Header with back and exit buttons
        header = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text="Back", size_hint=(0.2, 1))
        back_btn.bind(on_press=self.go_back)
        title = Label(text=f"Drugs in {self.category}", font_size='24sp')
        exit_btn = Button(text="Exit", size_hint=(0.2, 1))
        exit_btn.bind(on_press=self.confirm_exit)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        header.add_widget(exit_btn)
        self.layout.add_widget(header)
        
        # Main content
        scroll = ScrollView()
        button_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        button_layout.bind(minimum_height=button_layout.setter('height'))
        
        for drug in drug_database[self.category].keys():
            btn = Button(text=drug, 
                       size_hint_y=None, 
                       height=100,
                       background_color=(0.9, 0.9, 0.9, 1),
                       color=(1.000, 1.000, 1.000))
            btn.bind(on_press=self.drug_selected)
            button_layout.add_widget(btn)
        
        scroll.add_widget(button_layout)
        self.layout.add_widget(scroll)
    
    def drug_selected(self, instance):
        self.manager.current = 'details'
        self.manager.get_screen('details').set_details(self.category, instance.text)
    
    def go_back(self, instance):
        self.manager.current = 'categories'
    
    def confirm_exit(self, instance):
        self.show_confirmation_dialog()
    
    def show_confirmation_dialog(self):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text="Are you sure you want to exit?"))
        
        btn_box = BoxLayout(spacing=5)
        yes_btn = Button(text="Yes", size_hint=(0.5, None), height=40)
        no_btn = Button(text="No", size_hint=(0.5, None), height=40)
        
        btn_box.add_widget(no_btn)
        btn_box.add_widget(yes_btn)
        box.add_widget(btn_box)
        
        popup = Popup(title='Exit Confirmation',
                     size_hint=(0.7, 0.3),
                     content=box)
        
        yes_btn.bind(on_press=lambda x: App.get_running_app().stop())
        no_btn.bind(on_press=popup.dismiss)
        
        popup.open()

# Screen for drug details
class DetailsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.add_widget(self.layout)
    
    def set_details(self, category, drug):
        self.layout.clear_widgets()
        
        # Header with back and exit buttons
        header = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text="Back", size_hint=(0.2, 1))
        back_btn.bind(on_press=self.go_back)
        title = Label(text=drug, font_size='24sp')
        exit_btn = Button(text="Exit", size_hint=(0.2, 1))
        exit_btn.bind(on_press=self.confirm_exit)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        header.add_widget(exit_btn)
        self.layout.add_widget(header)
        
        # Category label
        category_label = Label(text=f"Category: {category}", 
                             size_hint=(1, 0.05),
                             color=(0.000, 0.000, 0.000))
        self.layout.add_widget(category_label)
        
        # Drug details
        scroll = ScrollView()
        details = Label(text=drug_database[category][drug], 
                       size_hint_y=None,
                       halign='left', 
                       valign='top', 
                       padding=(10, 10),
                       color=(0.000,0.000,0.000))
        details.bind(texture_size=details.setter('size'))
        scroll.add_widget(details)
        self.layout.add_widget(scroll)
    
    def go_back(self, instance):
        self.manager.current = 'drugs'
    
    def confirm_exit(self, instance):
        self.show_confirmation_dialog()
    
    def show_confirmation_dialog(self):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text="Are you sure you want to exit?"))
        
        btn_box = BoxLayout(spacing=5)
        yes_btn = Button(text="Yes", size_hint=(0.5, None), height=40)
        no_btn = Button(text="No", size_hint=(0.5, None), height=40)
        
        btn_box.add_widget(no_btn)
        btn_box.add_widget(yes_btn)
        box.add_widget(btn_box)
        
        popup = Popup(title='Exit Confirmation',
                     size_hint=(0.7, 0.3),
                     content=box)
        
        yes_btn.bind(on_press=lambda x: App.get_running_app().stop())
        no_btn.bind(on_press=popup.dismiss)
        
        popup.open()

# Main App
class MedicalDrugsApp(App):
    def build(self):
        Window.clearcolor = (0.695,0.505,0.330,0)  # Light gray background
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(CategoryScreen(name='categories'))
        sm.add_widget(DrugsScreen(name='drugs'))
        sm.add_widget(DetailsScreen(name='details'))
        return sm

if __name__ == '__main__':
    MedicalDrugsApp().run()
