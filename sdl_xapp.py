from ricxappframe.xapp_frame import Xapp
import time
import json

# Configuration
SDL_NAMESPACE = "ue-metrics"
TARGET_UE_KEY = "ue_12345_metrics"

def entrypoint(self):
    print("--- SECURITY SDL XAPP STARTING (V5) ---", flush=True)
    counter = 0

    while True:
        try:
            # 1. READ
            retrieved_data = self.sdl_get(SDL_NAMESPACE, TARGET_UE_KEY)
            
            # --- DEBUGGING: Let's see exactly what SDL gave us ---
            print(f"[DEBUG] Type received: {type(retrieved_data)}", flush=True)
            print(f"[DEBUG] Raw data: {retrieved_data}", flush=True)
            
            current_metrics = None
            raw_val = None

            # 2. EXTRACT VALUE (Handle both Dict and Direct Return)
            if retrieved_data is not None:
                if isinstance(retrieved_data, dict):
                    raw_val = retrieved_data.get(TARGET_UE_KEY)
                else:
                    # If it's a string/bytes, it returned the value directly!
                    raw_val = retrieved_data

            # 3. CLEAN AND PARSE JSON
            if raw_val is not None:
                if isinstance(raw_val, bytes):
                    raw_val = raw_val.decode('utf-8', errors='ignore')
                
                # Strip MessagePack/RIC header garbage
                if isinstance(raw_val, str) and "{" in raw_val:
                    json_start = raw_val.find("{")
                    clean_json_str = raw_val[json_start:]
                    
                    try:
                        current_metrics = json.loads(clean_json_str)
                        print(f"[SDL] Successfully parsed! Current throughput: {current_metrics.get('throughput')}", flush=True)
                    except json.JSONDecodeError as jde:
                        print(f"[SDL ERROR] JSON Parse Failed: {jde} on string: {clean_json_str}", flush=True)

            # 4. INITIALIZE IF NEEDED
            if current_metrics is None:
                print(f"[SDL] Key not found or empty. Initializing...", flush=True)
                current_metrics = {
                    "ue_id": "IMSI0012345",
                    "throughput": 0,
                    "signal_strength": -90,
                    "update_count": 0
                }

            # 5. MODIFY
            current_metrics["throughput"] += 5
            current_metrics["update_count"] += 1
            current_metrics["timestamp"] = time.time()

            # 6. WRITE
            payload_json = json.dumps(current_metrics)
            
            # Using the exact 3-argument signature your library requires
            self.sdl_set(SDL_NAMESPACE, TARGET_UE_KEY, payload_json)

            print(f"[SDL] Loop {counter}: Updated throughput to -> {current_metrics['throughput']}\n", flush=True)

            counter += 1
            time.sleep(2)

        except Exception as e:
            print(f"[SDL ERROR] Exception: {e} | Type: {type(e).__name__}", flush=True)
            time.sleep(5)

if __name__ == "__main__":
    xapp = Xapp(
        entrypoint=entrypoint, 
        rmr_port=4560, 
        rmr_wait_for_ready=False, 
        use_fake_sdl=False
    )
    xapp.run()
