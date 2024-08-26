import os
import sys
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from apps.chat import ChatBot
from paddleocr import PaddleOCR
import PyPDF2


PAGE_NUM = 5  # 识别的页数


def extract_text(pdf_path: str) -> str:
    text = extract_text_origin(pdf_path)
    if text == "":
        text = extract_text_ocr(pdf_path)
    return text


def extract_text_origin(pdf_path: str) -> str:
    with open(pdf_path, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf)
        page_count = len(reader.pages)
        txt = ""
        for p in range(page_count):
            page = reader.pages[p]
            txt += page.extract_text()
        return txt


def extract_text_ocr(pdf_path: str) -> str:
    ocr_service = PaddleOCR(use_angle_cls=True, lang="ch", page_num=PAGE_NUM)
    result = ocr_service.ocr(pdf_path)
    text = ""
    for page_idx in range(len(result)):
        page_result = result[page_idx]
        if page_result is None:
            continue
        for line in page_result:
            text += str(line[1][0])
            text += '\n'
    return text


def score(pdf_path: str) -> str:
    chatbot = ChatBot()
    text = extract_text_origin(pdf_path)
    prompt = '请帮我给这个简历一个评分，满分100分。注意，返回格式是：[数字]分，不需要其他任何多余信息。\n'
    return chatbot.common_chat(prompt + text)


def suggest(pdf_path: str) -> str:
    chatbot = ChatBot()
    text = extract_text_origin(pdf_path)
    prompt = '请帮我给这个简历提一些建议，不超过50字。注意，请结合简历具体分析，只需要返回一段建议文字，以“建议：”开头，不需要其他任何多余信息。可以发送一些emoji表情。\n'
    return chatbot.common_chat(prompt + text)


def innovation(pdf_path: str) -> str:
    chatbot = ChatBot()
    text = extract_text_origin(pdf_path)
    prompt = '请给这个简历提取创新之处，不超过50字。注意，请结合简历具体分析，并且只需要返回一段文字，不需要其他任何多余信息。\n'
    return chatbot.common_chat(prompt + text)


if __name__ == '__main__':
    result = innovation(
        "D:/Projects/Edivator/Edivator/intelli/resume/北京航空航天大学_刘雨承_本科3年级-2(1).pdf")
    print(result)
