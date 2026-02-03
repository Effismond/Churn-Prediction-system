import subprocess
import sys

PIPELINE_STEPS = [
    "pipelines.1_ingest",
    "pipelines.2_preprocess",   # ✅ FIXED
    "pipelines.3_train",
    "pipelines.4_predict",
]

for step in PIPELINE_STEPS:
    print(f"\n🚀 Running {step} ...")
    result = subprocess.run([sys.executable, "-m", step])

    if result.returncode != 0:
        print(f"\n❌ Pipeline stopped at {step}")
        sys.exit(1)

print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY")