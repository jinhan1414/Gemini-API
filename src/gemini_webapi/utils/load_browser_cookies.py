from .logger import logger
from .optimized_http_parser import CurlParser


def load_browser_cookies(domain_name: str = "", verbose=True) -> dict:
    """
    Try to load cookies from all supported browsers and return combined cookiejar.
    Optionally pass in a domain name to only load cookies from the specified domain.

    Parameters
    ----------
    domain_name : str, optional
        Domain name to filter cookies by, by default will load all cookies without filtering.
    verbose : bool, optional
        If `True`, will print more infomation in logs.

    Returns
    -------
    `dict`
        Dictionary with cookie name as key and cookie value as value.
    """

    # import browser_cookie3 as bc3

    cookies = {}
    # for cookie_fn in [
    #     # bc3.chrome,
    #     # bc3.chromium,
    #     # bc3.opera,
    #     # bc3.opera_gx,
    #     # bc3.brave,
    #     bc3.edge,
    #     # bc3.vivaldi,
    #     # bc3.firefox,
    #     # bc3.librewolf,
    #     # bc3.safari,
    # ]:
    #     try:
    #         for cookie in cookie_fn(domain_name=domain_name):
    #             cookies[cookie.name] = cookie.value
    #     except bc3.BrowserCookieError:
    #         pass
    #     except PermissionError as e:
    #         if verbose:
    #             logger.warning(
    #                 f"Permission denied while trying to load cookies from {cookie_fn.__name__}. {e}"
    #             )
    #     except Exception as e:
    #         if verbose:
    #             logger.error(
    #                 f"Error happened while trying to load cookies from {cookie_fn.__name__}. {e}"
    #             )

    curl_str = """
      curl 'https://play.google.com/log?format=json&hasfast=true&authuser=0' \
    -H 'accept: */*' \
    -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
    -H 'cache-control: no-cache' \
    -H 'content-encoding: gzip' \
    -H 'content-type: application/binary' \
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
    cookies = curl_parser.get_cookie()

    return cookies
