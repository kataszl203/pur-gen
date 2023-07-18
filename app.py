from shiny import App, reactive, render, ui
from shiny.types import ImgData
import MakeOligomers_shiny

app_ui = ui.page_fluid(
    ui.panel_title("oligomer"),
    ui.layout_sidebar(

      ui.panel_sidebar(
        ui.p(ui.input_file("uploaded_file", "Upload substrates in format: Name;SMILES")),
        
        
        ui.input_radio_buttons("size", "Select oligomer size", ["2 units","3 units","4 units"], 
                            selected=None),
        ui.input_checkbox("reaction_images", "Show reactions", False),
        
        ui.input_action_button("make_oligomers", "Make oligomers!"),
        
        
        ui.input_switch("smiles", "Save SMILES"),
        ui.input_switch("m2D", "Save 2D structures"),
        ui.input_switch("m3D", "Save 3D structures"),
        ui.input_switch("conformers", "Save conformers"),
        ui.input_switch("images", "Save images"),
        
        ui.p(ui.download_button("output", "Save output"))
      ),
      ui.panel_main(
          ui.output_ui("check_input"),
          ui.output_ui("perform_reactions"),
          ui.output_image("test_image")
          #ui.output_ui("smiles")
      )
    )

)


def server(input, output, session):
            # selected_m2D = input.m2D()
        # selected_m3D = input.m3D()
        # selected_conformers = input.conformers()
        # selected_images = input.images()
    
    
    # Input file information
    @output
    @render.ui
    def check_input():
        if input.uploaded_file() != None:
            uploaded_input = input.uploaded_file()[0]['datapath']
            title_line, valid_file = MakeOligomers_shiny.validate_input(uploaded_input)
            if valid_file:
                check_input = MakeOligomers_shiny.prepare_reaction(uploaded_input, title_line)
                return ui.HTML(check_input[1])
            else:
                return ui.HTML("Wrong input file! Upload substrates in format: Name;SMILES")
            
        else:
            return ui.HTML("Load input file")
            
    # Generate reactions
    @output
    # @render.image
    @render.ui
    @reactive.event(input.make_oligomers)
    def perform_reactions():        
        if input.uploaded_file() != None:
            uploaded_input = input.uploaded_file()[0]['datapath']
            title_line, valid_file = MakeOligomers_shiny.validate_input(uploaded_input)
            if valid_file:
                         
                check_input = MakeOligomers_shiny.prepare_reaction(uploaded_input, title_line)
                if check_input[0]:
                    selected_size = int(input.size().split()[0])
                    
                    if input.reaction_images():
                        if selected_size == 2:
                            i = MakeOligomers_shiny.perform_dimerization(check_input[2], check_input[3],True)
                        elif selected_size == 3:
                            i = MakeOligomers_shiny.perform_trimerization(check_input[2], check_input[3])
                        elif selected_size == 4:
                            i = MakeOligomers_shiny.perform_tetramerization(check_input[2], check_input[3])                
                    
                        
                    else:    
                    
                        if selected_size == 2:
                            i = MakeOligomers_shiny.perform_dimerization(check_input[2], check_input[3])
                        elif selected_size == 3:
                            i = MakeOligomers_shiny.perform_trimerization(check_input[2], check_input[3])
                        elif selected_size == 4:
                            i = MakeOligomers_shiny.perform_tetramerization(check_input[2], check_input[3])                
                        
                    return ui.HTML(i)
    
    # Generate smiles of products
    @output
    @render.image
    def test_image():
        img: ImgData = {"src": '1.png', "width": "100px"}
        return img

app = App(app_ui, server)


