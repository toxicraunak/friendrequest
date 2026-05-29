from flask import Flask, request, jsonify
import requests
import json
import threading
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
from protobuf import my_pb2, output_pb2
from byte import Encrypt_ID, encrypt_api
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

app = Flask(__name__)

AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

def encrypt_message(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    return cipher.encrypt(padded_message)

def parse_response(response_content):
    response_dict = {}
    lines = response_content.split("\n")
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            response_dict[key.strip()] = value.strip().strip('"')
    return response_dict

def get_token(uid, password):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    
    headers = {
        "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    
    try:
        r = requests.post(url, headers=headers, data=data, verify=False)
        j = r.json()
        
        token = (j.get("access_token") or j.get("token") or j.get("session_key") or j.get("jwt") or (j.get("data") or {}).get("token"))
        
        if not token:
            return None
        
        open_id = j.get('open_id', '')
        access_token = token
        
        game_data = my_pb2.GameData()
        game_data.timestamp = "2024-12-05 18:15:32"
        game_data.game_name = "free fire"
        game_data.game_version = 1
        game_data.version_code = "1.123.1"
        game_data.os_info = "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)"
        game_data.device_type = "Handheld"
        game_data.network_provider = "Verizon Wireless"
        game_data.connection_type = "WIFI"
        game_data.screen_width = 1280
        game_data.screen_height = 960
        game_data.dpi = "240"
        game_data.cpu_info = "ARMv7 VFPv3 NEON VMH | 2400 | 4"
        game_data.total_ram = 5951
        game_data.gpu_name = "Adreno (TM) 640"
        game_data.gpu_version = "OpenGL ES 3.0"
        game_data.user_id = "Google|74b585a9-0268-4ad3-8f36-ef41d2e53610"
        game_data.ip_address = "172.190.111.97"
        game_data.language = "en"
        game_data.open_id = open_id
        game_data.access_token = access_token
        game_data.platform_type = 4
        game_data.device_form_factor = "Handheld"
        game_data.device_model = "Asus ASUS_I005DA"
        game_data.field_60 = 32968
        game_data.field_61 = 29815
        game_data.field_62 = 2479
        game_data.field_63 = 914
        game_data.field_64 = 31213
        game_data.field_65 = 32968
        game_data.field_66 = 31213
        game_data.field_67 = 32968
        game_data.field_70 = 4
        game_data.field_73 = 2
        game_data.library_path = "/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/lib/arm"
        game_data.field_76 = 1
        game_data.apk_info = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/base.apk"
        game_data.field_78 = 6
        game_data.field_79 = 1
        game_data.os_architecture = "32"
        game_data.build_number = "2019117877"
        game_data.field_85 = 1
        game_data.graphics_backend = "OpenGLES2"
        game_data.max_texture_units = 16383
        game_data.rendering_api = 4
        game_data.encoded_field_89 = "\u0017T\u0011\u0017\u0002\b\u000eUMQ\bEZ\u0003@ZK;Z\u0002\u000eV\ri[QVi\u0003\ro\t\u0007e"
        game_data.field_92 = 9204
        game_data.marketplace = "3rd_party"
        game_data.encryption_key = "KqsHT2B4It60T/65PGR5PXwFxQkVjGNi+IMCK3CFBCBfrNpSUA1dZnjaT3HcYchlIFFL1ZJOg0cnulKCPGD3C3h1eFQ="
        game_data.total_storage = 111107
        game_data.field_97 = 1
        game_data.field_98 = 1
        game_data.field_99 = "4"
        game_data.field_100 = "4"
        
        serialized_data = game_data.SerializeToString()
        encrypted_data = encrypt_message(AES_KEY, AES_IV, serialized_data)
        
        url2 = "https://loginbp.ggblueshark.com/MajorLogin"
        headers2 = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/octet-stream",
            'Expect': "100-continue",
            'X-GA': "v1 1",
            'X-Unity-Version': "2018.4.11f1",
            'ReleaseVersion': "OB53"
        }
        
        response = requests.post(url2, data=encrypted_data, headers=headers2, verify=False)
        
        if response.status_code == 200:
            example_msg = output_pb2.Garena_420()
            example_msg.ParseFromString(response.content)
            parsed_resp = parse_response(str(example_msg))
            
            final_token = parsed_resp.get("token", "N/A")
            if final_token != "N/A":
                return final_token
            else:
                return None
        else:
            return None
            
    except Exception as e:
        return None

def load_accounts():
    try:
        accounts = []
        with open("accounts.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line and ":" in line:
                    uid, password = line.split(":", 1)
                    accounts.append({"uid": uid.strip(), "password": password.strip()})
        
        if len(accounts) > 100:
            accounts = accounts[:100]
        
        return accounts
    except Exception as e:
        return []

def send_friend_request(target_uid, token, account_uid):
    try:
        encrypted_id = Encrypt_ID(target_uid)
        payload = f"08a7c4839f1e10{encrypted_id}1801"
        encrypted_payload = encrypt_api(payload)

        url = "https://client.ind.freefiremobile.com/RequestAddingFriend"
        headers = {
            "Expect": "100-continue",
            "Authorization": f"Bearer {token}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB53",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "16",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-N975F Build/PI)",
            "Host": "clientbp.ggblueshark.com",
            "Connection": "close",
            "Accept-Encoding": "gzip, deflate, br"
        }

        response = requests.post(url, headers=headers, data=bytes.fromhex(encrypted_payload), verify=False)

        if response.status_code == 200:
            return True
        else:
            return False
            
    except Exception as e:
        return False

def process_account(account, target_uid, results, delay=0):
    if delay > 0:
        time.sleep(delay)
    
    uid = account.get("uid")
    password = account.get("password")
    
    if not uid or not password:
        results["failed"] += 1
        return
    
    token = get_token(uid, password)
    
    if token:
        success = send_friend_request(target_uid, token, uid)
        if success:
            results["success"] += 1
        else:
            results["failed"] += 1
    else:
        results["failed"] += 1

@app.route('/spam', methods=['GET'])
def spam_friend_requests():
    target_uid = request.args.get('uid')
    
    if not target_uid:
        return jsonify({"error": "uid parameter required"}), 400
    
    accounts = load_accounts()
    
    if not accounts:
        return jsonify({"error": "No accounts found in accounts.txt"}), 404
    
    results = {"success": 0, "failed": 0}
    
    threads = []
    thread_delay = 0.1
    
    for i, account in enumerate(accounts):
        thread = threading.Thread(
            target=process_account,
            args=(account, target_uid, results, i * thread_delay)
        )
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return jsonify({
        "target_uid": target_uid,
        "total_accounts": len(accounts),
        "successful_requests": results["success"],
        "failed_requests": results["failed"]
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)