import subprocess


print("processes:")

# Run the first Python file
subprocess.run(["python", "processes_test.py"])


print("""
threads:""")


# Run the second Python file
subprocess.run(["python", "threads_test.py"])
