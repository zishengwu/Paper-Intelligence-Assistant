import gradio as gr
import fitz
import base64
import ollama


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


def start_ask(instruction, chat_history, content, model):

    assert len(content)>0, '论文内容为空，请检查后重新上传！'
    
    if chat_history is None:
        chat_history = []
    chat_history.append((instruction, " "))
    
    # 模型最长支持32k的窗口，因此这里做了截断
    if len(content)>32000:
        content = content[:32000]
        
    
    stream = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': f"已知论文:{content}\n请根据论文内容来回答问题:{instruction}\n"}],
        stream=True,
    )

    response = ""
    for chunk in stream:
        tmp = chunk['message']['content']
        response += tmp
        chat_history[-1] = (instruction, response, )
        yield instruction, chat_history


def build_app():
    import gradio as gr
    with gr.Blocks(title="AsktoPDF:论文阅读助手") as app:


        with gr.Row():

            pdf_render = gr.HTML("请点击右侧上传论文进行预览")
            with gr.Column(scale=1):
                upload = gr.File(file_types=["pdf"], label="上传文档")
                models = gr.Dropdown(
                            label="选择模型",
                            show_label=True,
                            choices = [m['name'] for m in ollama.list()['models']] ,
                            type="value",
                            allow_custom_value=False,
                            scale=2
                        )
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
        submit.click(fn=start_ask, inputs=[instruction, chatbot, content, models], outputs=[instruction, chatbot], queue=True)
        clean.click(fn=lambda: None, inputs=None, outputs=chatbot, queue=False)

    return app

if __name__ == '__main__':
    app = build_app() 
    app.queue(max_size=5)
    app.launch()
