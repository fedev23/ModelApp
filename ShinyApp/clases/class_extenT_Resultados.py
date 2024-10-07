
import os
import tempfile
from shiny import ui, reactive
from funciones.utils import create_zip_from_directory, create_zip_from_file_unico
from clases.class_result import ResultadoClass

class ResultadoClassPruebaExtendida(ResultadoClass):
    def __init__(self, resultado_id, resultado_path, directory_path, salida, descarga_unic, salida_descarga_unic, html_adicional, resultado_adicional, descarga_adicional_unic
                 ,salida_adicional):
        super().__init__(resultado_id, resultado_path, directory_path, salida, descarga_unic, salida_descarga_unic)
        self.html_adicional = html_adicional
        self.resultado_adicional = resultado_adicional
        self.descarga_adicional_unic = descarga_adicional_unic
        self.salida_adicional = salida_adicional
        
        
    

    def resultados_card_adicionales(self):
        card = super().resultado_card()
        return ui.card(
            ui.card_header(
                f"Resultado {self.html_adicional}",f"{self.resultado_id}",
                ui.accordion(
                     ui.accordion_panel(
                         f"Resultado ({self.html_adicional})",
                        ui.div(
                            ui.div(
                              #self.html_output_prueba(), 
                               ui.output_ui(self.salida_adicional),
                               #ui.output_ui(self.salida), 
                            ),
                            #ui.output_ui(self.salida),
                            ui.download_button(self.descarga_adicional_unic,  f"Descargar resultado {self.html_adicional}"),
                        ),
                        value=f"panel_{self.html_adicional}",
                        class_="d-flex justify-content-between align-items-center"
                    ),
                    id=f"accordion_{self.html_adicional}",
                    open=False
                     ),
                ),
               super().resultado_card()
                
            )
    
    def abrir_acordeon_adicional(self, input):
        @reactive.Effect
        @reactive.event(input[f"accordion_{self.html_adicional}"])
        def activar_boton():
            print("Acordeón adicional abierto")
            self.accordion_open.set(True)
            self.ver_resultado()
            
            

    def salida_html_adicional(self):
     if os.path.exists(self.resultado_adicional):
            with open(self.resultado_adicional, 'r', encoding='utf-8') as file:
                content = file.read()
                print("HTML cargado exitosamente.")
                self.html_content.set(content)
                
                

    def html_output_prueba_adicional(self):
        # Modifica o amplía el método de la clase base
        if self.accordion_open.get():
                iframe_src = f'http://127.0.0.1:5000/static/{os.path.basename(self.resultado_path)}'
                iframe_src2 = f'http://127.0.0.1:5000/static/{os.path.basename(self.resultado_adicional)}' 
                return ui.div(
                    ui.tags.iframe(src=iframe_src, width='350%', height='500px'),
                    ui.tags.iframe(src=iframe_src2, width='350%', height='500px')
                )
        return ui.HTML("<p>Archivo no encontrado</p>")
    
   
                
    def htmls_output(self):
        return ui.div(
         html_output = super().html_output_prueba(),
        html_adicional = self.html_output_prueba_adicional 
        )
                
        

    def descargar_resultados(self):
        # Puedes extender el método de la clase base
        zip_path = super().descargar_resultados()
        print(f"Resultados descargados en {zip_path}")
        return zip_path

    def boton_para_descagar_unico(self):
        # Modifica el botón para descarga única
        boton = super().boton_para_descagar_unico()
        if boton:
            # Agrega lógica adicional si es necesario
            boton.label = f"Descargar único resultado ({self.additional_param})"
        return boton

    def descargar_unico_html(self):
        # Puedes extender la funcionalidad del método de la clase base
        zip_path = super().descargar_unico_html()
        print(f"Archivo único descargado en {zip_path}")
        return zip_path




