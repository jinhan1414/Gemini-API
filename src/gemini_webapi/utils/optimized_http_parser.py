import re
from urllib.parse import unquote


class CurlParser:
    def __init__(self, curl_command):
        self.curl_command = curl_command.strip()
        self.url = None
        self.method = "GET"
        self.headers = {}
        self.data = None
        self.cookies = {}

        self._parse()

    def _parse(self):
        # 提取 URL
        url_match = re.search(r"curl\s+'([^']+)'\s+", self.curl_command)
        if url_match:
            self.url = url_match.group(1)

        # 提取 -H 头部
        header_matches = re.findall(r"-H\s+'([^']*)'", self.curl_command)
        for header in header_matches:
            if ": " in header:
                key, value = header.split(": ", 1)
                self.headers[key] = value

        # 提取 -b cookie
        cookie_match = re.search(r"-b\s+'([^']*)'", self.curl_command)
        if cookie_match:
            cookie_str = cookie_match.group(1)
            cookies = dict([c.split("=", 1) for c in cookie_str.split("; ")])
            self.cookies = {k: unquote(v) for k, v in cookies.items()}

            # 合并到 headers
            cookie_header = "; ".join([f"{k}={v}" for k, v in self.cookies.items()])
            if "Cookie" in self.headers:
                self.headers["Cookie"] += "; " + cookie_header
            else:
                self.headers["Cookie"] = cookie_header

        # 判断是否是 POST 并提取 data
        data_match = re.search(r"--data-raw\s+'([^']*)'|--data\s+'([^']*)'", self.curl_command)
        if data_match:
            self.method = "POST"
            self.data = data_match.group(1) or data_match.group(2)

        # 判断 method 是否是其他类型（如 -X PUT）
        method_match = re.search(r"-X\s+(\w+)", self.curl_command)
        if method_match:
            self.method = method_match.group(1).upper()

    def get_url(self):
        return self.url

    def get_method(self):
        return self.method

    def get_headers(self):
        return self.headers

    def get_data(self):
        return self.data

    def get_cookie(self):
        """
        返回解析出的 cookie 字典
        """
        return self.cookies

if __name__ == '__main__':
    curl_str = """
    curl 'https://play.google.com/log?format=json&hasfast=true&authuser=0' \
  -H 'accept: */*' \
  -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'authorization: SAPISIDHASH 95f65d390db6127e4949606db5bd661330d909f8 SAPISID1PHASH 95f65d390db6127e4949606db5bd661330d909f8 SAPISID3PHASH 95f65d390db6127e4949606db5bd661330d909f8' \
  -H 'cache-control: no-cache' \
  -H 'content-encoding: gzip' \
  -H 'content-type: application/binary' \
  -b '__Secure-ENID=28.SE=B2m-HI9PXoKfpORkUmahZ3NzYW-gOdCLgcRR-Gt0zYmUlOtTNmVjpSkJhy5mpGhvYVwYGB1EZbhc8fDAbfR-UFlJ1dWd9LHnDld4covsa1M8_-M-gv168iFn6sGMLoEknom2Kssm_r0A0vaueG8PcN8bn1TR_AiBailWAwiSaVlixGZ70naOBJ969YmWcI2qXw-FWzaxaX49uMTSFYvhlpOsUS2Lq7jtIb91YC5ZGOH7rF5gHD3Uab0zlgqkeq5reqOV0kDsL_anvRbgOfPr98sTniN7owEjoJx5BEPaZDiVaI2KerAHmpmyesKOkfh9_Drf9aS-_7BVrjo1kNBpqpqr-tcqKJypQ8Amuaw7g2CRz9-N3YgdLAeUAf0f0SJs9fGrwEWckRnMd45h2jTEe5lutIkBKZjQU7Wk; SEARCH_SAMESITE=CgQIk54B; SID=g.a000xwijPP7BWiq8jFeq4OWg2ocP37Vxlze8EzfKV5lQ8ttljfTlj_vxYIMBYvjDcsrfdUNcWQACgYKAd8SARISFQHGX2MiObtxh_ZYoQqBfqPI6C1NvRoVAUF8yKrxv3TaR-CTnlV2-Imq4H0f0076; __Secure-1PSID=g.a000xwijPP7BWiq8jFeq4OWg2ocP37Vxlze8EzfKV5lQ8ttljfTln9ZAivYD3P3ujT1dkVGXVAACgYKAT0SARISFQHGX2Mi5cd8WtWBoZCk1GqWBwTsIRoVAUF8yKrRVWnV2H2-HcSqsX4U1yK_0076; __Secure-3PSID=g.a000xwijPP7BWiq8jFeq4OWg2ocP37Vxlze8EzfKV5lQ8ttljfTlR14ITiCJe4mgUhRMXUIwcAACgYKAcgSARISFQHGX2MiMPMkQolW1gXD-CsWHEiXARoVAUF8yKokUtDWa5dt4BFDPFhKPNDR0076; HSID=A28sHHKRpEAJGAal_; SSID=AXzNaSerH0tTBDJRS; APISID=WlHwOamnac_R0cIA/A-OxubF3AHDWlYvJB; SAPISID=h-hETQjl_wj4k4mr/A-yRUarGluz6TtixP; __Secure-1PAPISID=h-hETQjl_wj4k4mr/A-yRUarGluz6TtixP; __Secure-3PAPISID=h-hETQjl_wj4k4mr/A-yRUarGluz6TtixP; AEC=AVh_V2gTP7OHNIS-382AiP6MZU4-CcJY0Zu4E2a9chmmYlk4MCDxc8CmPQ; NID=524=VQpHLoB4Dn_ZBKQbZ-Ykq0-BqSkSojbgbDG31LN4a2T8FsasTKpzN5IwE45Yl7Bf60m8KMrHAS1fiWZaSOE3RBAXKAgy3CkHJgqFtL4ZLBEELfYUW0hT6FdklqWBpRjTlH7ssX_1JMzVg95F46ZYatX6e1qmHiQqcsS-K2DMnr0TSH6b6tuxxhltyjjAL3LAX3d362baVGRDFlfx8HGhzhSN8aPMhiIpuvo5rOreyNDT3Fw0A7aZC4EOGlEo4q5khI1tyr9fnyYytS4wdwMe808Bh41XdxdqPtRn5piI9_cfGGIutwThSFS_23bhjD6-Wj-VEh6HUve3hvNI_j3PiEC1P_6iuiKrSMVel15NGKnjeDxK7z8h7WnprJgTVOz6emuxrA6oxXwGs2hdai0_uOxW_aoPL26Ba39P5Ajduo8qpH0PtCb5LLin8nCJVawXTya_lL511fZsQDLg522_XFqy0RXXbuUxuQUBoBxXu_TlsVzCdgxo_N6B3z0XpE9CZnxpON5QVTrEdObIJhniccLJPJL7Eq6vITRz6w-mBUV_1sMExSebjwRhkTL5IiaM_z1r26QrrdaGNLUm1R8LUWlrnUZtfbGHh8DOOCtuZG9ACtaduj5d1Zjt1iBZQWZPpk1CpcaqFbPRr-_oOt0z4xrVgaP-f_NzjoJGNj63BawVRVjn0-bmxW5EpZifEam76ZcytmUoHf8fdGBbo5HX-zTitm_nRcFBePiqimQO3oaECV6u1RkUex8iQcjapzFcDauwXJu3VtbPnUrRmnDoGjVuWXJnBSiLYqm80DYkYyIRfTOyVzqwl50ejg; __Secure-1PSIDTS=sidts-CjEB5H03P1aeghtOqEq8xmRz6SGi0R5PDua0CnTjaVOOdurt_PUkHKpFXRhP8wQQl6IVEAA; __Secure-3PSIDTS=sidts-CjEB5H03P1aeghtOqEq8xmRz6SGi0R5PDua0CnTjaVOOdurt_PUkHKpFXRhP8wQQl6IVEAA; SIDCC=AKEyXzW4EEIh9nDP8Q8w1bHcAw03URfFUG5YJt_7wPGFAf9ozhsG1CJiFmsPc9W6LlmtVkaP5NY; __Secure-1PSIDCC=AKEyXzVK9vhmFCbpDdyaraZ6JZ03Orcr_uRPu5fgisnLGCnz75fVGlAXhI_9kAmDoPHVkvvsuKU; __Secure-3PSIDCC=AKEyXzUohGrzY5TZGpYOppvln8NWrENgHBIgnHTJkzPRfFFF1kq7uA-pO6Uwe5GrW59uxqQEcGT2' \
  -H 'origin: https://gemini.google.com' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H 'referer: https://gemini.google.com/' \
  -H 'sec-ch-ua: "Chromium";v="136", "Not.A/Brand";v="99", "Google Chrome";v="136"' \
  -H 'sec-ch-ua-arch: "x86"' \
  -H 'sec-ch-ua-bitness: "64"' \
  -H 'sec-ch-ua-form-factors: "Desktop"' \
  -H 'sec-ch-ua-full-version: "136.0.7103.113"' \
  -H 'sec-ch-ua-full-version-list: "Chromium";v="136.0.7103.113", "Not.A/Brand";v="99.0.0.0", "Google Chrome";v="136.0.7103.113"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-model: ""' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-ch-ua-platform-version: "15.0.0"' \
  -H 'sec-ch-ua-wow64: ?0' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36' \
  -H 'x-goog-authuser: 0' \
  --data-raw $'\u001f\u008b\u0008\u0000\u0000\u0000\u0000\u0000\u0000\n\u0095\u0095Ûrâ8\u0010\u0086_eK·#\u0088\u008e>lÕ\\´eãa8$\u0006<\u0013¯p¥\u0008°Â\u0021Ä`\u000e&lí»o9\u0021\u0090\u0099J*Y]¨J\u009fº[­î_¶Ö\u0014?lïï?=é· :Ìjª\u008b\u008e\u008bÛ|u3Z¯³õfô°©Ý\u008e\u008aI­\u009cÞÖÖÓb7-n\u0018a\u0092XDÔ\u0089¼Y²£\u008fÖ\u001a©Y\u0091/²í\u0002aD¹\u0085R¬Q7ßÔáÂ+F\u000f\u0013\u0084\u0091ë>Á0ÏÍýô\u008f\'óé\u008bq\u008a\u0009F?³\u0087I^®+&ë¤N\u0010F{ÇB\u0018=[ÕIÝ¦\u0084×)åU \u0081I\u009a¦\u0098\u0011\u008b`­\u0011µ\u0085Ë\u0008\u0091\\8¶\u008b>¨\u0002Òì\u0098ø\u0010I%\u0004s\u001bP#\u0081R5Á\u0003Z\u0003\u009f\u0089\u009aï\u0012áJ[2_\u0092\u0021Â\u009a¤X\u0093§3?\u008a^c\u008eCÈ±Ô\u001a)èôYÙ\u009cðòúïùj\u001cyÝ[Û3\u0083À3\u0097\u0019\u0087Ø·\u009dl\u001f\u0098Ë\u0081\u008c\u0012ßj\u008a\u0006|\u0099uÁ¹\u000fÀÙ~ç\u0090(§k\u0014ì\u0006?=Ó\u001eå&ñ\u001f\u0021RÎn\u001eÂÒd°\u009d¶½èR\u0096Q¢èA¨¢;\u000f¡Øí¼<jÂrû\u0000å\u0015»7\u0089\u009fµE\u0008Ëé\u000fÏ\\í{æêÚ\u008b®fQ\u0019\u008e\u000feâ«²m²2\u0081ý¢©L?ò\u008b1\u0084Pä\u0019¬bµ\u009cÏÕv¶Vß¢\u0096ç\u0081Ý\u0006Ó\n\u001b¦ýøÍ´gK\u0013ûy/ögÑÈ\u0089Á6^Ôrà"\u0008Ø÷ \u0004·lÂª³\u0081\u008d\u001c\u0083\u0015ßz²Ó\u0080µ\u0098ÀÈ´a\'\u0094\u0084Ø\u009fîºýy\u000f`\u0009\u001dµéÏãÇ\u009e£.TSåP¶\u0016-\u0011z\u0009Yx­ýÄû+ða5\u001flýÈ\u009fE±Z\u000c@\u001dú\u0089_ô\u0002%ýDåû\\É}\u000cw¼Ó(÷\u008eâ\u009ePëf\u0014BÞ1Up(¼\u000ed\u0081²³fàÄë\u0086Û\u009f7øa\u001cä \u001a_¢¦r"¡\u000e=¡²»D\u00912QwûÒ\u009f©D\u0009o¬V~©\u008aë\u008eZFe£0Âw\u0085\u0013Â.i\u0080ùúµRí[ígü\u0017¥iý"MjY6%\u0084àJF\u0098ñ×î\u009a\u0011.ÈQ\u0095ÿóM¿\u008aòÏ\u0010Qf\rÑ\u009fZ\u000f\u007f}\u0012Ã*Ý\u0021bT<í2|NKbW\u0090ç\u0091bÍ(\u0096TZ/KÍ\u0019¦X¿Îu\u0088.FËå°z\u0084ÌÅì(tf?»¤XSñ&\u0095oRëMJNTÊ3¥\'jKNN\u009c\u009f­\u001d\u0087Ùn5RL\u0009ÇC4cO\u0089òsJ\u008ek\u009dCrþ\u008aÛÖ\u0089\u000b»â\u001csf\u001fãUP¾@ç|¸¤\'HÏîî3¬\n|¶d\u0015\u0014\u0098Jñê¦\u000c\u008bß\u008aþ\u008e®\u0008\u0096\u0098¥é¿ïlë4­Z|êº\u0090\u008c|ø\u0021ü\u008c¦ôû?\u008eÏN\u0094pÊ%\u0091Õ\u008dÝ4ý\u000fæ\u0013\u000e\u0094¶\u0006\u0000\u0000'
    
    
    """
    curl_parser = CurlParser(curl_str)
    print(curl_parser.get_cookie())