# qube3_smoke_test.py
import sys
from array import array

CANDIDATE_DEVICES = [
    ("qube_servo3_usb", "0"),
    ("qube_servo3_usb", "1"),
]

# Channel arrays (use unsigned int like Quanser examples)
AO_CH  = array('I', [0])        # analog output channel(s)
AO_BUF = array('d', [0.0])      # voltage buffer (same length as AO_CH)
AO_N   = len(AO_CH)

ENC_CH  = array('I', [0, 1])    # encoder channel(s)
ENC_BUF = array('i', [0, 0])    # encoder count buffer (int)
ENC_N   = len(ENC_CH)

def try_open(device: str, device_id: str) -> bool:
    from quanser.hardware import HIL  # provided by Quanser SDK

    hil = HIL()
    print(f"Trying open: device='{device}', id='{device_id}' ...")

    try:
        hil.open(device, device_id)
    except Exception as e:
        print(f"  Open failed: {e}")
        return False

    try:
        # Always start safe: motor command = 0V
        try:
            hil.write_analog(AO_CH, AO_N, AO_BUF)
        except Exception as e:
            print(f"  write_analog failed (channel mapping may differ): {e}")

        # Read encoders
        try:
            hil.read_encoder(ENC_CH, ENC_N, ENC_BUF)
            print(f"  Encoder counts: {list(ENC_BUF)}")
        except Exception as e:
            print(f"  read_encoder failed (channel mapping may differ): {e}")

        print("  SUCCESS opening device.")
        return True

    finally:
        # Make sure motor is off
        try:
            hil.write_analog(AO_CH, AO_N, AO_BUF)
        except Exception:
            pass
        hil.close()

def main():
    ok = False
    for dev, dev_id in CANDIDATE_DEVICES:
        if try_open(dev, dev_id):
            ok = True
            break

    if not ok:
        print("\nCould not open device with the candidate names/IDs.")
        print("Next: we’ll confirm the exact device name/ID and channel map from Quanser examples/docs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
