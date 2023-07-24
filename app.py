from shiny import App, reactive, render, ui
from shiny.types import ImgData
from shinywidgets import output_widget, render_widget, register_widget
import ipywidgets
import MakeOligomers_shiny
from datetime import date


poliols_list = open("www/poliols.txt","r").read().splitlines()
isocyanate_list = open("www/isocyanates.txt","r").read().splitlines()

app_ui = ui.page_fluid(
    ui.panel_title("", "oligomer"),
    ui.layout_sidebar(

      ui.panel_sidebar(
        ui.p(
            ui.h1("o l i g o m e r", align="center"),
            ui.h4("Generator of short PU fragments", align="center"),
            ui.h6("SELECT SUBSTRATES"),
            
            # TO DO 
            # Add images for each compound in select option (as PIL generated from smiles or png)
            
            ui.input_select("isocyanates", "Isocyanates:", isocyanate_list, multiple = True),
            ui.input_select("poliols", "Hydroxyl compunds:", poliols_list, multiple = True),
            
            
            ui.input_file("uploaded_file", "Upload other substrates \n (Accepted file format: Name;SMILES)"),
            
            ui.output_ui("check_input"),
            
            ui.h6("SELECT SIZE"),
            ui.input_radio_buttons("size", "", ["2 units","3 units","4 units"]),
            
            ui.input_action_button("make_oligomers", "Make oligomers!")
            )
        ),
      ui.panel_main(
            
            ui.output_image("oligomer_image"),
            
            # Image options trials
            # ui.output_plot("my_widget", width="100px"),
            
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
            img: ImgData = {"src": 'www/oligomer_reaction.png', "width": "90%"}
        else:
            img: ImgData = {"src": 'www/oligomer_main.png', "width": "90%"}
        return img
    
       
    # Png generated from smiles can be rendered as plot
    @output 
    # @render_widget
    @render.plot
    def my_widget():
        smiles = MakeOligomers_shiny.smiles_to_image("CN=C=O")
        file = open("www/test_img.png", "rb")
        image = file.read()
        #register_widget("smiles",smiles)
        #return ipywidgets.Image(value=image,width=100)
        return smiles
        

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
            products_info = '<b> OLIGOMERS </b>'
                
            if selected_size == 2:
                reagents_smiles, products_smiles = MakeOligomers_shiny.perform_dimerization(subtrates_grouped[2], subtrates_grouped[3])
                reactions='<b>-_-_-_-_-_-_-_-_ dimerization products -_-_-_-_-_-_-_-_-_</b><br>'
                for rnum in range(len(reagents_smiles)):
                    reactions+='<br><b>Reaction %i:</b> %s + %s -> %s' %(rnum+1,reagents_smiles[rnum][0],reagents_smiles[rnum][1],products_smiles[rnum])
                    products_info+='<br> <b> %i.</b> %s' % (rnum+1,products_smiles[rnum])


            elif selected_size == 3:
                reagents_smiles, products_smiles = MakeOligomers_shiny.perform_trimerization(subtrates_grouped[2], subtrates_grouped[3])
                reactions='<b>-_-_-_-_-_-_-_-_ trimerization products -_-_-_-_-_-_-_-_-</b><br>'
                for rnum in range(len(reagents_smiles)):
                    reactions+='<br><b>Reaction %i:</b> %s + %s + %s -> %s' %(rnum+1,reagents_smiles[rnum][0],reagents_smiles[rnum][1],reagents_smiles[rnum][2],products_smiles[rnum])
                    products_info+='<br> <b> %i.</b> %s' % (rnum+1,products_smiles[rnum])
                
                
            elif selected_size == 4:
                reagents_smiles, products_smiles = MakeOligomers_shiny.perform_tetramerization(subtrates_grouped[2], subtrates_grouped[3])
                reactions='<b>-_-_-_-_-_-_-_- tetramerization products -_-_-_-_-_-_-_-_</b><br>'
                for rnum in range(len(reagents_smiles)):
                    reactions+='<br><b>Reaction %i:</b> %s + %s + %s + %s -> %s' %(rnum+1,reagents_smiles[rnum][0],reagents_smiles[rnum][1],reagents_smiles[rnum][2],reagents_smiles[rnum][3],products_smiles[rnum])
                    products_info+='<br> <b> %i.</b> %s' % (rnum+1,products_smiles[rnum])
                    
            reactions+="<br><br>"
            products_info += '<br><br>'
            return ui.HTML(subtrates_grouped[1]), ui.HTML(reactions), ui.HTML(products_info)
            

    
    # Show output buttons after button is clicked
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
                    ui.download_button("save_output", "Save output")
                    )
    
    # Download only for smiles as txt file
    # TO DO
    # Downloading folder with all selected options  
    @session.download(filename=lambda: f"oligomer-{date.today()}.txt")
    def save_output():
        
        substrates = []
        smiles = []
        
        # TO DO
        # How to acces output data without performing reactions again??
        
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
                reagents_smiles, products_smiles = MakeOligomers_shiny.perform_dimerization(subtrates_grouped[2], subtrates_grouped[3])
            elif selected_size == 3:
                reagents_smiles, products_smiles = MakeOligomers_shiny.perform_trimerization(subtrates_grouped[2], subtrates_grouped[3])
            elif selected_size == 4:
                reagents_smiles, products_smiles = MakeOligomers_shiny.perform_tetramerization(subtrates_grouped[2], subtrates_grouped[3])
        
        
        if input.smiles():
            for product in products_smiles:
                yield product 
                yield "\n"    
                

app = App(app_ui, server)


