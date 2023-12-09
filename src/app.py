from transformers import AutoTokenizer, AutoModel
import pdfplumber as ppl
import gradio as gr
import fitz
import base64
from modelscope import AutoTokenizer, AutoModel, snapshot_download
import torch

model_dir = snapshot_download("ZhipuAI/chatglm3-6b-32k", revision = "v1.0.0")
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

model = AutoModel.from_pretrained(model_dir,trust_remote_code=True).quantize(8).cuda()
model = model.eval()

def render_pdf(pdf_file):
    if pdf_file:
        # 打开 PDF 文件
        pdf_document = fitz.open(pdf_file.name)
        base64_pdf = base64.b64encode(pdf_document.tobytes()).decode('utf-8')  
        pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="600" height="800" type="application/pdf">'
        return gr.update(value=pdf_display)
    return

def extract_content(pdf_file):
    pdf_document = fitz.open(pdf_file.name)
    # 获取总页数
    total_pages = pdf_document.page_count
    # 提取整个文档的文本
    full_text = ""
    for page_num in range(total_pages):
        page = pdf_document.load_page(page_num)
        full_text += page.get_text("text")
    return full_text, gr.Button.update(interactive=True)


def start_ask(instruction, chat_history, content):

    assert len(content)>0, '论文内容为空，请检查后重新上传！'
    
    if chat_history is None:
        chat_history = []
    chat_history.append((instruction, " "))
    
    # 模型最长支持32k的窗口，因此这里做了截断
    if len(content)>30000:
        content = content[:30000]
        
    past_key_values, history = None, []
    prompt = f"已知论文:{content}\n请回答问题:{instruction}\n"
    for response, history, past_key_values in model.stream_chat(tokenizer,
                                                                prompt,
                                                                history=history,
                                                                temperature=1,
                                                                past_key_values=past_key_values,
                                                                return_past_key_values=True):

        chat_history[-1] = (instruction, response, )
        yield instruction, chat_history


def build_app():
    import gradio as gr
    with gr.Blocks(title="AsktoPDF:论文阅读助手") as app:


        with gr.Row():

            pdf_render = gr.HTML("请点击右侧上传论文进行预览")
            with gr.Column(scale=1):
                upload = gr.File(file_types=["pdf"], label="上传文档")
                content = gr.Textbox(lines=2, label="论文解析", max_lines=2, visible=False)
                chatbot = gr.Chatbot(
                        label="论文阅读助手",
                        value=None,
                        height=500
                    )
                instruction = gr.Textbox(lines=2, label="请输入您的问题", placeholder="在这里输入问题...", max_lines=2)
                with gr.Row():
                    submit = gr.Button("提交", size="sm", interactive=False)
                    clean = gr.Button("清除", size="sm")
         
        upload.upload(fn=render_pdf, inputs=upload, outputs=pdf_render, queue=False).then(fn=extract_content, inputs=upload, outputs=[content,submit], queue=False)
        submit.click(fn=start_ask, inputs=[instruction, chatbot, content], outputs=[instruction, chatbot], queue=True)
        clean.click(fn=lambda: None, inputs=None, outputs=chatbot, queue=False)

    return app

if __name__=="__main__":
    app = build_app() 
    app.queue(concurrency_count=2, max_size=5)
    app.launch()
