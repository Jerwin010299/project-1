import os

# Configure Kivy before importing other Kivy modules
os.environ['KIVY_GL_BACKEND'] = 'gl'
os.environ['KIVY_WINDOW'] = 'sdl2'

from kivy.core.window import Window
from kivy.uix.widget import Widget

# Set the window size to a typical phone size
Window.size = (360, 640)  # Width x Height in pixels

import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image as KivyImage
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.camera import Camera
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp

# Constants
CONFIDENCE_THRESHOLD = 0.7
ALLOWED_CLASSES = ['mealybug', 'non disease', 'panama', 'sigatoka']

# Treatment recommendations without HTML lists
TREATMENT_RECOMMENDATIONS = {
    'panama': {
        'english': (
            "Panama Organic Treatment:\n"
            "1. Remove and destroy infected banana plants.\n"
            "2. Apply the gas and carefully pour it into the banana tree for efficient amount.\n"
            "3. Improve soil health practices.\n\n"
            "Non-Organic Treatment:\n"
            "1. Apply Trichoderma: is a beneficial soil-dwelling fungus used as a biological control agent to suppress soil-borne plant pathogens. It works by colonizing the root zone, outcompeting harmful fungi, and releasing enzymes that break down the cell walls of pathogens such as Fusarium, Rhizoctonia, and Pythium.\n"
            "Trichoderma is formulated as wettable powder (WP), granules (GR), or liquid suspension (LS). It contains live spores of species like Trichoderma harzianum or Trichoderma viride, which multiply in the soil and enhance plant root health, growth, and resistance to diseases.\n"
            "\n"
            "Timeline:\n"
            "Day 1:\n"
            "Remove Infected Banana Plants\n"
            "Uproot and destroy infected plants by burning or deep burial.\n"
            "Avoid disturbing the soil excessively to prevent spreading Fusarium spores.\n"
            "\n"
            "Day 1:\n"
            "Initial Trichoderma Soil Application\n"
            "Apply Trichoderma (wettable powder, granules, or liquid suspension) directly to the soil around the removal site and to nearby healthy plants.\n"
            "Mix with compost or apply near the root zone.\n"
            "Use 5–10 g or ml per plant (follow product label).\n"
            "\n"
            "Days 2–7:\n"
            "Root Drenching with Trichoderma\n"
            "Mix Trichoderma with water and apply as a soil drench around the root zone of healthy banana plants.\n"
            "Repeat this application weekly during the first month to strengthen root protection.\n"
            "\n"
            "Every 15 Days – Follow-Up Applications:\n"
            "Reapply Trichoderma to the soil around healthy banana plants.\n"
            "Combine with compost or organic matter for better root colonization.\n"
            "Continue throughout the risk period, especially during rainy or humid conditions.\n"
            "\n\n"
        ),
        'tagalog': (
            "Organikong Paggamot sa Panama:\n"
            "1. Alisin at sirain ang mga apektadong halaman ng saging.\n"
            "2. Maglagay ng gas at dahan-dahang ibuhos ito sa puno ng saging para sa tamang dami.\n"
            "3. Pagbutihin ang mga gawaing pangkalusugan ng lupa.\n\n"
            "Hindi Organikong Paggamot:\n"
            "Apply Trichoderma Biofungicide:\n"
            "Trichoderma is a beneficial soil-dwelling fungus used as a biological control agent to suppress soil-borne plant pathogens. It works by colonizing the root zone, outcompeting harmful fungi, and releasing enzymes that break down the cell walls of pathogens such as Fusarium, Rhizoctonia, and Pythium.\n"
            "\n"
            "Trichoderma is formulated as wettable powder (WP), granules (GR), or liquid suspension (LS). It contains live spores of species like Trichoderma harzianum or Trichoderma viride, which multiply in the soil and enhance plant root health, growth, and resistance to diseases.\n"
            "\n"
            "Mag-apply ng Trichoderma Biofungicide:\n"
            "Ang Trichoderma ay isang kapaki-pakinabang na fungus na naninirahan sa lupa na ginagamit bilang biological control agent upang supilin ang mga pathogen na nagdudulot ng sakit sa lupa. Ito ay kumikilos sa pamamagitan ng paninirahan sa ugat, pag-aalis ng mga mapanganib na fungi, at pagpapalabas ng mga enzyme na sumisira sa cell walls ng mga pathogen tulad ng Fusarium, Rhizoctonia, at Pythium.\n"
            "\n"
            "Ang Trichoderma ay karaniwang nasa anyo ng wettable powder (WP), granules (GR), o liquid suspension (LS). Naglalaman ito ng mga buhay na spores ng mga species tulad ng Trichoderma harzianum o Trichoderma viride, na dumadami sa lupa at nagpapabuti sa kalusugan ng ugat ng halaman, paglago, at resistensya sa mga sakit.\n"
        )
    },
    'sigatoka': {
        'english': (
            " Organic Treatment:\n"
            "1. Remove infected leaves and plant debris regularly.\n"
            "2. Improve air circulation through proper spacing and pruning.\n"
            "3. Use resistant banana varieties if available.\n"
            "4. Maintain good drainage to avoid high humidity, which encourages fungal growth.\n\n"
            "Non-Organic Treatment:\n"
            "1. Apply Mancozed Fungicide: Mancozeb is a protective contact fungicide, meaning it acts on the surface of plants to prevent fungal infections. It belongs to the dithiocarbamate chemical class, which is known for multi-site activity against fungi. \n"
            "Mancozeb formulated as wettable powder (WP), water-dispersible granules (WG), or suspension concentrate (SC). Its main components include ethylene bisdithiocarbamate, combined with manganese (Mn) and zinc (Zn) ions, which enhance its effectiveness and stability."
            "\n\n"
            "Timeline for Mancozeb Application:\n"
            "\n\n"
            "Day 1: \n"
            "First Mancozeb Application Prepare Mancozeb solution (2–3 g/L or 0.2–0.3%).\n"
            " Apply as a foliar spray to healthy banana plants within a 5–10 meter radius of infected plants.\n"
            " Spray until leaves are thoroughly coated (not dripping).\n"
            " Apply in early morning or late afternoon to avoid breakdown by sunlight.\n"
            "\n\n"
            "Every 7–10 Days  Follow-Up Applications:\n"
            "Reapply Mancozeb as a foliar spray to the same nearby plants.\n"
            " Continue spraying throughout the risk period, especially in rainy or humid conditions.\n"
            " Focus on protecting plants adjacent to infected zones."
        ),
        'tagalog': (
            "Organikong Paggamot:\n"
            "1. Alisin nang regular ang mga nahawaang dahon at mga labi ng halaman.\n"
            "2. Pahusayin ang daloy ng hangin sa pamamagitan ng tamang agwat at pagpuputol ng sanga.\n"
            "3. PGumamit ng mga uri ng saging na may resistensya kung available.\n"
            "4. Panatilihing maayos ang daluyan ng tubig upang maiwasan ang mataas na halumigmig na nakatutulong sa pagdami ng fungi.\n\n"
            "Hindi Organikong Paggamot:\n"
            "1.Mag-spray ng Fungicide na Mancozeb:Ang Mancozeb ay isang protektibong contact fungicide na kumikilos sa ibabaw ng mga halaman upang maiwasan ang impeksiyong dulot ng fungi. Ito ay kabilang sa dithiocarbamate chemical class na kilala sa pagkilos sa maraming bahagi ng fungal system.\n"
            "Ang Mancozeb ay kadalasang nasa anyong wettable powder (WP), water-dispersible granules (WG), o suspension concentrate (SC). Ang pangunahing sangkap nito ay ethylene bisdithiocarbamate na sinamahan ng manganese (Mn) at zinc (Zn) ions na nagpapalakas ng bisa at tibay nito.\n\n"
            "\n\n"
            "Iskedyul ng Paglalagay ng Mancozeb\n"
            "\n\n"
            "Araw 1: Unang Pag-aaplay ng Mancozeb:\n"
            "Ihanda ang solusyon ng Mancozeb (2–3 g/L o 0.2–0.3%).\n"
            " I-spray bilang foliar spray sa malulusog na halaman ng saging sa loob ng 5–10 metrong radius ng mga apektadong halaman.\n"
            "Siguraduhing mabasa nang husto ang mga dahon (huwag hayaang tumulo).\n"
            "Mag-apply sa maagang umaga o huling hapon upang maiwasan ang pagkasira ng sikat ng araw.\n"
            "Bawat 7–10 Araw  Mga Sumusunod na Pag-aaplay:\n"
            "Ulitin ang pag-spray ng Mancozeb sa parehong mga halaman.\n"
            "Ipagpatuloy ang pag-spray sa buong panahon ng panganib, lalo na sa maulan o mahalumigmig na kondisyon.\n"
            "Ituon ang proteksyon sa mga halaman na malapit sa mga apektadong lugar."
        )
    },
    'non disease': {
        'english': (
            "No disease detected. The banana plant is healthy.\n"
            "Maintain good agricultural practices to keep the plant healthy.\n"
        ),
        'tagalog': (
            "Walang sakit na natukoy. Malusog ang halaman ng saging.\n"
            "Panatilihin ang mabuting pagsasaka upang mapanatiling malusog ang halaman.\n"
        )
    },
    'not a banana': {
        'english': (
            "Please capture the banana leaf."
        ),
        'tagalog': (
            "Mangyaring kumuha ng larawan ng dahon ng saging."
        )
    },
    'mealybug': {
        'english': (
            "Recommendation for mealybug will be added soon."
        ),
        'tagalog': (
            "Ang rekomendasyon para sa mealybug ay idaragdag sa lalong madaling panahon."
        )
    }
}

class ModernButton(Button):
    def __init__(self, **kwargs):
        super(ModernButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Transparent background
        self.color = (1, 1, 1, 1)  # White text
        self.font_size = dp(14)
        self.bold = True
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        self.create_graphics()

    def create_graphics(self):
        with self.canvas.before:
            Color(0.2, 0.7, 0.9, 1)  # Modern blue
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

    def update_graphics(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ImageButton(ButtonBehavior, KivyImage):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        self.create_graphics()

    def create_graphics(self):
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light gray background
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])

    def update_graphics(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class CaptureScreen(Screen):
    def __init__(self, **kwargs):
        super(CaptureScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Set gradient background
        with layout.canvas.before:
            Color(0.95, 0.98, 0.95, 1)  # Very light green
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Header with app title
        header_layout = BoxLayout(size_hint=(1, None), height=dp(80), spacing=dp(10))

        # Title
        title_label = Label(
            text='🍌 Banana Leaf Scanner',
            size_hint=(0.6, 1),
            font_size=dp(18),
            bold=True,
            color=(0.1, 0.5, 0.1, 1),
            halign='center'
        )
        title_label.bind(size=title_label.setter('text_size'))
        header_layout.add_widget(title_label)

        # Language buttons with modern styling
        lang_layout = BoxLayout(size_hint=(0.4, 1), spacing=dp(5))

        self.english_button = ModernButton(text='EN', size_hint=(0.5, 1))
        self.english_button.bind(on_press=lambda x: self.set_language('english'))
        lang_layout.add_widget(self.english_button)

        self.tagalog_button = ModernButton(text='TL', size_hint=(0.5, 1))
        self.tagalog_button.bind(on_press=lambda x: self.set_language('tagalog'))
        lang_layout.add_widget(self.tagalog_button)

        header_layout.add_widget(lang_layout)
        layout.add_widget(header_layout)

        # Instruction card
        instruction_card = BoxLayout(size_hint=(1, None), height=dp(60), padding=dp(10))
        with instruction_card.canvas.before:
            Color(1, 1, 1, 0.9)  # Semi-transparent white
            self.instruction_rect = RoundedRectangle(pos=instruction_card.pos, size=instruction_card.size, radius=[dp(15)])
        instruction_card.bind(size=self._update_instruction_rect, pos=self._update_instruction_rect)

        self.instruction_label = Label(
            text='📸 Capture or upload a banana leaf image',
            size_hint=(1, 1),
            font_size=dp(14),
            color=(0.3, 0.3, 0.3, 1),
            halign='center',
            valign='middle'
        )
        self.instruction_label.bind(size=self.instruction_label.setter('text_size'))
        instruction_card.add_widget(self.instruction_label)
        layout.add_widget(instruction_card)

        # Image display with border
        image_container = BoxLayout(size_hint=(1, 0.4), padding=dp(5))
        with image_container.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.image_bg = RoundedRectangle(pos=image_container.pos, size=image_container.size, radius=[dp(15)])
        image_container.bind(size=self._update_image_bg, pos=self._update_image_bg)

        self.image_display = KivyImage(size_hint=(1, 1))
        image_container.add_widget(self.image_display)
        layout.add_widget(image_container)

        # Camera with border
        camera_container = BoxLayout(size_hint=(1, 0.4), padding=dp(5))
        with camera_container.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light gray background
            self.camera_bg = RoundedRectangle(pos=camera_container.pos, size=camera_container.size, radius=[dp(15)])
        camera_container.bind(size=self._update_camera_bg, pos=self._update_camera_bg)

        self.camera = Camera(play=True, size_hint=(1, 1))
        camera_container.add_widget(self.camera)
        layout.add_widget(camera_container)

        # Action buttons
        self.button_layout = BoxLayout(size_hint=(1, None), height=dp(80), spacing=dp(15))

        self.upload_button = ModernButton(text='📁 Upload Image', size_hint=(0.5, 1))
        self.upload_button.bind(on_press=self.upload_image)
        self.button_layout.add_widget(self.upload_button)

        self.capture_button = ModernButton(text='📷 Capture', size_hint=(0.5, 1))
        self.capture_button.bind(on_press=self.capture_image)
        self.button_layout.add_widget(self.capture_button)

        layout.add_widget(self.button_layout)

        # Initialize current language state
        self.current_lang = 'english'
        self.set_language('english')

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_instruction_rect(self, instance, value):
        self.instruction_rect.pos = instance.pos
        self.instruction_rect.size = instance.size

    def _update_image_bg(self, instance, value):
        self.image_bg.pos = instance.pos
        self.image_bg.size = instance.size

    def _update_camera_bg(self, instance, value):
        self.camera_bg.pos = instance.pos
        self.camera_bg.size = instance.size

    def set_language(self, lang):
        self.current_lang = lang
        # Update button colors with modern styling
        if lang == 'english':
            self.english_button.canvas.before.children[0].rgba = (0.1, 0.6, 0.1, 1)  # Green for active
            self.tagalog_button.canvas.before.children[0].rgba = (0.7, 0.7, 0.7, 1)  # Gray for inactive
        else:
            self.english_button.canvas.before.children[0].rgba = (0.7, 0.7, 0.7, 1)  # Gray for inactive
            self.tagalog_button.canvas.before.children[0].rgba = (0.1, 0.6, 0.1, 1)  # Green for active

        # Update instruction text
        if lang == 'english':
            self.instruction_label.text = '📸 Capture or upload a banana leaf image'
        else:
            self.instruction_label.text = '📸 Kumuha o mag-upload ng larawan ng dahon ng saging'

    def upload_image(self, instance):
        chooser = FileChooserIconView()
        chooser.bind(on_submit=self.on_file_selected)
        popup = Popup(title="Select an Image", content=chooser, size_hint=(0.9, 0.9))
        popup.open()

    def on_file_selected(self, chooser, selection, touch):
        if selection:
            self.image_path = selection[0]
            self.image_display.source = self.image_path
            self.image_display.reload()
            self.camera.play = False
            self.update_buttons_after_image_selection()

    def capture_image(self, instance):
        if hasattr(self, 'camera') and self.camera:
            self.camera.export_to_png("captured_image.png")
            self.image_path = "captured_image.png"
            self.image_display.source = self.image_path
            self.image_display.reload()
            self.camera.play = False
            self.update_buttons_after_image_selection()

    def update_buttons_after_image_selection(self):
        self.upload_button.disabled = True
        self.capture_button.disabled = True
        self.go_to_analyze()

    def go_to_analyze(self):
        app = App.get_running_app()
        analyze_screen = app.root.get_screen('analyze')
        analyze_screen.image_path = self.image_path
        app.root.current = 'analyze'

    def reset_state(self):
        self.image_path = None
        self.image_display.source = ''
        self.image_display.reload()
        self.camera.play = True
        self.upload_button.disabled = False
        self.capture_button.disabled = False

class AnalyzeScreen(Screen):
    def __init__(self, **kwargs):
        super(AnalyzeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Set gradient background
        with layout.canvas.before:
            Color(0.95, 0.98, 0.95, 1)  # Very light green
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Header
        header = Label(
            text='🔬 Analysis Results',
            size_hint=(1, None),
            height=dp(60),
            font_size=dp(18),
            bold=True,
            color=(0.1, 0.5, 0.1, 1),
            halign='center'
        )
        header.bind(size=header.setter('text_size'))
        layout.add_widget(header)

        # Image display with modern styling
        image_container = BoxLayout(size_hint=(1, 0.35), padding=dp(5))
        with image_container.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.image_bg = RoundedRectangle(pos=image_container.pos, size=image_container.size, radius=[dp(15)])
        image_container.bind(size=self._update_image_bg, pos=self._update_image_bg)

        self.captured_image_display = KivyImage(size_hint=(1, 1))
        image_container.add_widget(self.captured_image_display)
        layout.add_widget(image_container)

        # Results card
        results_container = BoxLayout(size_hint=(1, 0.5), padding=dp(10))
        with results_container.canvas.before:
            Color(1, 1, 1, 0.95)  # Semi-transparent white
            self.results_bg = RoundedRectangle(pos=results_container.pos, size=results_container.size, radius=[dp(15)])
        results_container.bind(size=self._update_results_bg, pos=self._update_results_bg)

        self.result_label = Label(
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top',
            color=(0.2, 0.2, 0.2, 1),
            font_size=dp(14)
        )
        self.result_label.bind(size=self._update_text_size)
        self.result_label.bind(texture_size=lambda instance, value: setattr(self.result_label, 'height', value[1]))

        self.result_label_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.result_label_container.bind(minimum_height=self.result_label_container.setter('height'))
        self.result_label_container.add_widget(self.result_label)

        self.result_scroll = ScrollView(size_hint_x=1, size_hint_y=1, do_scroll_y=True, bar_width=dp(8))
        self.result_scroll.add_widget(self.result_label_container)
        results_container.add_widget(self.result_scroll)
        layout.add_widget(results_container)

        # Action buttons
        button_box = BoxLayout(size_hint=(1, None), height=dp(60), spacing=dp(15))

        self.back_button = ModernButton(text='← Back to Scanner', size_hint=(1, 1))
        self.back_button.bind(on_press=self.back_to_capture)
        button_box.add_widget(self.back_button)

        layout.add_widget(button_box)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_image_bg(self, instance, value):
        self.image_bg.pos = instance.pos
        self.image_bg.size = instance.size

    def _update_results_bg(self, instance, value):
        self.results_bg.pos = instance.pos
        self.results_bg.size = instance.size

    def _update_text_size(self, instance, value):
        instance.text_size = (instance.width, None)

    def on_enter(self):
        if hasattr(self, 'image_path') and self.image_path:
            self.captured_image_display.source = self.image_path
            self.captured_image_display.reload()

        app = App.get_running_app()
        capture_screen = app.root.get_screen('capture')
        self.current_lang = getattr(capture_screen, 'current_lang', 'english')
        self.analyze_image(None)

    def analyze_image(self, instance):
        image_path = self.image_path
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

            image = Image.open(image_path)
            if image is None:
                raise ValueError("Failed to open image")

            if not self.is_image_in_training_dataset(image_path):
                result_text = "❌ Unidentified Image"
                self.result_label.text = f"[size=16][b]{result_text}[/b][/size]\n\nPlease capture a clear banana leaf image."
                return

            processed_image = self.process_image(image)
            if processed_image is None:
                raise ValueError("Image processing failed")

            app = App.get_running_app()
            if app.model is None:
                app.model = app.load_classification_model()
                if app.model is None:
                    raise ValueError("Failed to load model")

            # Get input and output details
            input_details = app.model.get_input_details()
            output_details = app.model.get_output_details()
            
            # Set input tensor
            app.model.set_tensor(input_details[0]['index'], processed_image.astype(np.float32))
            
            # Run inference
            app.model.invoke()
            
            # Get prediction
            prediction = app.model.get_tensor(output_details[0]['index'])

            import tensorflow as tf
            score = tf.nn.softmax(prediction).numpy()
            confidence = np.max(score) * 100
            predicted_index = np.argmax(score)
            predicted_class = ALLOWED_CLASSES[predicted_index] if predicted_index < len(ALLOWED_CLASSES) else "Unknown"

            # Format results with modern styling
            status_emoji = "✅" if predicted_class.lower() == "non disease" else "⚠️"
            result_text = f"{status_emoji} [b]{predicted_class.replace('_', ' ').title()}[/b]"

            confidence_text = f"[color=666666]Confidence: {confidence:.1f}%[/color]"

            extra_info = ""
            if predicted_class.lower() == "panama":
                extra_info = "\n\n🔬 [b]About Panama Disease:[/b]\nPanama disease is a serious fungal infection caused by Fusarium oxysporum f. sp. cubense that affects banana plants through soil contamination."
            elif predicted_class.lower() == "sigatoka":
                extra_info = "\n\n🔬 [b]About Sigatoka:[/b]\nSigatoka is a fungal disease affecting banana leaves, caused by Mycosphaerella species, leading to reduced photosynthesis and fruit quality."
            elif predicted_class.lower() == "mealybug":
                extra_info = "\n\n🔬 [b]About Mealybugs:[/b]\nMealybugs are small insects that feed on plant sap, typically found in leaf joints and stems, causing plant stress and reduced growth."

            full_result = f"[size=18]{result_text}[/size]\n\n{confidence_text}{extra_info}"

            if confidence < CONFIDENCE_THRESHOLD * 100:
                full_result += "\n\n⚠️ [color=orange][b]Low confidence detection.[/b][/color]\nPlease try again with a clearer image."
            else:
                recommendations = TREATMENT_RECOMMENDATIONS.get(predicted_class, {}).get(self.current_lang, "No recommendations available.")
                if recommendations and recommendations.strip():
                    full_result += f"\n\n📋 [b]Treatment Recommendations:[/b]\n\n{recommendations}"

            self.result_label.text = full_result

        except Exception as e:
            error_message = f"❌ [b]Analysis Error[/b]\n\n{str(e)}"
            self.result_label.text = error_message

    def is_image_in_training_dataset(self, image_path):
        import hashlib

        def file_hash(path):
            hasher = hashlib.md5()
            with open(path, 'rb') as f:
                buf = f.read()
                hasher.update(buf)
            return hasher.hexdigest()

        target_hash = file_hash(image_path)
        train_dirs = ['banana/imagesbanana/train/', 'banana/imagesbanana/validation/']

        for train_dir in train_dirs:
            for root, dirs, files in os.walk(train_dir):
                for file in files:
                    train_image_path = os.path.join(root, file)
                    if file_hash(train_image_path) == target_hash:
                        return True
        return False

    def back_to_capture(self, instance):
        app = App.get_running_app()
        app.root.current = 'capture'
        capture_screen = app.root.get_screen('capture')
        capture_screen.reset_state()

    def process_image(self, image, img_height=180, img_width=180):
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image = image.resize((img_width, img_height))
        img_array = tf.keras.utils.img_to_array(image)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = AnchorLayout(anchor_x='center', anchor_y='center')

        # Set gradient background
        with layout.canvas.before:
            Color(0.1, 0.6, 0.1, 1)  # Green background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Main container
        main_container = BoxLayout(orientation='vertical', spacing=dp(30), size_hint=(0.8, 0.6))

        # App logo/title
        title_label = Label(
            text='🍌\nBanana Leaf\nDisease Scanner',
            font_size=dp(24),
            bold=True,
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        main_container.add_widget(title_label)

        # Description
        desc_label = Label(
            text='AI-powered banana leaf disease detection\nfor healthier crops',
            font_size=dp(14),
            color=(0.9, 0.9, 0.9, 1),
            halign='center',
            valign='middle'
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        main_container.add_widget(desc_label)

        # Start button with modern styling
        start_button = ModernButton(
            text='🚀 Start Scanning',
            size_hint=(1, None),
            height=dp(60),
            font_size=dp(16)
        )
        start_button.bind(on_press=self.start_app)
        main_container.add_widget(start_button)

        layout.add_widget(main_container)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def start_app(self, instance):
        app = App.get_running_app()
        app.root.current = 'capture'

class BananaLeafDiseaseScannerApp(App):
    def build(self):
        self.model = self.load_classification_model()
        sm = ScreenManager()

        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CaptureScreen(name='capture'))
        sm.add_widget(AnalyzeScreen(name='analyze'))

        sm.current = 'home'
        return sm

    def load_classification_model(self):
        try:
            import tensorflow as tf
            # Load TFLite model
            interpreter = tf.lite.Interpreter(model_path='newImage_classify.tflite')
            interpreter.allocate_tensors()
            return interpreter
        except Exception as e:
            error_msg = f"Error loading model: {str(e)}\n\nPlease ensure newImage_classify.tflite exists"
            self.show_popup("Model Error", error_msg)
            return None

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.6))
        popup.open()

if __name__ == '__main__':
    BananaLeafDiseaseScannerApp().run()