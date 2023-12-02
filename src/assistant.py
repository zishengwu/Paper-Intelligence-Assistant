from modelscope import AutoTokenizer, AutoModel, snapshot_download
from paperextracter import extract_paper
import torch

if __name__ == '__main__':
    file_path = '/mnt/workspace/askpdf/'
    model_dir = snapshot_download("ZhipuAI/chatglm3-6b-32k", revision = "v1.0.0")
    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_dir,trust_remote_code=True).quantize(8).cuda().eval()
     
    history = []
    file_content = None
    
    while True:
        choice = input("**************************\n" \
        "欢迎使用论文阅读助手～\n" \
        "1.输入论文名称(仅支持pdf后缀文件)\n" \
        "2.输入您的问题\n" \
        "3.按`q`退出\n" \
        "**************************\n"
        )
        
        if choice == 'q':
            break
        elif choice.split('.')[-1] == 'pdf':
            try:
                file_content = extract_paper(f"{file_path}"+choice)
            except Exception as e:
                print('论文获取失败:', e)
            else:
                print('论文解析成功！输入问题进行提问～')
        else:
            if file_content is None:
                print('未选择论文，请先选择需要阅读的论文')
                continue
            if len(history) == 0:
                query = f"已知内容：{file_content}\n{choice}"
            else:   
                query = f"{choice}"
                
            with torch.no_grad():
                response, history = model.chat(tokenizer, query, history=history)
            print(response)
            
