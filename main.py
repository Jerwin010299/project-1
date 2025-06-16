import os
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
from kivy.graphics import Color, Rectangle

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


# Create a custom button class to handle image button behavior
class ImageButton(ButtonBehavior, KivyImage):
    pass

class CaptureScreen(Screen):
    def __init__(self, **kwargs):
        super(CaptureScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Set background color to light green
        with layout.canvas.before:
            Color(0.9, 1, 0.9, 1)  # Light green background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Language toggle buttons at the very top
        lang_box = BoxLayout(size_hint=(1, None), height=50, spacing=10, padding=10)
        
        # English button on left
        self.english_button = Button(text='English', size_hint=(0.4, 1))
        self.english_button.bind(on_press=lambda x: self.set_language('english'))
        lang_box.add_widget(self.english_button)
        
        # Tagalog button on right
        self.tagalog_button = Button(text='Tagalog', size_hint=(0.4, 1))
        self.tagalog_button.bind(on_press=lambda x: self.set_language('tagalog'))
        lang_box.add_widget(self.tagalog_button)
        
        layout.add_widget(lang_box)

        # Instruction label at the top (visible immediately)
        self.instruction_label = Label(
            text='Please take a photo or select an image of banana leaves to upload.',
            size_hint=(1, None),
            height=50,
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1),
            opacity=1
        )
        self.instruction_label.bind(size=self.instruction_label.setter('text_size'))
        layout.add_widget(self.instruction_label)

        self.image_display = KivyImage(size_hint=(1, 0.45))  # Slightly less height to fit instruction label
        layout.add_widget(self.image_display)

        # Camera widget
        self.camera = Camera(play=True, size_hint=(1, 0.45))  # Slightly less height to fit instruction label
        layout.add_widget(self.camera)

        # Buttons for uploading and capturing images
        self.button_layout = BoxLayout(size_hint=(1, None), height=50, spacing=10)
        
        self.upload_button = Button(text='Upload Image', size_hint=(0.3, 1), background_color=(0.2, 0.6, 0.8, 1))  # Blue
        # Bind upload button to upload_image method
        self.upload_button.bind(on_press=self.upload_image)
        self.button_layout.add_widget(self.upload_button)

        # Create an image button for capturing images
        self.capture_button = ImageButton(source='banana/camera_icon.png', size_hint=(0.3, 1))  # Use your camera icon image
        # Bind capture button to capture_image method
        self.capture_button.bind(on_press=self.capture_image)
        self.button_layout.add_widget(self.capture_button)

        layout.add_widget(self.button_layout)

        # Initialize current language state
        self.current_lang = 'english'

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def set_language(self, lang):
        self.current_lang = lang
        # Update button states
        self.english_button.background_color = (0.7, 0.7, 1, 1) if lang == 'english' else (0.9, 0.9, 0.9, 1)
        self.tagalog_button.background_color = (0.7, 0.7, 1, 1) if lang == 'tagalog' else (0.9, 0.9, 0.9, 1)

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
            self.camera.play = False  # Stop the camera when an image is uploaded
            self.update_buttons_after_image_selection()

    def capture_image(self, instance):
        # Capture the image from the camera
        if hasattr(self, 'camera') and self.camera:
            self.camera.export_to_png("captured_image.png")  # Save the captured image
            print("Captured image saved as captured_image.png")  # Debugging line
            self.image_path = "captured_image.png"
            self.image_display.source = self.image_path
            self.image_display.reload()
            self.camera.play = False  # Stop the camera after capturing
            self.update_buttons_after_image_selection()
        else:
            print("Camera is not available. Capture image action skipped.")

    def show_upload_instruction(self, instance):
        # Removed method as instruction is always visible
        pass

    def show_capture_instruction(self, instance):
        # Removed method as instruction is always visible
        pass

    def clear_instruction(self, instance):
        # Removed method as instruction is always visible
        pass

        # Perform the next action after OK pressed
        if hasattr(self, '_next_action'):
            action, inst = self._next_action
            if action == 'upload':
                self.upload_image(inst)
            elif action == 'capture':
                self.capture_image(inst)
            del self._next_action

    def update_buttons_after_image_selection(self):
        # Hide upload and capture buttons, show analyze button
        self.upload_button.disabled = True
        self.capture_button.disabled = True
        self.go_to_analyze()  # Directly switch to analyze screen

    def go_to_analyze(self):
        # Switch to the Analyze screen and trigger analysis automatically
        app = App.get_running_app()
        analyze_screen = app.root.get_screen('analyze')
        analyze_screen.image_path = self.image_path
        app.root.current = 'analyze'

class AnalyzeScreen(Screen):
    def __init__(self, **kwargs):
        super(AnalyzeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add an Image widget to display the captured image
        self.captured_image_display = KivyImage(size_hint=(1, 0.5))  # Display the captured image
        layout.add_widget(self.captured_image_display)

        # Create a Label to display the result
        self.result_label = Label(size_hint_y=None, markup=True, halign='left', valign='top', color=(0, 0, 0, 1), font_size=30)  # Black text
        self.result_label.bind(size=self._update_text_size)
        self.result_label.bind(texture_size=lambda instance, value: setattr(self.result_label, 'height', value[1]))

        # Create a container BoxLayout for the label with dynamic height
        self.result_label_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.result_label_container.bind(minimum_height=self.result_label_container.setter('height'))
        self.result_label_container.add_widget(self.result_label)
        
        # Wrap the result_label_container inside a ScrollView for scrolling with visible scrollbar
        self.result_scroll = ScrollView(size_hint_x=1, size_hint_y=1, height=200, do_scroll_y=True, bar_width=20)
        self.result_scroll.add_widget(self.result_label_container)

        # Add the ScrollView to the layout to make it visible
        layout.add_widget(self.result_scroll)

        # Create action buttons below
        button_box = BoxLayout(size_hint=(1, None), height=50, spacing=10, padding=10)
        
        # Back button
        self.back_button = Button(text='BACK', size_hint=(1, 1.5))
        self.back_button.bind(on_press=self.back_to_home)
        button_box.add_widget(self.back_button)
        
        layout.add_widget(button_box)

        self.add_widget(layout)

    def on_enter(self):
        # Set the captured image to the image widget when entering the Analyze screen
        if hasattr(self, 'image_path') and self.image_path:
            self.captured_image_display.source = self.image_path
            self.captured_image_display.reload()
        # Set current_lang from CaptureScreen
        app = App.get_running_app()
        capture_screen = app.root.get_screen('capture')
        self.current_lang = getattr(capture_screen, 'current_lang', 'english')
        # Automatically trigger analysis when entering the screen
        self.analyze_image(None)

    def _update_text_size(self, instance, value):
        instance.text_size = (instance.width, None)

    def analyze_image(self, instance):
        image_path = self.image_path  # Use the selected image path
        print(f"[DEBUG] Starting analysis of image at: {image_path}")
        try:
            # Verify image exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

            # Open and verify image
            print("[DEBUG] Opening image...")
            image = Image.open(image_path)
            if image is None:
                raise ValueError("Failed to open image")
            print("[DEBUG] Image opened successfully")

            # Check if image is in training dataset
            if not self.is_image_in_training_dataset(image_path):
                result_text = "This image is not in the train."
                self.result_label.text = result_text
                print(f"[RESULT] {result_text}")
                self.show_combined_popup(result_text, "")
                return

            # Process image
            print("[DEBUG] Processing image...")
            processed_image = self.process_image(image)
            if processed_image is None:
                raise ValueError("Image processing failed")

            # Debug print processed image stats
            print(f"[DEBUG] Processed image stats - min: {processed_image.min()}, max: {processed_image.max()}, mean: {processed_image.mean()}")

            # Load model if not loaded
            app = App.get_running_app()
            if app.model is None:
                print("[DEBUG] Loading model...")
                app.model = app.load_classification_model()
                if app.model is None:
                    raise ValueError("Failed to load model")

            # Make prediction with Keras model
            print("[DEBUG] Making prediction with Keras model...")
            prediction = app.model.predict(processed_image)
            print("[DEBUG] Prediction completed")
            print(f"[DEBUG] Raw prediction output: {prediction}")
            print(f"[DEBUG] Prediction shape: {prediction.shape}")

            # Check if ALLOWED_CLASSES length matches prediction output length
            if prediction.shape[1] != len(ALLOWED_CLASSES):
                warning_msg = f"Warning: Number of model output classes ({prediction.shape[1]}) does not match ALLOWED_CLASSES length ({len(ALLOWED_CLASSES)}). Please update ALLOWED_CLASSES to match the trained classes."
                print(f"[WARNING] {warning_msg}")
                app.show_popup("Class Mismatch Warning", warning_msg)

            # Calculate softmax if needed (Keras model output might be logits)
            import tensorflow as tf
            score = tf.nn.softmax(prediction).numpy()
            print(f"[DEBUG] Raw prediction output shape: {prediction.shape}")
            print(f"[DEBUG] Raw prediction output: {prediction}")
            print(f"[DEBUG] Softmax scores: {score}")
            for i, s in enumerate(score[0]):
                class_name = ALLOWED_CLASSES[i] if i < len(ALLOWED_CLASSES) else f"Class_{i}"
                print(f"[DEBUG] Class index {i} mapped to class '{class_name}' with score={s}")
            confidence = np.max(score) * 100
            predicted_index = np.argmax(score)
            predicted_class = ALLOWED_CLASSES[predicted_index] if predicted_index < len(ALLOWED_CLASSES) else "Unknown"
            print(f"[DEBUG] Predicted class index: {predicted_index}, class name: {predicted_class}")

            # Prepare result text
            extra_info = ""
            if predicted_class.lower() == "panama":
                extra_info = (" Panama disease, also known as Fusarium wilt, is a serious plant disease affecting banana plants, "
                              "caused by the soil-borne fungus Fusarium oxysporum f. sp. cubense.")
            elif predicted_class.lower() == "sigatoka":
                extra_info = (" Sigatoka disease refers to a group of fungal diseases that affect banana and plantain plants, primarily caused by two species of fungi: "
                              "Mycosphaerella fijiensis (causing Black Sigatoka) and Mycosphaerella musicola (causing Yellow Sigatoka).")
            elif predicted_class.lower() == "mealybug":
                extra_info = (" Mealybugs are small, soft-bodied insects that belong to the family Pseudococcidae. They are common plant pests that feed on the sap of plants, typically hiding in leaf joints, stems, and roots.")
            result_text = f"Detected Condition: {predicted_class.title()}.{extra_info}"
            self.result_label.text = result_text
            print(f"[RESULT] {result_text}")

            # Check confidence and prepare recommendations
            if confidence < CONFIDENCE_THRESHOLD * 100:
                recommendations = "Low confidence in diagnosis. Please try again with a clearer image."
            else:
                # Use language from CaptureScreen
                app = App.get_running_app()
                capture_screen = app.root.get_screen('capture')
                current_lang = getattr(capture_screen, 'current_lang', 'english')
                recommendations = TREATMENT_RECOMMENDATIONS.get(predicted_class, {}).get(current_lang, "No recommendations available.")

            # Show combined popup with results and recommendations
            self.show_combined_popup(result_text, recommendations)

        except Exception as e:
            error_message = f"Error during analysis: {str(e)}"
            print(error_message)
            app = App.get_running_app()
            app.show_popup("Analysis Error", error_message)

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
                        print(f"[DEBUG] Match found with training image: {train_image_path}")
                        return True
        print("[DEBUG] No match found in training or validation dataset")
        return False

    def back_to_capture(self, instance):
        # Switch back to the Capture screen
        app = App.get_running_app()
        app.root.current = 'capture'
        # Reset the camera and button states
        capture_screen = app.root.get_screen('capture')
        capture_screen.camera.play = True  # Restart the camera
        capture_screen.upload_button.disabled = False  # Enable upload button
        capture_screen.capture_button.disabled = False  # Enable capture button
        print("Returned to Capture Screen")  # Debugging line

    def process_image(self, image, img_height=180, img_width=180):
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image = image.resize((img_width, img_height))
        img_array = tf.keras.utils.img_to_array(image)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        return img_array

    def show_combined_popup(self, result_text, recommendations):
        # Create a BoxLayout for the content
        self.popup_content = BoxLayout(orientation='vertical', spacing=7)

        # Create a ScrollView for the result text with dynamic height
        self.scroll_view_result = ScrollView(size_hint=(1, None), size=(Window.width * 0.7, 150), bar_width=20)
        
        # Create a container for the label with dynamic height
        self.result_label_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.result_label_container.bind(minimum_height=self.result_label_container.setter('height'))
        
        # Create a label for the result
        self.result_label = Label(
            text=result_text,
            size_hint_y=None,
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1),
            text_size=(Window.width * 0.7, None),
            markup=True
        )
        self.result_label.bind(
            texture_size=lambda instance, value: setattr(self.result_label, 'height', value[1])
        )
        self.result_label_container.add_widget(self.result_label)
        self.scroll_view_result.add_widget(self.result_label_container)
        self.popup_content.add_widget(self.scroll_view_result)

        # Always create buttons for options, even if recommendations is empty
        self.button_box = BoxLayout(size_hint=(1, None), height=50, spacing=10)
        
        self.option1_btn = Button(
            text='Option 1',
            size_hint=(0.4, 1),
            background_color=(1, 1, 1, 1)  # default white
        )
        self.option1_btn.bind(on_press=lambda btn: self.show_combined_recommendations(btn))
        
        self.option2_btn = Button(
            text='Option 2',
            size_hint=(0.4, 1),
            background_color=(1, 1, 1, 1)  # default white
            #disabled=True  # Keep this button disabled for now
        )
        self.option2_btn.bind(on_press=lambda btn: self.show_combined_recommendations(btn))

        # Disable option buttons if result_text is "This image is not in the train."
        if result_text.strip() == "This image is not in the train.":
            self.option1_btn.disabled = True
            self.option2_btn.disabled = True
        else:
            self.option1_btn.disabled = False
            self.option2_btn.disabled = False

        self.button_box.add_widget(self.option1_btn)
        self.button_box.add_widget(self.option2_btn)
        self.popup_content.add_widget(self.button_box)

        # Create a back button
        self.back_button = Button(
            text='Back',
            size_hint=(0.3, None),
            height=50,
            pos_hint={'center_x': 0.5}
        )
        self.back_button.bind(on_press=lambda x: self.popup.dismiss())
        self.popup_content.add_widget(self.back_button)

        # Create the Popup with popup_content as content
        self.popup = Popup(
            title='Analysis Result',
            content=self.popup_content,
            size_hint=(0.8, 0.6)
        )
        self.popup.open()

    def back_to_home(self, instance):
        self.popup.dismiss()
        app = App.get_running_app()
        app.root.current = 'home'

    def show_treatment_options(self, recommendations):
        pass

    def show_combined_recommendations(self, clicked_button=None):
        recommendations = self.current_recommendations
        combined_recommendation = recommendations
        if ("Organic Treatment" in recommendations or "Organiko" in recommendations) and \
           ("Non-Organic Treatment" in recommendations or "Hindi Organiko" in recommendations):
            # For English
            if self.current_lang == 'english':
                organic_treatment = recommendations.split("Non-Organic")[0]
                non_organic_treatment = "Non-Organic Treatment" + recommendations.split("Non-Organic Treatment")[1]
            else:
                organic_treatment = recommendations.split("Hindi Organikong Paggamot")[0]
                non_organic_treatment = "Hindi Organikong Paggamot" + recommendations.split("Hindi Organikong Paggamot")[1]
            combined_recommendation = organic_treatment + "\n\n[b]────────────────────[/b]\n\n" + non_organic_treatment

        # Update the result label text instead of opening a new popup
        self.result_label.text = combined_recommendation

        # Update button colors to indicate which option is selected
        if clicked_button:
            # Reset both buttons to default color
            self.option1_btn.background_color = (1, 1, 1, 1)  # white
            self.option2_btn.background_color = (1, 1, 1, 1)  # white
            # Set clicked button to green
            clicked_button.background_color = (0, 1, 0, 1)  # green

    def show_recommendation(self, recommendation):
        # Create a new popup to show the recommendation
        content = BoxLayout(orientation='vertical', spacing=10)
        
        # Create a ScrollView with dynamic sizing
        scroll_view = ScrollView(size_hint=(1, 1), bar_width=20)
        
        # Create a container for the label with dynamic height
        label_container = BoxLayout(orientation='vertical', size_hint_y=None)
        label_container.bind(minimum_height=label_container.setter('height'))
        
        # Add separator line between treatments if it contains both types (check both English and Tagalog)
        if ("Organic Treatment" in recommendation or "Organikong Paggamot" in recommendation) and \
           ("Non-Organic Treatment" in recommendation or "Hindi Organikong Paggamot" in recommendation):
            recommendation = recommendation.replace("\n\n", "\n\n[b]────────────────────[/b]\n\n")
        
        # Create a Label for the recommendation with proper text sizing
        rec_label = Label(
            text=recommendation,
            size_hint_y=None,
            halign='left',
            valign='top',
            text_size=(Window.width * 0.7, None),
            markup=True
        )
        rec_label.bind(
            texture_size=lambda instance, value: setattr(rec_label, 'height', value[1])
        )
        
        label_container.add_widget(rec_label)
        scroll_view.add_widget(label_container)
        content.add_widget(scroll_view)
        
        # Add back button
        back_button = Button(
            text='Back',
            size_hint=(0.3, None),
            height=50,
            pos_hint={'center_x': 0.5}
        )
        back_button.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(back_button)
        
        popup = Popup(
            title='Recommendation',
            content=content,
            size_hint=(0.8, 0.8)
        )
        popup.open()

from kivy.uix.anchorlayout import AnchorLayout

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = AnchorLayout(anchor_x='center', anchor_y='center', padding=50)

        start_button = Button(text='Start', size_hint=(0.2, 0.05), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        start_button.bind(on_press=self.start_app)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def start_app(self, instance):
        app = App.get_running_app()
        app.root.current = 'capture'


class BananaLeafDiseaseScannerApp(App):
    def build(self):
        self.model = self.load_classification_model()
        sm = ScreenManager()

        # Add screens to the ScreenManager
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CaptureScreen(name='capture'))
        sm.add_widget(AnalyzeScreen(name='analyze'))

        sm.current = 'home'  # Set initial screen to home

        return sm

    def load_classification_model(self):
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model('newImage_classify.keras')
            print("Keras model loaded successfully.")
            return model
        except Exception as e:
            error_msg = f"Error loading model: {str(e)}\n\nPlease ensure:\n1. Image_classify.keras exists\n2. TensorFlow is installed"
            self.show_popup("Model Error", error_msg)
            import traceback
            traceback.print_exc()
            return None

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 5))
        popup.open()

if __name__ == '__main__':
    BananaLeafDiseaseScannerApp().run()
