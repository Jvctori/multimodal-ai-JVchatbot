import requests
import json
from PIL import Image
import io
import os
import hashlib
from datetime import datetime
from googletrans import Translator

class AiServices:
    def __init__(self, api_token) -> None:
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        self.translator = Translator()
        
    def hash_img(self, prompt: str, modelo_imagem: str) -> str:
        timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        hash_input = f"{prompt}{modelo_imagem}{timestamp}".encode("utf-8")
        filename = hashlib.md5(hash_input).hexdigest()
        return f"{filename}.png"
        
    def generate_img(self, prompt: str, modelo_imagem: str) -> str:
        try:
            detect_src_lang = self.translator.detect(prompt)

            if detect_src_lang == "en":
                prompt_en = prompt
            else:
                prompt_en = self.translate_prompt(prompt, tgt_lang="en")

            api_url = f"https://api-inference.huggingface.co/models/{modelo_imagem}"

            response = requests.post(
                api_url,
                headers=self.headers,
                json={"inputs": prompt_en}
            )
            
            response.raise_for_status()
            
            if 'image' in response.headers.get('content-type', ''):
                img = Image.open(io.BytesIO(response.content))
                img_name = self.hash_img(prompt_en, modelo_imagem)
                img_dir = os.path.join("static", "generated_images")
                os.makedirs(img_dir, exist_ok=True)
                img_path = os.path.join(img_dir, img_name)
                img.save(img_path)
                return img_path
            else:
                error_data = response.json()
                raise Exception(f"API Error: {error_data}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")
        
    def translate_prompt(self, prompt: str, tgt_lang: str ="pt", force_translation: bool = True) -> str:
        if not force_translation:
            return prompt
        detected_lang = self.translator.detect(prompt).lang
        translation = self.translator.translate(
            prompt, src=detected_lang, dest=tgt_lang
        )
        return translation.text
        
    def code_generator(self, prompt):
        try:
            api_url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-32B-Instruct/v1/chat/completions"
            
            payload = {
                "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 500,
                "stream": True
            }
            
            response = requests.post(
                api_url,
                headers=self.headers,
                json=payload,
                stream=True
            )
            
            response.raise_for_status()
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            line = line[6:]
                        
                        if line.strip() == '[DONE]':
                            break
                            
                        data = json.loads(line)
                        if "choices" in data and len(data["choices"]) > 0:
                            content = data["choices"][0]["delta"].get("content", "")
                            if content:
                                full_response += content

                    except json.JSONDecodeError:
                        continue
                        
            return full_response

        except Exception as e:
            return f"Generation failed: {str(e)}"

            
    def summarize_text(self, prompt: str, force_translation: bool =True) -> str:
        try:
            api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
            
            if not force_translation:
                try:
                    response = requests.post(
                        api_url,
                        headers=self.headers,
                        json={"inputs": prompt}
                    )
                    
                    response.raise_for_status()
                    result = response.json()
                    
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get("summary_text", "")
                    else:
                        raise ValueError("Unexpected response format")
                        
                except requests.exceptions.RequestException as e:
                    raise ValueError(f"Request failed: {str(e)}")
                except json.JSONDecodeError:
                    raise ValueError(f"Invalid JSON response: {response.text}")
                except Exception as e:
                    raise ValueError(f"Summarization failed: {str(e)}")
                    
            text_en = self.translator.translate(prompt, dest="en").text
            response = requests.post(
                api_url,
                headers=self.headers,
                json={"inputs": text_en}
            )
            
            response.raise_for_status()
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                summary = result[0].get("summary_text", "")
                summ_pt = self.translate_prompt(summary, tgt_lang="pt")
                return summ_pt
            else:
                raise ValueError("Unexpected response format")
                
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")
