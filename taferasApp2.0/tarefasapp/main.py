from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

class TaskApp(App):
    def build(self):
        self.tasks = []
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Welcome message
        welcome_label = Label(text='Bem-vindo, Roger Barreto!', size_hint_y=None, height=50)
        layout.add_widget(welcome_label)
        
        # Input for new tasks
        self.task_input = TextInput(hint_text='Digite uma nova tarefa', size_hint_y=None, height=40)
        layout.add_widget(self.task_input)
        
        # Add task button
        add_button = Button(text='Adicionar Tarefa', size_hint_y=None, height=50)
        add_button.bind(on_press=self.add_task)
        layout.add_widget(add_button)
        
        # Scrollable task list
        self.task_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))
        
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 300))
        scroll_view.add_widget(self.task_list)
        layout.add_widget(scroll_view)
        
        return layout
    
    def add_task(self, instance):
        task = self.task_input.text.strip()
        if task:
            task_layout = BoxLayout(size_hint_y=None, height=40)
            task_label = Label(text=task)
            delete_button = Button(text='Excluir', size_hint_x=None, width=80)
            delete_button.bind(on_press=lambda x: self.delete_task(task_layout))
            
            task_layout.add_widget(task_label)
            task_layout.add_widget(delete_button)
            
            self.task_list.add_widget(task_layout)
            self.tasks.append(task)
            self.task_input.text = ''
    
    def delete_task(self, task_layout):
        self.task_list.remove_widget(task_layout)

if __name__ == '__main__':
    TaskApp().run()

