import qianfan

yichat = 'Yi-34B-Chat'


class ChatBot:
    def __init__(self, stream=False, model='Yi-34B-Chat'):
        import os
        os.environ["QIANFAN_ACCESS_KEY"] = ""
        os.environ["QIANFAN_SECRET_KEY"] = ""
        self.chat_comp = qianfan.ChatCompletion()
        self.stream = stream
        self.model_appointed = model

    def common_chat(self, content: str):
        resp = self.chat_comp.do(model=self.model_appointed, stream=self.stream, messages=[
            {"role": "user", "content": content}])
        return resp['body']['result']  # type: ignore

    def summarize(self, content: str) -> str:
        prompt = f'请帮我总结一下这段话：{content}，只需要返回总结后的内容，不需要其他任何多余信息。不超过100字。'
        resp = self.chat_comp.do(model=self.model_appointed, stream=self.stream, messages=[
            {"role": "user", "content": prompt}])
        return resp['body']['result']  # type: ignore

    def polish(self, content: str):
        prompt = f'请帮我润色这段话：{content}。只需要返回润色后的内容，不需要其他任何多余信息。'
        resp = self.chat_comp.do(model=self.model_appointed, stream=self.stream, messages=[
            {"role": "user", "content": prompt}])
        return resp['body']['result']  # type: ignore

    def translate(self, content: str, language: str = '英语'):
        prompt = f'请将这段话翻译成{language}：{content}。只需要返回翻译后的内容，不需要其他任何多余信息。'
        resp = self.chat_comp.do(model=self.model_appointed, stream=self.stream, messages=[
            {"role": "user", "content": prompt}])
        return resp['body']['result']  # type: ignore

    def continue_write(self, content: str):
        prompt = f'请根据下面提供的文本信息，续写这段文本：{content}。只需要返回续写后的内容，不需要返回其他任何多余信息。'
        resp = self.chat_comp.do(model=self.model_appointed, stream=self.stream, messages=[
            {"role": "user", "content": prompt}])
        return resp['body']['result']  # type: ignore

    def correct(self, content: str):
        prompt = f'请把下面的文字修改语法错误：{content}。只需要返回续写后的内容，不需要返回其他任何多余信息。'
        resp = self.chat_comp.do(model=self.model_appointed, stream=self.stream, messages=[
            {"role": "user", "content": prompt}])
        return resp['body']['result']  # type: ignore

    def styled_generate(self, content: str, style: str):
        prompt = f'请根据以下提示词，生成一段{style}风格的文本：{content}。只需要返回续写后的内容，不需要返回其他任何多余信息。'
        resp = self.chat_comp.do(model=self.model_appointed, stream=self.stream, messages=[
            {"role": "user", "content": prompt}])
        return resp['body']['result']  # type: ignore

    def form(self, content: str):
        prompt = f'请将下面这段文本叙述提取成表格。以html表格的源代码形式返回，如果提取成功则只返回html代码；如果识别不出表格，则返回“未识别出表格”。不需要返回任何多余的内容！！！！！ 文本内容如下：{content}'
        resp = self.chat_comp.do(model=self.model_appointed, stream=self.stream, messages=[
            {"role": "user", "content": prompt}])
        return resp['body']['result']  # type: ignore

    def get_keyword(self, content: str):
        prompt = f'请阅读下面这段文本，提取出10个关键字，关键字之间以","分隔。文本内容如下：{content}'
        resp = self.chat_comp.do(model=self.model_appointed, stream=self.stream, messages=[
            {"role": "user", "content": prompt}])
        return resp['body']['result']  # type: ignore
