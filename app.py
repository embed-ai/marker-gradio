import gradio as gr
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
import os


def process_pdf(pdf_file, progress=gr.Progress()):
    if pdf_file is None:
        return "Please upload a PDF file", "Waiting for file..."

    progress(0, desc="正在初始化...")
    converter = PdfConverter(
        artifact_dict=create_model_dict(),
    )

    progress(0.2, desc="正在加载PDF文件...")
    if not os.path.exists(pdf_file.name):
        return "File not found", "Error"

    progress(0.4, desc="正在转换PDF...")
    rendered = converter(pdf_file.name)

    progress(0.6, desc="正在处理页面内容...")
    progress(0.8, desc="正在提取文本...")
    text, _, images = text_from_rendered(rendered)

    progress(1.0, desc="完成!")
    return text, "处理完成"


with gr.Blocks() as demo:
    gr.Markdown("# PDF Text Extractor")
    gr.Markdown("Upload a PDF file to extract its text content")
    with gr.Column():
        pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
        status_output = gr.Textbox(label="状态", value="等待上传文件...", interactive=False)
        text_output = gr.Markdown(label="提取的文本", show_copy_button=True)
    pdf_input.change(
        fn=process_pdf,
        inputs=pdf_input,
        outputs=[text_output, status_output],
        show_progress=True,
    )

if __name__ == "__main__":
    demo.launch()
