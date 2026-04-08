import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

def run_as_root(command):
    # 'tsu' is the standard way to call root in Termux
    full_cmd = f"tsu -c '{command}'"
    result = subprocess.check_output(full_cmd, shell=True).decode('utf-8')
    return result

@app.route('/get_apps')
def get_apps():
    # Lists all installed system packages
    apps = run_as_root("pm list packages -s")
    return {"packages": apps.splitlines()}

@app.route('/disable', methods=['POST'])
def disable_app():
    package_name = request.json['package']
    # Disables the app safely
    run_as_root(f"pm disable-user --user 0 {package_name}")
    return {"status": "success"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

