import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.core.image import Image as CoreImage
from PIL import Image as PILImage
import io
import sqlite3
import datetime
import os  # Importar para verificar o caminho do arquivo

# Definição do tamanho da imagem para armazenamento (melhora o desempenho do SQLite)
IMAGE_MAX_SIZE = (100, 100)


class TaskApp(App):
    def build(self):
        self.tasks = []
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()
        self.create_table()

        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 1. Informações de Boas-Vindas
        welcome_label = Label(
            text='Bem-vindo, Roger Barreto! 🚀', size_hint_y=None, height=50)
        layout.add_widget(welcome_label)

        # 2. Layout para Inputs
        input_layout = BoxLayout(
            orientation='vertical', spacing=5, size_hint_y=None, height=450)

        self.task_input = TextInput(
            hint_text='Descrição da Tarefa', size_hint_y=None, height=40)
        input_layout.add_widget(self.task_input)

        self.client_input = TextInput(
            hint_text='Nome do Cliente', size_hint_y=None, height=40)
        input_layout.add_widget(self.client_input)

        self.address_input = TextInput(
            hint_text='Endereço do Cliente', size_hint_y=None, height=40)
        input_layout.add_widget(self.address_input)

        self.service_type_input = TextInput(
            hint_text='Tipo de Serviço', size_hint_y=None, height=40)
        input_layout.add_widget(self.service_type_input)

        # input_type='number' foi removido porque não é padrão para TextInput no Kivy,
        # e é melhor validar a conversão para float
        self.labor_value_input = TextInput(
            hint_text='Valor de Mão de Obra (ex: 150.00)', size_hint_y=None, height=40)
        input_layout.add_widget(self.labor_value_input)

        self.execution_date_input = TextInput(
            hint_text='Data de Execução (YYYY-MM-DD)', size_hint_y=None, height=40)
        input_layout.add_widget(self.execution_date_input)

        self.completion_date_input = TextInput(
            hint_text='Data de Conclusão (YYYY-MM-DD)', size_hint_y=None, height=40)
        input_layout.add_widget(self.completion_date_input)

        self.image_input = TextInput(
            hint_text='Caminho da Imagem (ex: C:/foto.jpg)', size_hint_y=None, height=40)
        input_layout.add_widget(self.image_input)

        # Pré-visualização da imagem (para UX)
        self.image_preview = Image(size_hint_y=None, height=60)
        input_layout.add_widget(self.image_preview)

        layout.add_widget(input_layout)

        # Botão para adicionar e pré-visualizar (para testar o caminho)
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        preview_button = Button(text='Pré-visualizar Imagem', size_hint_x=0.5)
        preview_button.bind(
            on_press=lambda x: self.load_image_and_display_preview(self.image_input.text))
        button_layout.add_widget(preview_button)

        add_button = Button(text='Adicionar Tarefa', size_hint_x=0.5)
        add_button.bind(on_press=self.add_task)
        button_layout.add_widget(add_button)

        layout.add_widget(button_layout)

        # 3. Lista de Tarefas
        self.task_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))

        # Ajustado size_hint para ocupar o espaço restante
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.task_list)
        layout.add_widget(scroll_view)

        # Carregar tarefas ao iniciar
        self.load_tasks()

        return layout

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                client_name TEXT,
                client_address TEXT,
                service_type TEXT,
                labor_value REAL,
                execution_date TEXT,
                completion_date TEXT,
                image BLOB
            )
        ''')
        self.conn.commit()

    def load_image_and_display_preview(self, image_path):
        """Carrega a imagem e exibe no widget de pré-visualização."""
        self.image_preview.texture = None
        if not image_path or not os.path.exists(image_path):
            self.show_popup(
                "Caminho de imagem inválido ou arquivo não encontrado.")
            return

        try:
            # Tenta carregar e redimensionar a imagem para visualização
            pil_image = PILImage.open(image_path)
            pil_image.thumbnail(IMAGE_MAX_SIZE)

            # Salva no buffer para o Kivy CoreImage
            image_bytes = io.BytesIO()
            pil_image.save(image_bytes, format='PNG')  # Usar PNG ou JPEG
            image_bytes.seek(0)

            core_image = CoreImage(image_bytes, ext='png')
            self.image_preview.texture = core_image.texture

        except Exception as e:
            self.show_popup(f"Erro ao carregar ou pré-visualizar imagem: {e}")

    def add_task(self, instance):
        task = self.task_input.text.strip()
        client_name = self.client_input.text.strip()
        client_address = self.address_input.text.strip()
        service_type = self.service_type_input.text.strip()
        labor_value_text = self.labor_value_input.text.strip().replace(
            ',', '.')  # Permite vírgula ou ponto
        execution_date = self.execution_date_input.text.strip()
        completion_date = self.completion_date_input.text.strip()
        image_path = self.image_input.text.strip()

        # 1. Validação da Tarefa Principal
        if not task:
            self.show_popup("Por favor, digite uma descrição para a Tarefa.")
            return

        # 2. Validação e Conversão do Valor de Mão de Obra
        labor_value = 0.0
        if labor_value_text:
            try:
                labor_value = float(labor_value_text)
            except ValueError:
                self.show_popup(
                    "Valor de mão de obra inválido. Digite um número válido (ex: 150.00).")
                return

        # 3. Validação das Datas
        if execution_date:
            try:
                datetime.datetime.strptime(execution_date, '%Y-%m-%d')
            except ValueError:
                self.show_popup(
                    "Formato de data de execução incorreto (YYYY-MM-DD).")
                return

        if completion_date:
            try:
                datetime.datetime.strptime(completion_date, '%Y-%m-%d')
            except ValueError:
                self.show_popup(
                    "Formato de data de conclusão incorreto (YYYY-MM-DD).")
                return

        # 4. Carregamento e Armazenamento da Imagem como BLOB
        image_blob = None
        if image_path and os.path.exists(image_path):
            try:
                # Carrega, redimensiona e comprime antes de salvar no banco de dados
                pil_image = PILImage.open(image_path)
                # Reduz o tamanho da imagem
                pil_image.thumbnail(IMAGE_MAX_SIZE)
                image_bytes = io.BytesIO()
                pil_image.save(image_bytes, format='JPEG', quality=85)
                image_blob = image_bytes.getvalue()
            except Exception as e:
                self.show_popup(
                    f"Erro ao carregar imagem para o banco de dados: {e}")
                return

        # 5. Inserção no Banco de Dados
        self.cursor.execute('''
            INSERT INTO tasks (task, client_name, client_address, service_type, labor_value, execution_date, completion_date, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (task, client_name, client_address, service_type, labor_value, execution_date, completion_date, image_blob))
        self.conn.commit()

        # Limpar Inputs e Preview
        self.task_input.text = ''
        self.client_input.text = ''
        self.address_input.text = ''
        self.service_type_input.text = ''
        self.labor_value_input.text = ''
        self.execution_date_input.text = ''
        self.completion_date_input.text = ''
        self.image_input.text = ''
        self.image_preview.texture = None  # Limpar preview

        self.load_tasks()  # Recarregar a lista

    def load_tasks(self):
        self.task_list.clear_widgets()
        # Mais recente primeiro
        self.cursor.execute('SELECT * FROM tasks ORDER BY id DESC')
        tasks_from_db = self.cursor.fetchall()

        for task_data in tasks_from_db:
            task_layout = BoxLayout(
                size_hint_y=None, height=80, padding=5, spacing=5)  # Aumenta a altura

            # Display image if available
            if task_data[8]:
                try:
                    image_data = io.BytesIO(task_data[8])
                    # Extensão 'jpg' é usada porque salvamos como JPEG
                    core_image = CoreImage(image_data, ext='jpg')
                    kivy_image = Image(
                        texture=core_image.texture, size_hint_x=None, width=70)
                    task_layout.add_widget(kivy_image)
                except Exception as e:
                    # Se houver erro ao exibir, printa o erro e adiciona um espaço vazio
                    print(
                        f"Erro ao exibir imagem da tarefa {task_data[0]}: {e}")
                    task_layout.add_widget(
                        Label(text='[Erro na Imagem]', size_hint_x=None, width=70))
            else:
                # Adiciona um widget de espaço vazio para manter o alinhamento
                task_layout.add_widget(
                    Label(text='[Sem Imagem]', size_hint_x=None, width=70))

            task_info = f"""
            **{task_data[1]}** (ID: {task_data[0]})
            Cliente: {task_data[2]} | Endereço: {task_data[3]}
            Serviço: {task_data[4]} | Valor: R$ {task_data[5]:.2f}
            Execução: {task_data[6] or 'N/A'} | Conclusão: {task_data[7] or 'N/A'}
            """

            # Use Label ou um RichText para melhor formatação
            task_label = Label(text=task_info, size_hint_x=1.0, text_size=(task_layout.width * 2, None),
                               halign='left', valign='middle', markup=True)  # Ativar markup

            delete_button = Button(text='Excluir', size_hint_x=None, width=80)
            # A função lambda garante que a ID correta seja passada no clique
            delete_button.bind(on_press=lambda instance,
                               task_id=task_data[0]: self.delete_task(task_id))

            task_layout.add_widget(task_label)
            task_layout.add_widget(delete_button)
            self.task_list.add_widget(task_layout)

    def delete_task(self, task_id):
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()
        self.load_tasks()

    def show_popup(self, text):
        popup = Popup(title='Aviso',
                      content=Label(text=text),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def on_stop(self):
        self.conn.close()


if __name__ == '__main__':
    TaskApp().run()
