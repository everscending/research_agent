import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager
from init_agent import defaultModel, setModel

load_dotenv(override=True)

async def run(query: str):
    async for chunk in ResearchManager().run(query):
        yield chunk

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    model_dropdown = gr.Dropdown(
            choices=["gpt-4o-mini", "deepseek-chat"], 
            label="Model", 
            info="Select your preferred model",
        )

    model_dropdown.change(fn=setModel, inputs=model_dropdown)

    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")
    
    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

ui.launch(inbrowser=True)

