from ricxappframe.xapp_frame import Xapp
import time
import json
import sys

SDL_NAMESPACE = "sec_project_ns"

def entrypoint(self):
    print("--- SECURITY XAPP STARTING ---", flush=True)
    counter = 0
    while True:
        try:
            # Create your key and payload
            target_key = f"ue_target_{counter}"
            payload_dict = {"ue_id": f"IMSI00{counter}", "timestamp": time.time()}
            
            # Serialize payload to a string
            payload_json = json.dumps(payload_dict)

            # FIX: Explicitly pass key and value as separate arguments
            # Most ricxappframe versions accept (namespace, key, value)
            self.sdl_set(SDL_NAMESPACE, target_key, payload_json)

            # For sdl_get, it returns the value directly for that key
            retrieved = self.sdl_get(SDL_NAMESPACE, target_key)

            print(f"[SDL] Loop {counter}: Success!", flush=True)
            print(f"[SDL] Written Key: {target_key}", flush=True)
            print(f"[SDL] Retrieved Data: {retrieved}", flush=True)

            counter += 1
            time.sleep(2)
            
        except Exception as e:
            # This will now catch and print if there is still a signature mismatch
            print(f"[SDL ERROR]: {e}", flush=True)
            time.sleep(5)

if __name__ == "__main__":
    # Initialize xApp
    # rmr_wait_for_ready=False is vital for SDL-only apps
    xapp = Xapp(entrypoint=entrypoint, rmr_port=4560, rmr_wait_for_ready=False, use_fake_sdl=False)
    xapp.run()
