from shiny import App, reactive, render, ui
from shiny.types import ImgData
import MakeOligomers_shiny

isocyanate_list = open("isocyanates.txt","r").read().splitlines() 
poliols_list = open("poliols.txt","r").read().splitlines()

app_ui = ui.page_fluid(
    ui.panel_title("", "oligomer"),
    ui.layout_sidebar(

      ui.panel_sidebar(
        ui.p(
            ui.h1("o l i g o m e r", align="center"),
            ui.h4("Generator of short PU fragments", align="center"),
            
            ui.h6("SELECT SUBSTRATES"),
            
            ui.input_select("isocyanates", "Isocyanates:", isocyanate_list, multiple = True),
            
            ui.input_select("poliols", "Hydroxyl compunds:", poliols_list, multiple = True),
            
            ui.input_file("uploaded_file", "Upload other substrates \n (Accepted file format: Name;SMILES)"),
            
            ui.output_ui("check_input"),
            
            ui. output_ui("select_size"),
            ui.h6("SELECT SIZE"),
            ui.input_radio_buttons("size", "", ["2 units","3 units","4 units"], 
                                selected=None),
            
            ui.input_action_button("make_oligomers", "Make oligomers!")
      ), width=4),
      ui.panel_main(
            ui.output_image("oligomer_image",),
            
            ui.output_ui("process_substrates"),
            
            ui.output_ui("perform_reactions"),
            
            ui.output_ui("download_options")
      )
    )

)


def server(input, output, session):
    
    # Main panel image 
    @output
    @render.image
    def oligomer_image():
        if input.make_oligomers():
            img: ImgData = {"src": 'oligomer_reaction.png', "width": "90%"}
        else:
            img: ImgData = {"src": 'oligomer_main.png', "width": "90%"}
        return img
        
    
    # Check uploaded file   
    @output
    @render.ui
    def check_input():
        if input.uploaded_file() != None:
            uploaded_input = input.uploaded_file()[0]['datapath']
            title_line, valid_file = MakeOligomers_shiny.validate_input(uploaded_input)
            if not valid_file:
                return ui.HTML("""<b>ERROR: Wrong input file!</b><br> 
                               Upload substrates in format: Name;SMILES<br><br>""")    
   
    # Process substrates
    @output
    @render.ui
    @reactive.event(input.make_oligomers)
    def process_substrates():
        if input.make_oligomers():
            substrates = []
            smiles = []
            if input.isocyanates():
                for iso in input.isocyanates():
                    comp = iso.split(";")
                    smiles.append(comp[1])
                    substrates.append([comp[0],comp[1]])
            
            if input.poliols():
                for ol in input.poliols():
                    comp = ol.split(";")
                    smiles.append(comp[1])
                    substrates.append([comp[0],comp[1]])
            
            if input.uploaded_file():
                input_file = input.uploaded_file()[0]['datapath']
                uploaded_substrates = open(input_file,"r").read().splitlines()
                if uploaded_substrates[0] == 'Name;SMILES\n':
                    lines = range(1,len(uploaded_substrates))
                else:
                    lines = range(len(uploaded_substrates))
                    
                for line in lines:
                    if uploaded_substrates[line] != "":
                        comp = uploaded_substrates[line].split(";")
                        if comp[1] not in smiles:
                            substrates.append([comp[0],comp[1]])
                            smiles.append(comp[1])
            if not (input.isocyanates() or input.poliols() or input.uploaded_file()):
                return ui.HTML("Substrates not selected.")               

            # Perform reactions
            if substrates:
                subtrates_grouped = MakeOligomers_shiny.prepare_reaction(substrates)
                selected_size = int(input.size().split()[0])
                    
                if selected_size == 2:
                    i = MakeOligomers_shiny.perform_dimerization(subtrates_grouped[2], subtrates_grouped[3])
                elif selected_size == 3:
                    i = MakeOligomers_shiny.perform_trimerization(subtrates_grouped[2], subtrates_grouped[3])
                elif selected_size == 4:
                    i = MakeOligomers_shiny.perform_tetramerization(subtrates_grouped[2], subtrates_grouped[3])
                
                return ui.HTML(subtrates_grouped[1]), ui.HTML(i[0]), ui.HTML(i[1])
                
    
    # Show output buttons
    @output
    @render.ui
    def download_options():
        if input.make_oligomers():
            return (ui.h6("DOWNLOAD RESULTS"),
                    ui.input_switch("smiles", "Save SMILES"),
                    ui.input_switch("m2D", "Save 2D structures"),
                    ui.input_switch("m3D", "Save 3D structures"),
                    ui.input_switch("conformers", "Save conformers"),
                    ui.input_switch("images", "Save images"),
                    ui.download_button("output", "Save output")
                    )
                
            
    # Generate reactions
    @output
    @render.ui
    @reactive.event(input.make_oligomers)
    def perform_reactions():
        selected_isocyanates = input.isocyanates()
        selected_poliols = input.poliols()  
        selected_substrates = selected_isocyanates + selected_poliols
        if input.uploaded_file() != None:
            uploaded_input = input.uploaded_file()[0]['datapath']
            uploaded_substrates = open(uploaded_input,"r").read().splitlines()
            for item in uploaded_substrates:
                selected_substrates+=(item,)
             
        i = selected_substrates
        
        
        # if input.uploaded_file() != None:
        #     uploaded_input = input.uploaded_file()[0]['datapath']
        #     title_line, valid_file = MakeOligomers_shiny.validate_input(uploaded_input)
        #     if valid_file:
                         
        #         check_input = MakeOligomers_shiny.prepare_reaction(uploaded_input, title_line)
        #         if check_input[0]:
        #             selected_size = int(input.size().split()[0])
                    
        #             if input.reaction_images():
        #                 if selected_size == 2:
        #                     i = MakeOligomers_shiny.perform_dimerization(check_input[2], check_input[3],True)
        #                 elif selected_size == 3:
        #                     i = MakeOligomers_shiny.perform_trimerization(check_input[2], check_input[3])
        #                 elif selected_size == 4:
        #                     i = MakeOligomers_shiny.perform_tetramerization(check_input[2], check_input[3])                
                    
                        
        #             else:    
                    
        #                 if selected_size == 2:
        #                     i = MakeOligomers_shiny.perform_dimerization(check_input[2], check_input[3])
        #                 elif selected_size == 3:
        #                     i = MakeOligomers_shiny.perform_trimerization(check_input[2], check_input[3])
        #                 elif selected_size == 4:
        #                     i = MakeOligomers_shiny.perform_tetramerization(check_input[2], check_input[3])                
                        
        return ui.HTML("")
    
    
    
    


app = App(app_ui, server)


