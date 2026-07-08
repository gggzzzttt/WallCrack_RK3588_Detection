import socket
import json
import time

# 本地本机仿真，改127.0.0.1
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8888
PROTO_HEADER = b"CRACK_DATA"

def send_crack_data(img_bytes: bytes, detect_result: dict):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        print("[1] 测试服务器连接...")
        sock.connect((SERVER_IP, SERVER_PORT))
        print(f"✅ 已连接上位机 {SERVER_IP}:{SERVER_PORT}")

        sock.sendall(PROTO_HEADER)

        send_json = {
            "device_id": "RK3588_001",
            "timestamp": int(time.time()),
            "crack_count": detect_result["crack_count"],
            "max_width": detect_result["max_width"],
            "max_length": detect_result["max_length"],
            "avg_width": detect_result["avg_width"],
            "confidence": detect_result["avg_conf"],
            "crack_details": detect_result["crack_list"]
        }
        json_bin = json.dumps(send_json).encode("utf-8")
        sock.sendall(len(json_bin).to_bytes(4, byteorder="big") + json_bin)
        sock.sendall(len(img_bytes).to_bytes(4, byteorder="big") + img_bytes)

        print("✅ JSON数据+图片全部上传完成")
        sock.close()
    except Exception as e:
        print(f"❌ 上传失败: {e}")

if __name__ == "__main__":
    real_detect_data = {
        "crack_count": 2,
        "max_width": 2.3,
        "max_length": 18.6,
        "avg_width": 1.7,
        "avg_conf": 0.872,
        "crack_list": [
            {"width":2.3, "length":18.6, "conf":0.89},
            {"width":1.1, "length":9.2, "conf":0.85}
        ]
    }
    # Windows根目录放result.jpg
    with open("./result.jpg", "rb") as f:
        frame_bin = f.read()
    send_crack_data(frame_bin, real_detect_data)