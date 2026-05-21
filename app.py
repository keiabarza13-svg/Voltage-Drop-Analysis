import sys
import threading
import webbrowser
import tkinter as tk
from flask import Flask, render_template, request
from calculations import perform_vd_analysis

app = Flask(__name__)

# --- YOUR FLASK ROUTES (Kept Exactly The Same) ---

@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/calculator')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    user_data = {
        'voltage': request.form.get('voltage'),
        'load_current': request.form.get('load_current'),
        'distance': request.form.get('distance'),
        'wire_size': request.form.get('wire_size', '125'),
        'installation': request.form.get('installation', 'PVC Conduit'),
        'material': request.form.get('material', 'Copper'),
        'system_type': request.form.get('system_type', 'Three Phase'),
        'n_parallel': request.form.get('n_parallel', 1),
        'temp_conductor': request.form.get('temp_conductor', 75),
        'from_point': request.form.get('from_point', 'POINT A'),
        'to_point': request.form.get('to_point', 'POINT B')
    }

    analysis_result = perform_vd_analysis(user_data)
    return render_template('solution.html', res1=analysis_result, res2=analysis_result)


@app.route('/analyze', methods=['POST'])
def analyze():
    def get_data(prefix):
        return {
            "location": request.form.get(f'{prefix}_name'),
            "system_type": request.form.get(f'{prefix}_system_type'),
            "voltage": request.form.get(f'{prefix}_voltage'),
            "material": request.form.get(f'{prefix}_material'),
            "wire_size": request.form.get(f'{prefix}_wire_size'),
            "installation": request.form.get(f'{prefix}_install'),
            "n_parallel": request.form.get(f'{prefix}_n', 1),
            "distance": request.form.get(f'{prefix}_dist', 0),
            "load_current": request.form.get(f'{prefix}_load', 0),
            "temp_conductor": request.form.get(f'{prefix}_temp', 75),
            "desired_vd": request.form.get(f'{prefix}_limit', 3.0)
        }

    data_l1 = get_data('l1')
    data_l2 = get_data('l2')

    try:
        limit_to_send = float(data_l1['desired_vd'])
    except ValueError:
        limit_to_send = 3.0 

    res1 = perform_vd_analysis(data_l1)
    res2 = perform_vd_analysis(data_l2)

    return render_template(
        'solution.html', 
        res1=res1, 
        res2=res2,
        vd_limit=limit_to_send
    )

# --- STANDALONE WINDOW LAUNCHER CONTROLS ---

def run_flask():
    # Launches the Flask backend engine locally
    app.run(port=5000, debug=False, use_reloader=False)

def open_browser():
    # Automatically pulls up the frontend local link
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    # 1. Spin up the Flask backend script in an independent thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

  # 2. Open a standard window desktop launcher panel for your professor
    root = tk.Tk()
    root.title('CDM | Voltage Drop Analyzer')
    
    # Safely load the window icon so it never crashes the application
    try:
        import os
        # Checks if running via the compiled executable path
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, 'app_icon.ico')
        else:
            icon_path = 'app_icon.ico'
            
        root.iconbitmap(icon_path)
    except Exception:
        # If the file is missing for any reason, bypass it silently instead of crashing
        pass

    root.geometry("450x250")

    status_label = tk.Label(
        root, 
        text="Voltage Drop Analysis Engine Active", 
        font=("Arial", 14, "bold"), 
        fg="#2e7d32", 
        bg="#f4f6f9"
    )
    status_label.pack(pady=25)

    info_label = tk.Label(
        root, 
        text="Click below to open your software interface:", 
        font=("Arial", 10), 
        fg="#555555", 
        bg="#f4f6f9"
    )
    info_label.pack(pady=5)

    launch_btn = tk.Button(
        root, 
        text="Launch Analyzer Application", 
        command=open_browser, 
        font=("Arial", 11, "bold"), 
        bg="#1565c0", 
        fg="white", 
        padx=20, 
        pady=8,
        activebackground="#0d47a1",
        activeforeground="white",
        cursor="hand2"
    )
    launch_btn.pack(pady=20)

    # 3. Maintain desktop window instance active
    root.mainloop()