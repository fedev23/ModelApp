from shiny import reactive, render, ui
import pandas as pd
import asyncio
from global_var import global_data_loader_manager  # Importar el gestor global
from funciones.create_param import create_screen
from clases.global_name import global_name_manager
from clases.global_modelo import modelo_produccion
from clases.class_extact_time import global_fecha
from funciones.create_nav_menu import create_nav_menu
from clases.class_screens import ScreenClass
from funciones.utils import retornar_card
from clases.class_user_proyectName import global_user_proyecto
from funciones.utils_2 import errores


def server_produccion(input, output, session, name_suffix):
    hay_error = reactive.Value(False)
    proceso_a_completado = reactive.Value(False)
    directorio_produccion = r'C:\Users\fvillanueva\Desktop\SmartModel_new_version\new_version_new\Automat\datos_entrada'
    name = "Producción"
    mensaje = reactive.Value("")
    data_loader = global_data_loader_manager.get_loader(name_suffix)
    # Instanciamos la clase ScreenClass
    screen_instance = ScreenClass(directorio_produccion, name_suffix)

    @output
    @render.text
    def nombre_proyecto_produccion():
        return f'Proyecto: {global_user_proyecto.mostrar_nombre_proyecto_como_titulo()}'

    @output
    @render.ui
    def nav_out_to_produccion():
        return create_nav_menu(name_suffix, name)

    @reactive.Effect
    @reactive.event(input.file_produccion)
    async def loadOutSample():
        print("entre")
        await screen_instance.load_data(input.file_produccion, input.delimiter_produccion, name_suffix)

    @reactive.Effect
    @reactive.event(input.load_param_produccion)
    def produccion_out_to_and_valid():
        df = data_loader.getDataset()
        if df is None:
            mensaje.set(f"No se seleccionó ningún archivo en {name}")
        if screen_instance.proceso_a_completado.get():
            create_navigation_handler(f'load_param_{name_suffix}', 'Screen_3')
            ui.update_accordion("my_accordion", show=["Produccion"])

    @output
    @render.text
    def error_in_produccion():
        return errores(mensaje)

    @output
    @render.data_frame
    def summary_data_produccion():
        return screen_instance.render_data_summary()

    @output
    @render.ui
    def mostrarOut_produccion():
        if proceso_a_completado.get():
            return ui.input_action_button("ir_ejecucion_produccion", "Ir a ejecución")
        return ui.TagList()

    # estoy usando la clase para la creacion de modelos aca, lueog veo si adapto todas o las dejo en modelo

    @output
    @render.ui
    def card_produccion1():
        return retornar_card(
            get_file_name=global_name_manager.get_file_name_produccion,
            get_fecha=global_fecha.get_fecha,
            modelo=modelo_produccion
        )

    @output
    @render.text
    def mensaje_produccion():
        return modelo_produccion.mostrar_mensaje()

    # USO ESTE DECORADOR PARA CORRER EL PROCESO ANSYC Y NO HAYA INTERRUCIONES EN EL CODIGO LEER DOCUENTACION
    # https://shiny.posit.co/py/docs/nonblocking.html
    @ui.bind_task_button(button_id="execute_produccion")
    @reactive.extended_task
    async def ejecutar_produccion_async():
        # Ejecutar proceso y establecer el valor en el objeto reactivo
        await modelo_produccion.ejecutar_proceso_prueba()

    @reactive.effect
    @reactive.event(input.execute_produccion)
    def ejecutar_produccion():
        ejecutar_produccion_async()

    def create_navigation_handler(input_id, screen_name):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
            await session.send_custom_message('navigate', screen_name)

    @reactive.Effect
    @reactive.event(input[f'open_html_{modelo_produccion.nombre}'])
    def enviar_result():
        create_navigation_handler(
            f'open_html_{modelo_produccion.nombre}', 'Screen_Resultados')
        ui.update_accordion("my_accordion", show=["produccion"])

    create_navigation_handler('start_produccion', 'Screen_User')
    create_navigation_handler('screen_in_sample_produccion', 'screen_in_sample')
    create_navigation_handler('screen_Desarollo_produccion', 'Screen_Desarollo')
    create_navigation_handler('load_Validacion_produccion', 'Screen_valid')
    create_navigation_handler('screen_Produccion_produccion', 'Screen_Porduccion')
    create_navigation_handler('ir_modelos_produccion', 'Screen_3')
    create_navigation_handler("ir_result_produccion", "Screen_Resultados")
    create_navigation_handler("volver_produccion", "Screen_User")
