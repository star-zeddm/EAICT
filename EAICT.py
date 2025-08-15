from tkinter import *
from tkinter import messagebox
import requests
import re
import webbrowser
import configparser
from PIL import Image, ImageTk
import os

# HEADERS = {
#         "Cookie": "BIDUPSID=E235731BA6B919F5F3C24FAA2ACDB65D; PSTM=1732673045; BAIDUID=E235731BA6B919F58D6B750BB22BBCFF:FG=1; H_PS_PSSID=60271_61027_61054_61135_61140_61156_61178_61218_61211_61214_61239_61287; BAIDUID_BFESS=E235731BA6B919F58D6B750BB22BBCFF:FG=1; in_source=; log_first_time=1737430791534; ppfuid=FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGl54cTh3pOgTyao5J7yyxW7/VC+Kd/PngdwCv5WfV0iP3efldEnw4+7qfVzNX7X7ZvXEymXZ7vIeVtTSY2u6kADVgeLNEqiQqRHoDHn7huVqy2H/zju0tlHnG7joNOPEawxg3XduDu1LQGcI8Qah4c9Ks5+Bm57DHOG4XwLtn1ztW8tRqKUkqDhgP5FRw9NLXmTkwA5GQ/hyIdmdqG8e+8W8OdEuZ242+1RyigUrmZ4jUHv1DxZiH330Apc6oKkZo0Y6IJXad8xN1gQMZ1tOmckSecr9yhMSRLVoFktEC1isFW/ROI5v+vVAliVWJGW5HgFMb7+JFWxNGoA0JNiv6hCb0gkXpkEpISi6tVHh+hsQifjACGGz0MbLI9AAutvQNmLovQE8DrrUkOPSWZkiBwIUvxonSGS2lgiNZBxgK/Nad6P3sfvyvYhyXNwxm6SzH+Oja1l6cy9uoP7y446ILa1CLEOaV1jDkGoksNhRtn7B1VPovN1TRU04qLrmECuDGMBVR4vlhy8DqZQ1/LUEQ9mrM1XTShMu8Y6z7mcjIEx0SRhpMWhMo8MNW10I79rYiEZqj4cFtwDdJ/UZaa6iAMtQJsQN5mcP7l0phxlMCLHljdpCE44gtacKuIAL7fDTck9aMDA0wNIlJo9fK+rPw0T9+JIpQ6nVWxL4vL34i6mfzL4hLXcGAwm/blGCaj2qqlhN1cdi5hUk99gF8iC4u7PLY1O540Gbhx6NM0AEaGAyhwuOPgholqmaWjD3gGT2h9Asw5MktHEx3qmgMyCheA4RuK4Xh9wa58/i6DblN6kL37MoBk2+fk1Zu8uXMwS+/rrQ6U1O7Zv2wiyJOnrYyq/5Tv2IOghUDulefRvlX9eT7gQwEiclvXWS2pMTilyx6wORXYWMC8Ewe1rUuQprEZZNDywMI17CupLBOAx9qwTTBhEMNzi6OXbElHkA3erw56I0vmkH9G20tmAiqCABGBI1qeHlbtIIUXAPQK2AKm25kN9e++uG7KATaiQSHPJR405LDjC+5v0mQclI0YcJp8DvGLdRUpGcbUX7V27dvoxZNlkNAKwTxTOnYZkLWOYVTD5EoNlrqqJb8Op38LjSNcK; Hm_lvt_18ca88c840f4f94ef856298c2c8435a9=1737431002; HMACCOUNT=C9F0300199ABB3D0; login_id=373825955; device_type=dgtsale-h5; acc_id=373825955; GAT_QRNIGOL_FFA=cf1d3d9b1a82d2f87d633bd8a03423; log_last_time=1737431003121; sajssdk_2015_cross_new_user=1; BDPPN=ab93de6dadbbbee4eb393e067d662aad; login_type=passport; _t4z_qc8_=xlTM-TogKuTwd8lOkqB5L8VMHZ8qnveAtwmd; Hm_lpvt_18ca88c840f4f94ef856298c2c8435a9=1737431067; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22373825955%22%2C%22first_id%22%3A%2219486f533764b7-0da05e0dc9aa3e-1037357a-2073600-19486f533771231%22%2C%22props%22%3A%7B%7D%2C%22%24device_id%22%3A%2219486f533764b7-0da05e0dc9aa3e-1037357a-2073600-19486f533771231%22%7D; ab_sr=1.0.1_MTIyNzBjYTA5MjhmY2UyMjcxOGIyZTIzZjIzYTcyZWVkOGFhNjBlNjY0NDllZDJjNDJlZTI3MmNhMjI4MWEyYmY4ZWZmY2E4MTY5YTVhOGQ2MGIzOGNhZGU2YjQ1MWYwNzA1MWNhNzcxYTY0ODk5YzQwYTkzMzI2MTIwZTk1MmY2NjFlNjUyZmRmNTVjNjM4NDk1MjhmZmZmMzIyZWI4ZA==; BDUSS=NaTVNiVXh-YVlJSk1hTGlKemVNdXhHZnNOVWVLQ05WTkE3R0hVc0JDdy1wYlpuSVFBQUFBJCQAAAAAAQAAAAEAAAC~a1Z6v9rL42Jhc2U2NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD4Yj2c-GI9ndD; BDUSS_BFESS=NaTVNiVXh-YVlJSk1hTGlKemVNdXhHZnNOVWVLQ05WTkE3R0hVc0JDdy1wYlpuSVFBQUFBJCQAAAAAAQAAAAEAAAC~a1Z6v9rL42Jhc2U2NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD4Yj2c-GI9ndD; RT=z=1&dm=baidu.com&si=27896759-2464-488d-818c-d453abcab41a&ss=m65xfdf9&sl=m&tt=ui6&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=709j",
#         "Content-Length": "193",
#         "Sec-Ch-Ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
#         "Auth-Type": "PAAS",
#         "Sec-Ch-Ua-Mobile": "?0",
#         "Env": "WEB",
#         "Client-Version": "0",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.60 Safari/537.36",
#         "Content-Type": "application/json;charset=UTF-8",
#         "Accept": "application/json, text/plain, */*",
#         "X-Sourceid": "24b43d846bd3bf470000550eb1425f8e",
#         "X-Requested-With": "XMLHttpRequest",
#         "Api-Version": "0",
#         "User-Info": "uc_id=;uc_appid=585;acc_token=;acc_id=373825955;login_id=373825955;device_type=dgtsale-h5;paas_appid=18;version=12;login_type=passport",
#         "Sec-Ch-Ua-Platform": '"Windows"',
#         "Origin": "https://xunkebao.baidu.com",
#         "Sec-Fetch-Site": "same-origin",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Dest": "empty",
#         "Referer": "https://xunkebao.baidu.com/index.html",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "zh-CN,zh;q=0.9",
#         "Priority": "u=1, i",
#         "Connection": "close"
#     }
class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("800x600+200+200")
        self.master.title('爱企查API工具')

        # 初始化配置
        self.headers = self.load_headers()  # 只加载headers

        # 设置窗口图标
        self.set_window_icon()

        self.create_widgets()
        self.pack(fill=BOTH, expand=True)

    def load_headers(self):
        """从config.ini加载HTTP请求头"""
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), 'request_headers.ini')

        try:
            if not os.path.exists(config_path):
                raise FileNotFoundError("request_headers.ini文件不存在")

            config.read(config_path, encoding='utf-8')

            if not config.has_section('HTTP_HEADERS'):
                raise ValueError("config.ini中缺少[HTTP_HEADERS]节")

            # 构建headers字典
            headers = {}
            for key, value in config.items('HTTP_HEADERS'):
                headers[key] = value.strip('"')  # 去除可能的多余引号

            return headers

        except Exception as e:
            messagebox.showerror("配置错误", f"加载请求头失败: {str(e)}")
            self.master.destroy()
            raise

    def set_window_icon(self):
        """设置应用图标"""
        try:
            self.master.iconbitmap("app_icon.ico")
        except:
            try:
                icon = Image.open("app_icon.png")
                icon_photo = ImageTk.PhotoImage(icon)
                self.master.iconphoto(True, icon_photo)
            except:
                print("图标文件未找到，使用默认图标")

    def create_widgets(self):
        """初始化UI组件"""
        # 顶部输入框和查询按钮
        self.input_frame = Frame(self)
        self.input_frame.pack(fill=X, padx=10, pady=5)

        Label(self.input_frame, text="企业名称:").pack(side=LEFT)
        self.entry = Entry(self.input_frame, width=40)
        self.entry.pack(side=LEFT, padx=5)
        Button(self.input_frame, text="查询", command=self.get_keyid).pack(side=LEFT)

        # 结果显示区域
        self.result_frame = Frame(self)
        self.result_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        self.list_text = Text(self.result_frame, width=40, height=20, bg="#f0f0f0")
        self.list_text.pack(side=LEFT, fill=Y, padx=(0, 5))

        self.detail_text = Text(self.result_frame, width=60, height=20, bg="black", fg="white")
        self.detail_text.pack(side=LEFT, fill=BOTH, expand=True)

        # 底部操作按钮和状态栏
        self.button_frame = Frame(self)
        self.button_frame.pack(fill=X, padx=10, pady=5)

        Button(self.button_frame, text="解锁企业信息", command=self.unlock).pack(side=LEFT, padx=5)
        Button(self.button_frame, text="获取联系方式", command=self.get_phone).pack(side=LEFT)

        # GitHub链接
        self.status_bar = Frame(self, bd=1, relief=SUNKEN)
        self.status_bar.pack(side=BOTTOM, fill=X, padx=5, pady=2)

        github_url = "https://github.com/star-zeddm/"
        self.github_link = Label(
            self.status_bar,
            text=f"GitHub: {github_url}",
            fg="blue",
            cursor="hand2",
            font=("Arial", 9, "underline")
        )
        self.github_link.pack(side=RIGHT, padx=10, pady=2)
        self.github_link.bind("<Button-1>", lambda e: webbrowser.open_new(github_url))
        self.github_link.bind("<Enter>", lambda e: self.github_link.config(fg="red"))
        self.github_link.bind("<Leave>", lambda e: self.github_link.config(fg="blue"))

        self.status_label = Label(self.status_bar, text="就绪", anchor=W)
        self.status_label.pack(side=LEFT, fill=X, expand=True)

    # 以下是业务方法（使用self.headers）
    def get_keyid(self):
        """查询企业列表"""
        self.list_text.delete(1.0, END)
        enterprise_name = self.entry.get().strip()
        if not enterprise_name:
            messagebox.showwarning("提示", "请输入企业名称")
            return

        url = 'https://xunkebao.baidu.com/crm/web/aiqicha/bizcrm/enterprise/simpleSearch'
        payload = {
            "params": {
                "searchTypeCode": "name",
                "searchValue": enterprise_name,
                "isNeedHighLight": True,
                "highLightTag": "<em>"
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()  # 检查HTTP错误
            data_list = response.json()['data']["dataList"]

            self.v = StringVar()
            for idx, company in enumerate(data_list):
                name = company["name"].replace("<em>", "").replace("</em>", "")
                rb = Radiobutton(
                    self.list_text,
                    text=f"{idx}: {name}",
                    value=company['id'],
                    variable=self.v,
                    anchor="w",
                    bg="#f0f0f0"
                )
                self.list_text.window_create(END, window=rb)
                self.list_text.insert(END, "\n")

        except requests.RequestException as e:
            messagebox.showerror("请求错误", f"查询失败: {str(e)}")
        except ValueError as e:
            messagebox.showerror("数据错误", f"解析响应失败: {str(e)}")

    def unlock(self):
        """解锁企业信息"""
        if not hasattr(self, 'v') or not self.v.get():
            messagebox.showwarning("提示", "请先选择企业")
            return

        url = "https://xunkebao.baidu.com/crm/web/aiqicha/bizcrm/enterprise/resourceunlock/unlockresource"
        payload = {
            "param": {
                "resourceType": 1,
                "resourceIds": [self.v.get()],
                "isNeedValidate": True
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()["data"]

            if result.get("unlockSuceccedIdlist"):
                message = f"解锁成功: {result['unlockSuceccedIdlist'][0]}"
            else:
                message = f"企业已解锁: {result['alreadyUnlockIdlist'][0]}"

            self.detail_text.insert(END, message + "\n")
            self.status_label.config(text=message)

        except requests.RequestException as e:
            messagebox.showerror("请求错误", f"解锁失败: {str(e)}")

    def get_phone(self):
        """获取联系方式"""
        if not hasattr(self, 'v') or not self.v.get():
            messagebox.showwarning("提示", "请先选择企业")
            return

        self.detail_text.delete(1.0, END)
        try:
            contacts = self._query_contacts(self.v.get())

            # 分类显示
            phones = [c for c in contacts if re.match(r'^1[3-9]\d{9}$', c)]
            emails = [c for c in contacts if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', c)]
            others = [c for c in contacts if c not in phones + emails]

            self.detail_text.insert(END, "=== 手机号 ===\n" + "\n".join(phones) + "\n\n")
            self.detail_text.insert(END, "=== 邮箱 ===\n" + "\n".join(emails) + "\n\n")
            self.detail_text.insert(END, "=== 其他信息 ===\n" + "\n".join(others))

        except Exception as e:
            messagebox.showerror("错误", f"获取联系方式失败: {str(e)}")

    def _query_contacts(self, enterprise_id):
        """内部方法：查询联系方式"""
        url = "https://xunkebao.baidu.com/crm/web/aiqicha/bizcrm/enterprise/enterpriseContact/queryContactDetail"
        payload = {
            "param": {
                "enterpriseId": enterprise_id,
                "isNeedCrawlWeChat": True
            }
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        data = response.json()["data"][0]["contactsDetailTypeAndNumsVos"]
        return [item["value"] for detail in data for item in detail["contactsDetailAndNumsVos"]]


if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()