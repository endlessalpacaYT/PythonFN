import datetime
import requests
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

ip = '0.0.0.0'
port = 3551

username = "PythonFN"
profiles_db = {}

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxMjMiLCJpYXQiOjE2MjUwMzgwMDB9.JcJmn5pEDw7HgnDxHjRbOyxJ9CfIEpO4ckhsv4Zo4_8"

def create_profile(account_id, profile_id, rvn):
    return {
        "accountId": account_id,
        "profileId": profile_id,
        "profileRevision": int(rvn) + 1,
        "profileCommandRevision": int(rvn) + 1,
        "profileChangesBaseRevision": int(rvn),
        "profileChanges": [],
        "profileData": {
            "displayName": f"User-{account_id}",
            "vbucks": 1000,
            "items": [
                {"itemId": "skin001", "name": "Default Skin"},
                {"itemId": "glider001", "name": "Basic Glider"}
            ]
        }
    }

def create_athena_profile(account_id, rvn):
    return {
        "accountId": account_id,
        "profileId": "athena",
        "profileRevision": int(rvn) + 1,
        "profileCommandRevision": int(rvn) + 1,
        "profileChangesBaseRevision": int(rvn),
        "profileChanges": [],
        "profileData": {
            "loadout": {
                "skin": "default_skin",
                "glider": "default_glider",
                "pickaxe": "default_pickaxe"
            },
            "quests": [
                {"questId": "quest001", "status": "in_progress", "progress": 50},
                {"questId": "quest002", "status": "not_started", "progress": 0}
            ],
            "completedQuests": []
        }
    }

# Made In Python 3.12, Will log alot of the routes for debugging

# Will make sure to comment alot cuz it was in the task and this is prolly going on github too :)

# This route is not needed but i will have it here anyway, PS: ive never used flask before help me :()
@app.route('/')
def home():
    return "Fortnite Backend in Python, For Homework!!!"

# First we will do auth routes, MOST IMPORTANT!!!

@app.route('/account/api/oauth/token', methods=['POST'])
def tokenmock():
    data = {
        "access_token": token,
        "expires_in": 28800,
        "expires_at": "9999-12-02T01:12:01.100Z",
        "token_type": "bearer",
        "refresh_token": token,
        "refresh_expires": 86400,
        "refresh_expires_at": "9999-12-02T01:12:01.100Z",
        "account_id": "PythonFN",
        "client_id": "PythonFN",
        "internal_client": True,
        "client_service": "fortnite",
        "displayName": username,
        "app": "fortnite",
        "in_app_id": "AccountId",
        "device_id": "PythonFN"
    }

    return jsonify(data)

@app.route('/account/api/oauth/verify', methods=['POST'])
def verify():
    data = {
        "access_token": token,
        "expires_in": 28800,
        "expires_at": "9999-12-02T01:12:01.100Z",
        "token_type": "bearer",
        "refresh_token": token,
        "refresh_expires": 86400,
        "refresh_expires_at": "9999-12-02T01:12:01.100Z",
        "account_id": "PythonFN",
        "client_id": "PythonFN",
        "internal_client": True,
        "client_service": "fortnite",
        "displayName": username,
        "app": "fortnite",
        "in_app_id": "AccountId",
        "device_id": "PythonFN"
    }

    return jsonify(data)

@app.route('/account/api/oauth/sessions/kill/<token>', methods=['POST'])
def killToken(token):
    return jsonify({"message": "session killed for token: " + token})

@app.route('/account/api/oauth/sessions/kill', methods=['POST'])
def kill(token):
    return jsonify({"message": "sessions killed"})

# Account Routes:

@app.route('/account/api/public/account/<account_id>', methods=['GET'])
def get_account(account_id):
    if account_id == "PythonFN":
        return jsonify({
            "accountId": account_id,
            "displayName": username,
            "externalAuths": []
        })
    else:
        return jsonify({"error": "Account not found"}), 404
    
@app.route('/api/v1/user/setting', methods=['GET'])
def user_setting():
    return jsonify({
        "settings": {
            "language": "en",
            "region": "NA"
        }
    }), 200

@app.route('/fortnite/api/game/v2/profile/<account_id>/client/QueryProfile', methods=['POST'])
def query_profile(account_id):
    profile_id = request.args.get('profileId', 'athena') 
    rvn = request.args.get('rvn', -1)  

    profile = profiles_db.get(profile_id)

    if not profile:
        profile = create_profile(account_id, profile_id, rvn)
        profiles_db[profile_id] = profile

    return jsonify({
        "profileId": profile["profileId"],
        "profileRevision": profile["profileRevision"],
        "profileChangesBaseRevision": profile["profileChangesBaseRevision"],
        "profileCommandRevision": profile["profileCommandRevision"],
        "serverTime": str(datetime.datetime.utcnow()),
        "responseVersion": 1,
        "profileData": profile["profileData"]
    }), 200

@app.route('/fortnite/api/game/v2/profile/<account_id>/client/ClientQuestLogin', methods=['POST'])
def client_quest_login(account_id):
    profile_id = request.args.get('profileId', 'athena')  
    rvn = request.args.get('rvn', -1) 

    profile = profiles_db.get(profile_id)

    if not profile:
        profile = create_athena_profile(account_id, rvn)
        profiles_db[profile_id] = profile

    return jsonify({
        "profileId": profile["profileId"],
        "profileRevision": profile["profileRevision"],
        "profileChangesBaseRevision": profile["profileChangesBaseRevision"],
        "profileCommandRevision": profile["profileCommandRevision"],
        "serverTime": str(datetime.datetime.now(datetime.timezone.utc)),
        "responseVersion": 1,
        "profileData": profile["profileData"]
    }), 200
    
# lightswitch api routes, (service status thingy)

@app.route('/lightswitch/api/service/Fortnite/status', methods=['GET'])
def fortnite_status():
    data = {
        "serviceInstanceId": "fortnite",
        "status": "UP",
        "message": "Fortnite is online",
        "maintenanceUri": None,
        "overrideCatalogIds": [
            "a7f138b2e51945ffbfdacc1af0541053"
        ],
        "allowedActions": [],
        "banned": False,
        "launcherInfoDTO": {
            "appName": "Fortnite",
            "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
            "namespace": "fn"
        }
    }
    return jsonify(data)

@app.route('/lightswitch/api/service/bulk/status', methods=['GET'])
def bulk_status():
    data = [{
        "serviceInstanceId": "fortnite",
        "status": "UP",
        "message": "fortnite is up.",
        "maintenanceUri": None,
        "overrideCatalogIds": [
            "a7f138b2e51945ffbfdacc1af0541053"
        ],
        "allowedActions": [
            "PLAY",
            "DOWNLOAD"
        ],
        "banned": False,
        "launcherInfoDTO": {
            "appName": "Fortnite",
            "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
            "namespace": "fn"
        }
    }]
    return jsonify(data)
    
# micelanous routes

@app.route('/datarouter/api/v1/public/data', methods=['POST'])
def data_router():
    return jsonify({"message": "Data received"}), 200

@app.route('/fortnite/api/game/v2/tryPlayOnPlatform/account/<path:account_id>', methods=['POST'])
def try_play_on_platform(account_id):
    # make it plain text because for some reason fortnite made it super hard to do with json or sum
    response = make_response("true")
    response.headers["Content-Type"] = "text/plain"
    return response

@app.route('/fortnite/api/game/v2/grant_access/<accountId>', methods=['POST'])
def grant_access(accountId):
    response = make_response("true")
    response.headers["Content-Type"] = "text/plain"
    return response

@app.route('/fortnite/api/game/v2/enabled_features', methods=['GET'])
def enabled_features():
    return jsonify({
        "features": ["battle_royale", "creative", "save_the_world"]
    }), 200

@app.route('/fortnite/api/storefront/v2/keychain', methods=['GET'])
def keychain():
    keychain_url = "https://cdn.pongodev.com/Fortnite/Stuff/keychain.json"
    
    response = requests.get(keychain_url)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Failed to fetch keychain"}), response.status_code
    
@app.route('/fortnite/api/game/v2/profile/<accountId>/client/SetMtxPlatform', methods=['POST'])
def set_mtx_platform(accountId):
    profile_id = request.args.get('profileId')
    rvn = request.args.get('rvn')

    if profile_id == "common_core":
        data = {
            "profileRevision": int(rvn) + 1,  
            "profileId": profile_id,
            "profileChanges": [],
            "profileCommandRevision": 2,
            "profileData": {
                "mtxPlatform": "PC",  
                "currencyBalance": 1000
            }
        }
        return jsonify(data), 200
    else:
        return jsonify({"error": "Profile not found or unsupported"}), 404

if __name__ == '__main__':
    # Self explanitory, just put your ip and port you wanna run it on
    # ip should ussually be 0.0.0.0 or 127.0.0.1, i like to do 0.0.0.0
    # port 3551 and 8080 is quite common ports for a fn backend, i just prefer 3551
    print(f"PythonFN running on http://{ip}:{port}")
    app.run(host=ip, port=port, debug=False)