from logging import exception
from huggingface_hub import InferenceClient
from PIL import Image
import os
import hashlib
from datetime import datetime
from googletrans import Translator

class AiServices:
    
    def __init__(self, api_token):
        self.api_token = api_token
        self.InferenceClient = InferenceClient(token=api_token)
        self.translator = Translator()

    def hash_img(self, prompt, modelo_imagem):
        timestamp = datetime.now().strftime('%d%m%Y_%H%M%S')
        hash_input = f'{prompt}{modelo_imagem}{timestamp}'.encode('utf-8')
        filename = hashlib.md5(hash_input).hexdigest()
        return f"{filename}.png"

    def generate_img(self,prompt, modelo_imagem):

        prompt_en = self.translate_prompt(prompt, tgt_lang='en')
        client = InferenceClient(modelo_imagem, token=self.api_token)

        print(f"\n=== DEBUG INFORMAÇÃO DA GERAÇÃO DE IMAGEM ===")
        print(f"Modelo sendo usado: {modelo_imagem}")
        print(f"Prompt recebido: {prompt}")
        print(f"Prompt em inglês: {prompt_en}")
        print("============================================\n")

        img = client.text_to_image(prompt_en)
        img_name = self.hash_img(prompt_en,modelo_imagem)
        img_dir = os.path.join('static','generated_images')
        os.makedirs(img_dir, exist_ok=True)
        img_path = os.path.join(img_dir, img_name)
        img.save(img_path)

        return img_path
        
    def translate_prompt(self, prompt, tgt_lang='pt', force_translation=True):
        if not force_translation:
            return prompt 

        detected_lang = self.translator.detect(prompt).lang 
        translation = self.translator.translate(prompt, src=detected_lang, dest=tgt_lang)  
        return translation.text

    def code_generator(self, prompt):
        try:
            client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.3",token=self.api_token)
            text = client.text_generation(prompt) 
            return text
        except Exception as e:
                return str(e)

    def summarize_text(self, prompt, force_translation=True):
        client = InferenceClient("facebook/bart-large-cnn", token=self.api_token)
        
        if not force_translation:
            try:
                response = client.summarization(prompt)
                if 'summary_text' in response:
                    return response.summary_text
                else:
                    raise ValueError("Error: 'summary_text' não esta presente em response")
            except Exception as e:
                raise ValueError(f"Error: {str(e)}")
            
        try:
            text_en = self.translator.translate(prompt, dest='en').text 
        except Exception as e:
            raise ValueError(f"Error ao tentar traduzir texto para en : {str(e)}")
        
        try:
            response = client.summarization(text_en)
            summary = response['summary_text']
        except Exception as e:
            raise ValueError(f'Error ao acessar "summary_text" na api: {str(e)}')

        try:
            summ_pt = self.translate_prompt(summary, tgt_lang='pt')
        except Exception as e:
            raise ValueError(f'Error ao gerar resumo: {str(e)}')

        return summ_pt
        
               
        

