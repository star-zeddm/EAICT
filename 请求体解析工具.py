import re
import tkinter as tk
from tkinter import scrolledtext, messagebox
from urllib.parse import urlparse
import configparser
import os
import webbrowser


class HTTPRequestConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("HTTP请求转换工具")
        self.root.geometry("800x650")

        # 创建界面组件
        self.create_widgets()

    def create_widgets(self):
        # 原始请求输入框
        tk.Label(self.root, text="原始HTTP请求:").pack(pady=(10, 0), anchor="w")
        self.raw_input = scrolledtext.ScrolledText(self.root, width=100, height=15)
        self.raw_input.pack(padx=10, pady=(0, 10))

        # 转换按钮
        self.convert_btn = tk.Button(self.root, text="转换为Python代码", command=self.convert_request)
        self.convert_btn.pack(pady=5)

        # 生成的Python代码
        tk.Label(self.root, text="生成的Python代码:").pack(pady=(10, 0), anchor="w")
        self.output_code = scrolledtext.ScrolledText(self.root, width=100, height=15)
        self.output_code.pack(padx=10, pady=(0, 10))

        # 底部按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # 保存按钮
        self.save_btn = tk.Button(button_frame, text="保存请求头(自动生成)", command=self.save_headers_to_ini)
        self.save_btn.pack(side="left", padx=5)

        # 复制按钮
        self.copy_btn = tk.Button(button_frame, text="复制代码", command=self.copy_to_clipboard)
        self.copy_btn.pack(side="left", padx=5)

        # 清除按钮
        self.clear_btn = tk.Button(button_frame, text="清除", command=self.clear_all)
        self.clear_btn.pack(side="left", padx=5)

        # GitHub链接
        github_frame = tk.Frame(self.root)
        github_frame.pack(side="bottom", pady=10)
        tk.Label(github_frame, text="GitHub项目地址:").pack(side="left")
        self.github_link = tk.Label(github_frame, text="https://github.com/star-zeddm/", fg="blue", cursor="hand2")
        self.github_link.pack(side="left")
        self.github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/star-zeddm/"))

    def parse_http_request(self, raw_http):
        """解析原始HTTP请求"""
        try:
            # 分割请求行和头部
            lines = [line.strip('\r') for line in raw_http.strip().split('\n')]

            # 解析请求行
            first_line = lines[0].strip()
            if not first_line:
                raise ValueError("无效的HTTP请求: 缺少请求行")

            # 处理可能的多空格分隔
            request_parts = re.split(r'\s+', first_line, 2)
            if len(request_parts) != 3:
                raise ValueError("无效的HTTP请求行格式")

            method, path, http_version = request_parts

            # 解析头部和正文
            host = None
            headers = {}
            body = None
            body_started = False
            current_header = None

            for line in lines[1:]:
                if not line:  # 空行表示头部结束
                    body_started = True
                    continue

                if not body_started:
                    # 处理头部续行（以空格或制表符开头）
                    if line.startswith((' ', '\t')) and current_header:
                        headers[current_header] += line.strip()
                    elif ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        headers[key] = value
                        current_header = key
                        if key.lower() == 'host':
                            host = value
                else:
                    # 收集请求体
                    if body is None:
                        body = line
                    else:
                        body += '\n' + line

            # 如果没有显式指定Host头部，尝试从其他头部推断
            if not host:
                for header in ['referer', 'origin', 'Referer', 'Origin']:
                    if header in headers:
                        try:
                            host = urlparse(headers[header]).netloc
                            if host:
                                break
                        except:
                            continue

            # 构建完整的URL
            if not host and 'Host' in headers:
                host = headers['Host']

            if not host:
                raise ValueError("无法确定请求的主机地址")

            # 确定协议
            scheme = 'https'
            if any(h.lower() in headers for h in ['X-Forwarded-Proto', 'x-forwarded-proto']):
                proto_header = 'X-Forwarded-Proto' if 'X-Forwarded-Proto' in headers else 'x-forwarded-proto'
                scheme = headers[proto_header]
            elif 'Referer' in headers and headers['Referer'].startswith('http://'):
                scheme = 'http'

            # 处理URL
            if path.startswith(('http://', 'https://')):
                url = path
            else:
                # 确保路径以斜杠开头
                if not path.startswith('/'):
                    path = '/' + path
                url = f"{scheme}://{host}{path}"

            return {
                'method': method,
                'url': url,
                'headers': headers,
                'body': body
            }

        except Exception as e:
            raise ValueError(f"解析HTTP请求时出错: {str(e)}")

    def generate_python_code(self, parsed_request):
        """生成Python requests代码"""
        method = parsed_request['method'].lower()
        url = parsed_request['url']
        headers = parsed_request['headers']
        body = parsed_request['body']

        code = "import requests\n\n"
        code += f"url = '{url}'\n"
        code += "headers = {\n"
        for key, value in headers.items():
            # 处理值中的单引号
            safe_value = value.replace("'", "\\'")
            code += f"    '{key}': '{safe_value}',\n"
        code += "}\n\n"

        if body:
            # 处理JSON请求体
            if 'Content-Type' in headers and 'json' in headers['Content-Type'].lower():
                code += "import json\n"
                code += f"data = json.dumps({body})\n\n"
                code += f"response = requests.{method}(url, headers=headers, data=data)\n"
            else:
                # 处理普通请求体
                safe_body = body.replace("'", "\\'")
                code += f"data = '''{safe_body}'''\n\n"
                code += f"response = requests.{method}(url, headers=headers, data=data)\n"
        else:
            code += f"response = requests.{method}(url, headers=headers)\n"

        code += "\nprint(response.status_code)\n"
        code += "print(response.text)\n"

        return code

    def convert_request(self):
        """转换按钮点击事件"""
        raw_text = self.raw_input.get("1.0", tk.END).strip()
        if not raw_text:
            messagebox.showwarning("警告", "请输入原始HTTP请求内容")
            return

        try:
            parsed = self.parse_http_request(raw_text)
            python_code = self.generate_python_code(parsed)
            self.output_code.delete("1.0", tk.END)
            self.output_code.insert("1.0", python_code)
            self.current_headers = parsed['headers']  # 保存当前请求头供导出使用

            # 自动保存INI文件
            self.save_headers_to_ini(silent=True)

        except Exception as e:
            messagebox.showerror("错误", f"解析HTTP请求时出错:\n{str(e)}")

    def save_headers_to_ini(self, silent=False):
        """保存请求头为INI文件"""
        if not hasattr(self, 'current_headers') or not self.current_headers:
            if not silent:
                messagebox.showwarning("警告", "没有可保存的请求头信息")
            return

        try:
            # 创建配置解析器
            config = configparser.ConfigParser(interpolation=None)  # 禁用插值

            # 创建一个新的节并添加转义后的头部
            config['HTTP_HEADERS'] = {}
            for key, value in self.current_headers.items():
                # 替换可能的特殊字符
                safe_value = value.replace('%', '%%')
                config['HTTP_HEADERS'][key] = safe_value

            # 在当前目录生成request_headers.ini文件
            file_path = os.path.join(os.getcwd(), "request_headers.ini")

            with open(file_path, 'w', encoding='utf-8') as configfile:
                config.write(configfile)

            if not silent:
                messagebox.showinfo("成功", f"请求头已自动保存到:\n{file_path}")

        except Exception as e:
            if not silent:
                messagebox.showerror("错误", f"保存文件时出错:\n{str(e)}")

    def copy_to_clipboard(self):
        """复制代码到剪贴板"""
        code = self.output_code.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("警告", "没有可复制的内容")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        messagebox.showinfo("成功", "代码已复制到剪贴板")

    def clear_all(self):
        """清除所有内容"""
        self.raw_input.delete("1.0", tk.END)
        self.output_code.delete("1.0", tk.END)
        if hasattr(self, 'current_headers'):
            del self.current_headers


if __name__ == "__main__":
    root = tk.Tk()
    app = HTTPRequestConverter(root)
    root.mainloop()