import gradio as gr
import matplotlib.pyplot as plt
import FRC
import FTC

def createOPRFig(opr_dict):
    # If there's no data or an error occurred, return an empty plot
    if not opr_dict or isinstance(opr_dict, str):
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
        return fig
    
    sorted_teams = sorted(opr_dict.items(), key=lambda x: x[1])
    teams = [str(team) for team, score in sorted_teams]
    scores = [score for team, score in sorted_teams]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(teams, scores, color='blue')

    ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)
    
    ax.set_title("Total OPR Distribution by Team")
    ax.set_xlabel("Team Number")
    ax.set_ylabel("Total OPR")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return fig

# This is the main function Gradio will call when the button is pressed.
# It takes the values from the GUI elements as parameters.
def calculate_opr(gameType, eventKey, apiKey, weighted):
    try:
        if gameType == "FRC":
            # We pass the two inputs to your FRC library
            # Make sure your FRCOPR function returns the list instead of printing it!
            result, totalOPR = FRC.FRCOPR(eventKey, apiKey, weighted)
            
        elif gameType == "FTC":
            # We pass the two inputs to your FTC library
            result, totalOPR = FTC.FTCOPR(eventKey, apiKey, weighted)
        
        distributionFig = createOPRFig(totalOPR)

        return result, distributionFig
            
    except Exception as e:
        # If something goes wrong, display the error in the output box
        return f"An error occurred: {str(e)}"

# Build the Gradio Interface
with gr.Blocks(theme = gr.themes.Soft()) as demo:
    gr.Markdown("# Robotics OPR Calculator")
    gr.Markdown("Select your game and provide the required inputs to calculate the Offensive Power Rating (OPR).")
    
    with gr.Row():
        # A radio button acts as a side-by-side toggle!
        game_toggle = gr.Radio(
            choices = ["FRC", "FTC"], 
            label = "Game Type", 
            value = "FRC" # Default value
        )
        weighted = gr.Radio(
            choices = [True, False], 
            label = "Weighted", 
            value = True # Default value
        )
        
    with gr.Row():
        # The two inputs you mentioned your program needs
        # You can change the labels to be more specific (e.g., "Team Number", "Event Code")
        eventKeyBox = gr.Textbox(label = "Event Key")
        apiKeyBox = gr.Textbox(label = "API Key")
    
    gr.Markdown("Your data is not preserved. ")
        
    calculate_btn = gr.Button("Calculate", variant="primary")
    
    # The output box to display your lists
    with gr.Row():
        with gr.Column(scale = 2):
            # The Textbox gets scale=1 (1/3 of the width)
            output_display = gr.Textbox(label = "OPR List")
            
        with gr.Column(scale = 3):
            # The Plot gets scale=2 (2/3 of the width)
            output_graph = gr.Plot(label = "OPR Distribution")
    
    # Connect the button to the function, defining what goes in and what comes out
    calculate_btn.click(
        fn = calculate_opr,
        inputs = [game_toggle, eventKeyBox, apiKeyBox, weighted],
        outputs = [output_display, output_graph]
    )

# Run the application
if __name__ == "__main__":
    demo.launch()