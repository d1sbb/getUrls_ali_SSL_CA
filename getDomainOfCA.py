import requests
import sys

def get_domain_and_port(url):
    if url.startswith("https://"):
        return url[12:], "443"
    elif url.startswith("http://"):
        return url[11:], "80"
    else:
        return url, "443"
        # raise ValueError("不支持的协议. 仅支持 HTTP 和 HTTPS.")

def send_get_request(url):
    domain, port = get_domain_and_port(url)
    data = '{"Domain":"%s:%s"}' % (domain, port)

    headers = {
        "Host": "yundun.console.aliyun.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Cookie": "login_aliyunid_ticket=你的阿里key",
        "Accept": "*/*"
    }

    params = {
        "regionId": "cn-hangzhou",
        "data": data
    }
    response = requests.get("https://yundun.console.aliyun.com/openapi/cas/2018-08-13/DescribeForScanningServerCertificate.json", headers=headers, params=params)
    results = response.json()
    results = results["data"]["Results"]
    san_values_list = []
    for entry in results:
        certificates = entry["CertificateInfoList"]
        for certificate in certificates:
            san_values_list.extend(certificate["SanValues"])
    # 将列表中的元素连接成一个字符串，使用逗号分隔
    san_values_string = '\n'.join(san_values_list)
    return san_values_string

def main():
    print("这是阿里的一个SSL状态检测的接口，通过相同证书来收集其他域名 By_tallbao")
    print("运行前请换成自己的阿里云cookie，仅需填login_aliyunid_ticket的值^^")
    url = input("请输入URL: ")

    try:
        response_text = send_get_request(url)
        with open("getDomains.txt", "a") as file:
            file.write(response_text)
        print("获取内容已保存到 getDomains.txt 文件中。")
    except Exception as e:
        print("发生错误:", e)

if __name__ == "__main__":
    main()