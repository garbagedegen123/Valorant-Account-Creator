import httpx, json, random, os, sys, ctypes, pyfiglet, time, string, threading; from itertools import cycle

class bcolors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class returnProxy:
    def GetProxy():
        with open('./Data/Proxies.txt', 'r') as temp_file:
            proxy = [line.rstrip('\n') for line in temp_file]
            return proxy
    proxy=GetProxy()
    proxy_pool = cycle(proxy)
    def GetProxies():
        proxy = next(returnProxy.proxy_pool)
        if len(proxy.split(':')) == 4:
            splitted = proxy.split(':') 
            return f"http://{splitted[2]}:{splitted[3]}@{splitted[0]}:{splitted[1]}" # Converts ip:port:user:pass format to user:pass@ip:port. could be made better but it works
        else:
            return f'http://{proxy}'


class Valorant:
    def __init__(self):
        self.config = json.load(open('./config.json'))
        self.api_key = self.config['capmonster_api_key']
        self.set_title()
        self.logo()
    
    def set_title(self):
        if os.name == 'nt':
            ctypes.windll.kernel32.SetConsoleTitleW(f"ClipValGen | clipssender#2940 | https://discord.gg/clipssender")
        else:
            ctypes.windll.kernel32.SetConsoleTitleW(f"ClipValGen | clipssender#2940 | https://discord.gg/clipssender")

    def logo(self):
        os.system('cls')
        print(pyfiglet.figlet_format(f"ClipValGen"))
        print(f"{bcolors.RED}Author: clipssender#2920{bcolors.RESET}")
    
    def get_captcha_key(self) -> str:

        task_payload = {
            'clientKey': str(self.config['capmonster_api_key']),
            'task': {
                "type":"HCaptchaTaskProxyless",
                "isInvisible": True,
                "nocache": True,
                "websiteURL":"https://auth.riotgames.com/login#client_id=play-valorant-web-prod&nonce=NzcsMTA2LDEwMCwx&prompt=signup&redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in%2F%3Fredirect%3D%2Fdownload%2F&response_type=token%20id_token&scope=account%20openid&state=c2lnbnVw&ui_locales=it",
                "websiteKey":"a010c060-9eb5-498c-a7b9-9204c881f9dc",
                "userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36" if str(self.config["useragent"])=="" else str(self.config["useragent"]) #change this to ur useragent for better results
                            }
        }
        key = None

        with httpx.Client(headers={'content-type': 'application/json', 'accept': 'application/json'},
                          timeout=30) as client:
            try:
                task_id = client.post(f'https://api.capmonster.cloud/createTask', json=task_payload).json()["taskId"]
                print(f'Recieved captcha task ID: {task_id}')

                get_task_payload = {
                    'clientKey': str(self.config['capmonster_api_key']),
                    'taskId': task_id
                }

                while key is None:
                    try:
                        response = httpx.post(f'https://api.capmonster.cloud/getTaskResult',
                                               json=get_task_payload,
                                               timeout=30).json()

                        if 'ERROR_PROXY_CONNECT_REFUSED' in str(response):
                            
                            
                            return 'ERROR'

                        if 'ERROR' in str(response):
                            
                            return 'ERROR'

                        if response['status'] == 'ready':
                            key = response["solution"]["gRecaptchaResponse"]
                        else:
                            time.sleep(3)
                    except Exception as e:

                        if 'ERROR_PROXY_CONNECT_REFUSED' in str(e):
                            
                            key = 'ERROR'
                        else:
                            pass

                
                return key

            except Exception as e:
                print(f'Captcha task result error: {e}')

                if 'ERROR_PROXY_CONNECT_REFUSED' in str(e):
                    
                    
                    return 'ERROR'
                else:
                    pass


    def creator(self):
        while True:
            try:
                
                client = httpx.Client(
                http2=True, 
                timeout=30, 
                cookies={"locale": "en-US"},
                headers={
                'accept':'*/*',
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'en-GB,en-US;q=0.9,en;q=0.8',
                'access-control-request-headers':'content-type',
                'access-control-request-method':'POST',
                'connection':'keep-alive',
                'host':'signup-api.riotgames.com',
                'origin':'https://auth.riotgames.com',
                'referer':'https://auth.riotgames.com/',
                'sec-fetch-dest':'empty',
                'sec-fetch-mode':'cors',
                'sec-fetch-site':'same-site',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36' if str(self.config["useragent"])=="" else str(self.config["useragent"])
            },
            proxies=returnProxy.GetProxies()
            )
                username=''.join(random.choices(string.ascii_letters + string.digits, k=6))
                email = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + "@discordapp.com"
                password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
                response=client.post('https://signup-api.riotgames.com/v1/accounts', json={
                           "tou_agree": True,
                           "newsletter": True,
                           "date_of_birth": "1999-12-23" if self.config["customDOB"]==False else str(self.config["customdob"]),
                           "email": f"{email}",
                           "username": f"{username}",
                           "password": f"{password}",
                           "confirm_password": f"{password}",
                           "client_id": "play-valorant-web-prod",
                           "redirect_uri": "https://playvalorant.com/opt_in/?redirect=/download/",
                           "locale": "it",
                           "token": f"hcaptcha {self.get_captcha_key()}"
                })
                if response.status_code in [204, 200]:
                    token=response.json()['token']
                    print(f'{bcolors.GREEN}[+]{bcolors.RESET}{bcolors.CYAN} Account Created: {username}:{password} | Token: {token[:35]}... {bcolors.RESET}')
                    with open('output/accounts.txt', 'a') as f:
                        f.write(f'{username}:{password}\n')
                    with open('output/tokens.txt', 'a') as f:
                        f.write(f'{token}\n')
                    with open('output/accounts_full.txt', 'a') as f:
                        f.write(f'{email}:{password}:{token}\n')
                        continue
                else:
                    print(f'{bcolors.RED}[-]{bcolors.RESET}{bcolors.CYAN} Failed to Create Account {bcolors.RESET}')






                #print(f'{bcolors.GREEN}[+]{bcolors.RESET}{bcolors.CYAN} Attempting to Log into Account: {username}:{password} {bcolors.RESET}')
                #client.get('https://auth.riotgames.com/api/v1/authorization')
                #response=client.put('https://auth.riotgames.com/api/v1/authorization', json={"type":"auth","username":{username},"password":{password},"remember":False,"language":"en_US"})
                #print(response.text)
                #if response.status_code==200:
                #    print(f'{bcolors.RED}[+]{bcolors.RESET}{bcolors.GREEN} Logged into Account: {username}:{password} {bcolors.RESET}')
                #    game_name=''.join(random.choices(string.digits, k=3))
                #    response=httpx.post('https://account.riotgames.com/api/riot-id?email_locale=en_US', headers=client.headers,cookies=client.cookies, json={"game_name":f"clipdaddy{game_name}","tag_line":"3131"})
                #    if response.status_code==200:
                #        print(f'{bcolors.RED}[+]{bcolors.RESET}{bcolors.GREEN} Created Riot ID: clipdaddy{game_name} | {username}:{password} {bcolors.RESET}')
                #else:
                #    print('Failed to log into account') 
    
                #response=client.post('https://auth.riotgames.com/api/v1/signup', json={
                #    "token": f"{self.token}",
                #    "locale": "it"
                #})
                #print(response.text)
                #if response.status_code in [204, 200]:
                #    print(f'{bcolors.GREEN}[+]{bcolors.RESET} Account Created: {self.username}:{self.password} | Token: {self.token[:20]} {bcolors.RESET}')
                #    with open('output/accounts.txt', 'a') as f:
                #        f.write(f'{self.username}:{self.password}\n')
                #    with open('output/tokens.txt', 'a') as f:
                #        f.write(f'{self.token}\n')
                #    with open('output/accounts_full.txt', 'a') as f:
                #        f.write(f'{self.email}:{self.password}:{self.token}\n')
                #else:
                #    print(f'{bcolors.RED}[-] Failed to Create Account')
    
            except:
                pass
    

    def main(self):
        try:
            threadamount=int(input(f'{bcolors.GREEN}Thread Amount: '))
            for i in range(threadamount):
                thread=threading.Thread(target=self.creator)
                thread.start()
            for i in range(threadamount):
                thread.join()
        except KeyboardInterrupt:
            sys.exit()

if __name__=="__main__":
    try:
       Valorant().main()
    except KeyboardInterrupt:
        sys.exit()