import pdfplumber as ppl
import fitz

# page_center是一个经验值，即pdf文档页面中间的x坐标，用于把字符分成左右两部分
def extract_paper(filename, page_center=290):

    def _is_chinese(word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False
        
    pdf = ppl.open(filename)
    paras = []
    for page in pdf.pages:
        page_words = page.extract_words()
        # x0：单词的第一个字符的x坐标
        # x1：单词的最后一个字符的x坐标
        # top：单词的第一个字符的y坐标
        sentence = [[word['text'], round(word['x0']), round(word['x1']), round(word['top'])] for word in page_words]
        rows = []
        tmp = []
        for word in sentence:
            # 前后单词y坐标相差大于4（这里4也是一个经验值，一般不超过10），说明不是同一行
            if tmp and abs(word[-1] - tmp[-1][-1]) > 4:
                # 另起一行
                rows.append(tmp)
                tmp = []
            tmp.append(word)
        if tmp:
            rows.append(tmp)

        rows_in_page = []
        left_block, right_block = [], []

        for row in rows:
            is_two_columns=False
            row_left, row_right = [], []
            # row是一个二维list，表示一行的内容，形式如：[[text, x0, x1, top], [[text, x0, x1, top]], ...]
            for i in range(len(row)):

                # 用单词最后一个字符的x坐标判断属于左边还是右边
                if row[i][2]<page_center:
                    row_left.append(row[i])
                else:
                    row_right.append(row[i])
                # 前后两个单词相距超过10（说明中间有较长的空白），并且前后两个单词分别属于左右两边，则说明这一行是列式布局
                if i>0 and row[i][1]- row[i-1][2]>10 and row[i][1]>page_center and row[i-1][2]<page_center:
                    is_two_columns=True
            if is_two_columns:
                left_block.extend(row_left)
                right_block.extend(row_right)
            else:
                # 把之前的left和right添加，先左后右
                if left_block:
                    rows_in_page.extend(left_block)
                if right_block:
                    rows_in_page.extend(right_block)
                # 这一行不是列式布局，则正常添加当前行
                rows_in_page.extend(row)
                
                left_block=[]
                right_block=[]

        # 中英文字符空格处理
        txt = [x[0] if _is_chinese(x[0]) else ' '+x[0] for x in rows_in_page]
        paras.extend(txt)

    return "".join(paras)

def extract_content(pdf_file):
    pdf_document = fitz.open(pdf_file)
    # 获取总页数
    total_pages = pdf_document.page_count
    # 提取整个文档的文本
    full_text = ""
    for page_num in range(total_pages):
        page = pdf_document.load_page(page_num)
        full_text += page.get_text("text")
    return full_text
