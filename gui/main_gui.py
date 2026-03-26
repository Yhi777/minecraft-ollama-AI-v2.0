import PySimpleGUI as sg
import threading
import time

class BotGUI:
    def __init__(self):
        self.window = None
        self.running = False
        self.bot_instance = None
        self.ollama_ai = None
        self.learning_module = None
        self.data_logger = None

    def create_layout(self):
        sg.theme('DarkGrey11')
        
        # Left column: Connection and Settings
        left_col = [
            [sg.Frame('Connection Settings', [
                [sg.Text('Server IP:'), sg.InputText('localhost', key='-IP-', size=(20, 1))],
                [sg.Text('Server Port:'), sg.InputText('25565', key='-PORT-', size=(10, 1))],
                [sg.Text('Username:'), sg.InputText('SuperSmartBot', key='-USERNAME-', size=(20, 1))],
                [sg.Button('Connect', size=(10, 1), key='-CONNECT-'), sg.Button('Disconnect', size=(10, 1), key='-DISCONNECT-', disabled=True)]
            ], expand_x=True)],
            [sg.Frame('AI & Ollama Settings', [
                [sg.Text('Ollama Endpoint:'), sg.InputText('http://localhost:11434', key='-OLLAMA_ENDPOINT-', size=(25, 1))],
                [sg.Text('Ollama Model:'), sg.InputText('llama2', key='-OLLAMA_MODEL-', size=(20, 1))],
                [sg.Button('Apply AI Settings', key='-APPLY_AI-')],
                [sg.Checkbox('Enable Ollama Reasoning', default=True, key='-ENABLE_OLLAMA-')],
                [sg.Checkbox('Enable PyTorch Learning', default=True, key='-ENABLE_PYTORCH-')]
            ], expand_x=True)],
            [sg.Frame('Bot Control', [
                [sg.Text('Main Goal:'), sg.InputText('Explore and survive', key='-GOAL-', size=(25, 1))],
                [sg.Button('Update Goal', key='-SET_GOAL-')],
                [sg.Button('Start Autonomous Mode', key='-START_AUTO-', button_color=('white', 'green')), 
                 sg.Button('Stop Autonomous Mode', key='-STOP_AUTO-', button_color=('white', 'red'), disabled=True)],
                [sg.Text('Movement Mode:'), sg.Combo(['Natural', 'Sprint', 'Stealth'], default_value='Natural', key='-MOVE_MODE-')]
            ], expand_x=True)]
        ]
        
        # Right column: Status and Analytics
        right_col = [
            [sg.Frame('Real-time Perception', [
                [sg.Text('Status: Offline', key='-STATUS-', text_color='red', font=('Helvetica', 12, 'bold'))],
                [sg.Text('Position: (0.0, 0.0, 0.0)', key='-POS-')],
                [sg.ProgressBar(20, orientation='h', size=(20, 20), key='-HEALTH_BAR-', bar_color=('red', 'white')), sg.Text('HP: 20/20', key='-HEALTH_TEXT-')],
                [sg.Text('Inventory Items: 0', key='-INV_COUNT-')],
                [sg.Text('Current Action: None', key='-ACTION-', text_color='cyan')],
                [sg.Text('Reasoning Log:'), sg.Multiline('', size=(45, 8), key='-AI_LOG-', autoscroll=True, disabled=True, font=('Consolas', 9))]
            ], expand_x=True)],
            [sg.Frame('Learning Metrics', [
                [sg.Text('Brain Model: advanced_brain_v1.pth')],
                [sg.Text('Exploration Rate (Epsilon): 1.00', key='-EPSILON-')],
                [sg.Text('Current Reward: 0.00', key='-REWARD-')],
                [sg.Button('Save Brain Weights', key='-SAVE_MODEL-')],
                [sg.Button('Export Analytics Spreadsheet', key='-GEN_EXCEL-', button_color=('black', 'orange'))]
            ], expand_x=True)]
        ]
        
        layout = [
            [sg.Text('Minecraft Autonomous AI Bot - Upgraded v2.0', font=('Helvetica', 22, 'bold'), justification='center', expand_x=True, text_color='gold')],
            [sg.HorizontalSeparator()],
            [sg.Column(left_col, vertical_alignment='top'), sg.VSeparator(), sg.Column(right_col, vertical_alignment='top')],
            [sg.Output(size=(100, 10), key='-CONSOLE-', font=('Consolas', 9))]
        ]
        return layout

    def run(self, bot_loop_callback):
        self.window = sg.Window('Minecraft Autonomous AI Bot v2.0', self.create_layout(), finalize=True, resizable=True)
        
        while True:
            event, values = self.window.read(timeout=100)
            if event == sg.WIN_CLOSED:
                break
            
            if event == '-CONNECT-':
                # Start connection in background thread
                threading.Thread(target=bot_loop_callback, args=(values,), daemon=True).start()
                self.window['-CONNECT-'].update(disabled=True)
                self.window['-DISCONNECT-'].update(disabled=False)
                self.window['-STATUS-'].update('Status: Connecting...', text_color='orange')

            if event == '-DISCONNECT-':
                # Signal bot to stop (would need a flag in the bot instance)
                self.window['-CONNECT-'].update(disabled=False)
                self.window['-DISCONNECT-'].update(disabled=True)
                self.window['-STATUS-'].update('Status: Offline', text_color='red')

            if event == '-START_AUTO-':
                self.window['-START_AUTO-'].update(disabled=True)
                self.window['-STOP_AUTO-'].update(disabled=False)
                print("Autonomous Mode Enabled.")

            if event == '-STOP_AUTO-':
                self.window['-START_AUTO-'].update(disabled=False)
                self.window['-STOP_AUTO-'].update(disabled=True)
                print("Autonomous Mode Disabled.")

        self.window.close()

    def update_gui_state(self, data):
        """Thread-safe update of the GUI elements."""
        if not self.window:
            return
            
        if 'status' in data:
            self.window['-STATUS-'].update(f"Status: {data['status']}", text_color='green' if data['status'] == 'Online' else 'red')
        if 'pos' in data:
            p = data['pos']
            self.window['-POS-'].update(f"Position: ({p['x']:.1f}, {p['y']:.1f}, {p['z']:.1f})")
        if 'health' in data:
            h = data['health']
            self.window['-HEALTH_BAR-'].update(h)
            self.window['-HEALTH_TEXT-'].update(f"HP: {h}/20")
        if 'inv_count' in data:
            self.window['-INV_COUNT-'].update(f"Inventory Items: {data['inv_count']}")
        if 'action' in data:
            self.window['-ACTION-'].update(f"Current Action: {data['action']}")
        if 'ai_log' in data:
            self.window['-AI_LOG-'].print(f"[{time.strftime('%H:%M:%S')}] {data['ai_log']}")
        if 'epsilon' in data:
            self.window['-EPSILON-'].update(f"Exploration Rate (Epsilon): {data['epsilon']:.2f}")
        if 'reward' in data:
            self.window['-REWARD-'].update(f"Current Reward: {data['reward']:.2f}")
