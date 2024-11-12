from .ai_services import AiServices
from typing import Optional, Tuple 
import os


class PromptProcessor:
    
    def __init__(self, ai_services: AiServices) -> None:

        self.ai_services = ai_services
        self.valid_commands = ["$imagem", "$codigo", "$resumo"]

    def _detect_command(self, unified_prompt: str) -> Optional[str]:
    
        if unified_prompt.startswith('$traduzir.') or unified_prompt.startswith("$traduzir"):

            return '$traduzir'

        for command in self.valid_commands:

            if unified_prompt.startswith(command):

                return command

        return None

    def _handle_translation(self, complete_prompt: str) -> Tuple[str,str]:
        
        try:
            if complete_prompt.startswith('$traduzir.'):

                first_jump = complete_prompt.find(' ')

                if first_jump == -1:

                    raise ValueError ('Error: formato inválido. Use $traduzir.XX texto')


                command_parts = complete_prompt[:first_jump].split('.')

                lang = command_parts[1]
                text = complete_prompt[first_jump+1:].strip()
                print(f'Idioma detectado: {lang}')
                print(f'Texto a ser traduzido: {text}')
                

                if not text:

                    raise ValueError ('Error: texto para tradução não fornecido')

                translation = self.ai_services.translate_prompt(text, tgt_lang=lang)

            else:

                text = complete_prompt[len("$traduzir"):].strip()

                if not text:

                    raise ValueError ('Error: texto para a tradução não fornecido')

                translation = self.ai_services.translate_prompt(text)

            return 'translation', translation
            
        except Exception as e:

            raise ValueError (f'Error ao traduzir texto: {str(e)}')

    def _generate_image(self, prompt: str, modelo_image: str) -> Tuple[str,str]:

        try:

            image_path = self.ai_services.generate_img(prompt, modelo_image)
            image_name = os.path.basename(image_path)

            return 'image', image_name

        except Exception as e:

            raise ValueError (f'Error ao gerar imagem: {str(e)}')

    def _generate_code(self, prompt: str) -> Tuple[str,str]:

        try:

            generated_code = self.ai_services.code_generator(prompt)

            return 'code', generated_code

        except Exception as e:

            raise ValueError (f'Error ao gerar o codigo: {str(e)}')

    def _generate_summary(self, text: str) -> Tuple[str,str]:

        try:

            summary = self.ai_services.summarize_text(text)

            return 'summary', summary

        except Exception as e:

            raise ValueError (f'Error ao gerar resumo: {str(e)}')

    def _process_command(self,complete_command: str, complete_prompt: str, modelo_image: str) -> Tuple[str,str]:

        try:
            if complete_command == '$traduzir':

                return self._handle_translation(complete_prompt)
                
            prompt_text = complete_prompt[len(complete_command)+1:].lstrip().strip()

            if complete_command == "$imagem":

                return self._generate_image(prompt_text, modelo_image)

            elif complete_command == "$codigo":

                return self._generate_code(prompt_text)

            elif complete_command == "$resumo":
                
                return self._generate_summary(prompt_text)
            else:

                raise ValueError(f'comando inválido: {complete_command}')

        except Exception as e:

            raise ValueError(f'Error ao processar comando "{complete_command}": {str(e)}')
 
    def process_prompt(self, unified_prompt: str, modelo_image: str) -> Tuple[str,str]:

        if not unified_prompt or not modelo_image:

            raise ValueError ("Todos os campos são obrigatórios")

        detected_command = self._detect_command(unified_prompt)

        if detected_command is None:

            raise ValueError ("Comando inválido")

        return self._process_command(detected_command, unified_prompt, modelo_image)




