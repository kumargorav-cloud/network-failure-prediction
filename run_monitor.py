import subprocess

print("Running collector...")
subprocess.run(["python3","collector.py"])

print("Updating baseline (if possible)...")
subprocess.run(['python3',"baseline_learner.py"])

print("Calculating risk...")
subprocess.run(['python3',"risk_engine.py"])
