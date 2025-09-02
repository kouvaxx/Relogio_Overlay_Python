import tkinter as tk
import time
import win32gui
import win32con
import win32api
import threading
import mss
import numpy as np
from collections import deque

# --- Configurações ---
BORDER = 5
MIN_WIDTH, MIN_HEIGHT = 60, 20
ALPHA_LEVELS = [0.85, 0.5, 0.2]
current_alpha_index = 0

# --- Variáveis de estado para o modo FPS ---
fps_mode_active = False
fps_thread = None

def update_time():
    """Atualiza o texto do relógio a cada segundo."""
    time_label.config(text=time.strftime('%H:%M'))
    root.after(1000, update_time)

# --- Loop do contador de FPS (executa em uma thread) ---
def fps_counter_loop():
    """Mede e exibe o FPS de forma precisa."""
    # deque é uma lista otimizada para adicionar e remover itens das pontas
    frame_times = deque(maxlen=60) # Armazena o tempo dos últimos 60 frames
    
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        
        while fps_mode_active:
            t_start = time.perf_counter()
            
            sct.grab(monitor) # Captura um frame
            
            t_end = time.perf_counter()
            frame_time = t_end - t_start
            frame_times.append(frame_time)
            
            # Calcula o FPS a partir da média dos tempos de frame
            if frame_times:
                avg_frame_time = np.mean(frame_times)
                fps = 1 / avg_frame_time if avg_frame_time > 0 else 0
                # Agenda a atualização da UI na thread principal
                root.after(0, lambda: fps_label.config(text=f"| {fps:.0f} FPS"))
            
            # Pequena pausa para não sobrecarregar a CPU com este loop
            time.sleep(0.001)

def toggle_fps_mode():
    """Inicia ou para o contador de FPS, mostrando ou escondendo o label."""
    global fps_mode_active, fps_thread
    fps_mode_active = not fps_mode_active
    
    if fps_mode_active:
        # Mostra o label de FPS
        fps_label.pack(side='left', padx=(0, 4), pady=2)
        
        # Inicia a thread do contador de FPS
        fps_thread = threading.Thread(target=fps_counter_loop, daemon=True)
        fps_thread.start()
    else:
        # Para o loop na thread (ele irá parar na próxima iteração)
        # e esconde o label de FPS
        fps_label.pack_forget()

def cycle_transparency():
    global current_alpha_index
    current_alpha_index = (current_alpha_index + 1) % len(ALPHA_LEVELS)
    new_alpha = ALPHA_LEVELS[current_alpha_index]
    root.attributes('-alpha', new_alpha)

def toggle_topmost():
    global is_topmost
    is_topmost = not is_topmost
    hwnd = win32gui.GetParent(root.winfo_id())
    rect = win32gui.GetWindowRect(hwnd)
    x, y, w, h = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
    if is_topmost:
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, w, h, 0)
        btn_pin.config(text='📌')
    else:
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, x, y, w, h, 0)
        btn_pin.config(text='📍')

# ... (as outras funções de manipulação da janela permanecem as mesmas) ...
def get_rel_coords(event):
    x, y = event.x_root - root.winfo_rootx(), event.y_root - root.winfo_rooty()
    return x, y
def update_cursor(event):
    x, y = get_rel_coords(event)
    w, h = root.winfo_width(), root.winfo_height()
    left, right, top, bottom = x < BORDER, x > w - BORDER, y < BORDER, y > h - BORDER
    if (top and left) or (bottom and right): cursor = 'size_nw_se'
    elif (top and right) or (bottom and left): cursor = 'size_ne_sw'
    elif left or right: cursor = 'size_we'
    elif top or bottom: cursor = 'size_ns'
    else: cursor = 'arrow'
    root.config(cursor=cursor)
def on_button_press(event):
    root.mode_x, root.mode_y = event.x_root, event.y_root
    root.win_x, root.win_y = root.winfo_x(), root.winfo_y()
    root.win_w, root.win_h = root.winfo_width(), root.winfo_height()
    x, y = get_rel_coords(event)
    w, h = root.win_w, root.win_h
    left, right, top, bottom = x < BORDER, x > w - BORDER, y < BORDER, y > h - BORDER
    if top and left: root.mode = 'nw'
    elif top and right: root.mode = 'ne'
    elif bottom and left: root.mode = 'sw'
    elif bottom and right: root.mode = 'se'
    elif left: root.mode = 'w'
    elif right: root.mode = 'e'
    elif top: root.mode = 'n'
    elif bottom: root.mode = 's'
    else: root.mode = 'move'
def on_button_drag(event):
    dx, dy = event.x_root - root.mode_x, event.y_root - root.mode_y
    mode = getattr(root, 'mode', 'move')
    x, y, w, h = root.win_x, root.win_y, root.win_w, root.win_h
    new_x, new_y, new_w, new_h = x, y, w, h
    if mode == 'move':
        new_x, new_y = x + dx, y + dy
    else:
        if 'n' in mode:
            new_h = max(MIN_HEIGHT, h - dy)
            new_y = y + (h - new_h)
        if 's' in mode: new_h = max(MIN_HEIGHT, h + dy)
        if 'w' in mode:
            new_w = max(MIN_WIDTH, w - dx)
            new_x = x + (w - new_w)
        if 'e' in mode: new_w = max(MIN_WIDTH, w + dx)
    root.geometry(f'{new_w}x{new_h}+{new_x}+{new_y}')

# --- Janela principal ---
root = tk.Tk()
root.overrideredirect(True)
root.geometry('190x30+20+20') # Largura ajustada para o novo layout
root.config(bg='black')
root.attributes('-alpha', ALPHA_LEVELS[current_alpha_index])
is_topmost = True
root.attributes('-topmost', is_topmost)
root.update_idletasks()
hwnd = win32gui.GetParent(root.winfo_id())
ex_styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_styles | win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST | win32con.WS_EX_TOOLWINDOW)

# --- Layout interno ---
frame = tk.Frame(root, bg='black')
frame.pack(fill='both', expand=True)

# Mudei o nome do label principal para 'time_label'
time_label = tk.Label(frame, font=('Segoe UI', 14, 'bold'), fg='white', bg='black')
time_label.pack(side='left', padx=(4, 0), pady=2)

# NOVO LABEL PARA O FPS (ele começa escondido)
fps_label = tk.Label(frame, font=('Segoe UI', 14, 'bold'), fg='white', bg='black')
# (não usamos .pack() aqui, pois ele começa escondido)

# --- BOTÕES ---
btn_close = tk.Button(frame, text='×', command=root.destroy, bg='black', fg='white', bd=0, relief='flat', font=('Segoe UI', 12, 'bold'), activebackground='red', activeforeground='white')
btn_close.pack(side='right', padx=(0, 4))
btn_pin = tk.Button(frame, text='📌', command=toggle_topmost, bg='black', fg='white', bd=0, relief='flat', font=('Segoe UI', 10), activebackground='black', activeforeground='white')
btn_pin.pack(side='right')
btn_alpha = tk.Button(frame, text='💧', command=cycle_transparency, bg='black', fg='white', bd=0, relief='flat', font=('Segoe UI', 10), activebackground='black', activeforeground='white')
btn_alpha.pack(side='right')
btn_fps = tk.Button(frame, text='FPS', command=toggle_fps_mode, bg='black', fg='white', bd=0, relief='flat', font=('Segoe UI', 9, 'bold'), activebackground='black', activeforeground='white')
btn_fps.pack(side='right')

# --- Bindings ---
update_time()
root.bind('<Escape>', lambda e: root.destroy())
root.bind('<Motion>', update_cursor)
root.bind('<ButtonPress-1>', on_button_press)
root.bind('<B1-Motion>', on_button_drag)
root.mainloop()