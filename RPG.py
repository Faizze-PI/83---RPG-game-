import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading
import time


class ColdWarGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("83: Iron Curtain Crisis")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a0f')
        self.root.resizable(True, True)

        # Game state
        self.game_state = {
            'readiness': 70,
            'trust': 25,
            'intel': 60,
            'paranoia': 40,
            'reputation': 50,
            'turn': 1,
            'hour': 3,
            'game_over': False,
            'choices': [],
            'crisis_level': 0,
            'last_nato_response': ""
        }

        # NATO responses database
        self.nato_responses = {
            'defcon1': [
                "NATO RESPONSE: DEFCON 1! US Strategic Command matches Soviet alert. Reagan convenes emergency cabinet meeting.",
                "NATO RESPONSE: Emergency session of NATO council. All forces go to maximum readiness.",
                "NATO RESPONSE: 'They've gone completely mad!' - British PM Thatcher orders retaliatory protocols."
            ],
            'intelligence': [
                "NATO RESPONSE: CIA detects unusual Soviet intelligence activity. Counter-intelligence measures activated.",
                "NATO RESPONSE: NSA reports Soviet SIGINT surge. Electronic warfare units put on standby.",
                "NATO RESPONSE: 'They're probing our defenses' - NATO command increases communication security."
            ],
            'diplomatic': [
                "NATO RESPONSE: State Department receives Soviet ultimatum. Emergency diplomacy initiated.",
                "NATO RESPONSE: NATO ambassadors coordinate response. 'This is unacceptable provocation.'",
                "NATO RESPONSE: Western allies express outrage at Soviet demands. Emergency UN session called."
            ],
            'invasion': [
                "NATO RESPONSE: RED ALERT! Warsaw Pact forces massing at border. All NATO units to combat stations!",
                "NATO RESPONSE: 'This is not a drill!' - NATO commander orders immediate mobilization.",
                "NATO RESPONSE: Pentagon confirms Soviet armor movements. Airborne divisions put on alert."
            ],
            'vigilance': [
                "NATO RESPONSE: Soviet forces remain at normal readiness. NATO continues Able Archer exercise.",
                "NATO RESPONSE: Intelligence reports Soviet restraint. Exercise continues as planned.",
                "NATO RESPONSE: 'Curious Soviet inaction' - NATO commanders monitor situation cautiously."
            ],
            'hotline': [
                "NATO RESPONSE: White House confirms hotline communication. 'Dialogue preferred to confrontation.'",
                "NATO RESPONSE: Reagan personally responds to Soviet inquiry. Direct communication established.",
                "NATO RESPONSE: Diplomatic breakthrough - both sides communicating directly for first time in crisis."
            ],
            'nuclear_demo': [
                "NATO RESPONSE: NORAD confirms nuclear detonation in Arctic! Global condemnation begins.",
                "NATO RESPONSE: 'They've crossed the nuclear threshold!' - Emergency NATO summit convened.",
                "NATO RESPONSE: UN Security Council emergency session. Worldwide protests against Soviet test."
            ],
            'sabotage': [
                "NATO RESPONSE: Communications disruptions detected. Cyber warfare units activated.",
                "NATO RESPONSE: 'Soviet sabotage attempt foiled' - NATO counter-intelligence successful.",
                "NATO RESPONSE: Infrastructure attacks reported. NATO engineers working to restore systems."
            ],
            'un_appeal': [
                "NATO RESPONSE: Soviet UN ambassador makes dramatic appeal. International community divided.",
                "NATO RESPONSE: 'Propaganda stunt' - Western diplomats dismiss Soviet claims at UN.",
                "NATO RESPONSE: UN debate intensifies. Non-aligned nations call for emergency peace conference."
            ],
            'stand_down': [
                "NATO RESPONSE: Soviet forces reducing alert levels. NATO considers reciprocal de-escalation.",
                "NATO RESPONSE: 'Positive development' - NATO commanders note Soviet restraint.",
                "NATO RESPONSE: Diplomatic channels report Soviet willingness to de-escalate. Breakthrough possible."
            ],
            'intel_synthesis': [
                "NATO RESPONSE: Soviet intelligence analysis detected. NATO increases counter-surveillance.",
                "NATO RESPONSE: 'They're trying to understand our intentions' - NATO intelligence assessment.",
                "NATO RESPONSE: Soviet pattern analysis noted. NATO adjusts exercise parameters accordingly."
            ],
            'limited_strike': [
                "NATO RESPONSE: Soviet limited aggression detected! Retaliatory measures being calculated.",
                "NATO RESPONSE: 'They're testing our resolve' - NATO prepares proportional response.",
                "NATO RESPONSE: Limited Soviet attack confirmed. NATO considering measured military response."
            ]
        }

        # Events system
        self.events = [
            {
                'text': "FLASH: Soviet satellite detects massive NATO bomber formations approaching Polish border!",
                'effect': lambda: self.modify_stats(readiness=15, paranoia=10, crisis_level=5)
            },
            {
                'text': "KGB URGENT: NATO defector reveals Able Archer contains real nuclear targeting data!",
                'effect': lambda: self.modify_stats(intel=20, trust=-15, crisis_level=8)
            },
            {
                'text': "TECHNICAL ALERT: False radar signature triggers nuclear missile warning in East Germany!",
                'effect': lambda: self.modify_stats(intel=-10, paranoia=15, crisis_level=6)
            },
            {
                'text': "POLITBURO DIRECTIVE: 'The Motherland expects decisive action, Marshal Ogarkov.'",
                'effect': lambda: self.modify_stats(paranoia=20, readiness=5, crisis_level=4)
            },
            {
                'text': "CIA INTERCEPT: American President heard saying 'Perhaps it's time to end this charade.'",
                'effect': lambda: self.modify_stats(trust=-20, paranoia=15, crisis_level=7)
            },
            {
                'text': "WARSAW PACT ALERT: Polish forces report unusual NATO electronic warfare activity!",
                'effect': lambda: self.modify_stats(readiness=10, intel=5, crisis_level=3)
            },
            {
                'text': "SUBMARINE COMMAND: Nuclear sub in Atlantic reports being tracked by NATO destroyers!",
                'effect': lambda: self.modify_stats(readiness=12, trust=-8, crisis_level=5)
            },
            {
                'text': "URGENT: Power grid fluctuations detected near American missile silos—possible launch prep!",
                'effect': lambda: self.modify_stats(paranoia=25, readiness=8, crisis_level=9)
            }
        ]

        self.setup_gui()
        self.update_story_text()
        self.update_all_stats()
        self.update_nato_response(
            "NATO STATUS: Able Archer 83 exercise continues as planned. Monitoring Soviet reactions.")

    def setup_gui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#0a0a0f')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Title Frame
        self.create_title_frame(main_frame)

        # Three-column layout
        game_frame = tk.Frame(main_frame, bg='#0a0a0f')
        game_frame.pack(fill='both', expand=True, pady=10)

        # Left column - Story
        left_frame = tk.Frame(game_frame, bg='#1a0f1a', relief='ridge', bd=3)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        self.create_story_section(left_frame)

        # Middle column - Command Decisions
        middle_frame = tk.Frame(game_frame, bg='#1a1a2a', relief='ridge', bd=3)
        middle_frame.pack(side='left', fill='y', padx=5)
        middle_frame.configure(width=450)

        self.create_choices_section(middle_frame)

        # Right column - Stats and NATO Response
        right_frame = tk.Frame(game_frame, bg='#0f1a1a', relief='ridge', bd=3)
        right_frame.pack(side='left', fill='both', expand=True, padx=(5, 0))

        self.create_stats_panel(right_frame)
        self.create_nato_response_section(right_frame)

    def create_title_frame(self, parent):
        title_frame = tk.Frame(parent, bg='#2d1810', relief='ridge', bd=4)
        title_frame.pack(fill='x', pady=(0, 10))

        title_container = tk.Frame(title_frame, bg='#2d1810')
        title_container.pack(pady=15)

        eight_label = tk.Label(title_container, text="8",
                               font=('Arial Black', 48, 'bold'),
                               fg='#00ffff', bg='#2d1810')
        eight_label.pack(side='left')

        three_label = tk.Label(title_container, text="3",
                               font=('Arial Black', 48, 'bold'),
                               fg='#ff0080', bg='#2d1810')
        three_label.pack(side='left')

        subtitle = tk.Label(title_frame, text="IRON CURTAIN CRISIS",
                            font=('Courier New', 16, 'bold'),
                            fg='#ffff00', bg='#2d1810')
        subtitle.pack()

        scenario_text = tk.Label(title_frame,
                                 text="November 7, 1983. 03:00 AM MOSCOW TIME.\n"
                                 "You are Marshal Nikolai Ogarkov, Chief of the Soviet General Staff.\n"
                                 "NATO's Able Archer 83 exercise has begun—but your intelligence networks are screaming warnings.",
                                 font=('Courier New', 10),
                                 fg='#e0e0ff', bg='#2d1810',
                                 wraplength=800,
                                 justify='center')
        scenario_text.pack(pady=10)

        info_frame = tk.Frame(title_frame, bg='#2d1810')
        info_frame.pack(fill='x', padx=20, pady=5)

        self.turn_label = tk.Label(info_frame, text="DAY 1 - HOUR 03",
                                   font=('Courier New', 12, 'bold'),
                                   fg='#00ffff', bg='#2d1810')
        self.turn_label.pack(side='left')

        self.crisis_label = tk.Label(info_frame, text="CRISIS LEVEL: 0%",
                                     font=('Courier New', 12, 'bold'),
                                     fg='#ff4444', bg='#2d1810')
        self.crisis_label.pack(side='right')

    def create_story_section(self, parent):
        situation_header = tk.Label(parent, text="⚡ KREMLIN WAR ROOM ⚡",
                                    font=('Courier New', 16, 'bold'),
                                    fg='#ff00ff', bg='#1a0f1a')
        situation_header.pack(pady=15)

        story_frame = tk.Frame(parent, bg='#1a0f1a')
        story_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.story_text = tk.Text(story_frame,
                                  height=15,
                                  font=('Courier New', 11),
                                  bg='#2a1f2a', fg='#e0e0ff',
                                  relief='ridge', bd=2,
                                  wrap='word',
                                  state='disabled')

        scrollbar = tk.Scrollbar(story_frame, command=self.story_text.yview)
        self.story_text.config(yscrollcommand=scrollbar.set)

        self.story_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.event_frame = tk.Frame(parent, bg='#1a0f1a')
        self.event_frame.pack(fill='x', padx=20, pady=10)

    def create_choices_section(self, parent):
        choices_label = tk.Label(parent, text="COMMAND DECISIONS",
                                 font=('Courier New', 14, 'bold'),
                                 fg='#00ffff', bg='#1a1a2a')
        choices_label.pack(pady=(15, 10))

        # Create a canvas for scrolling
        canvas = tk.Canvas(parent, bg='#1a1a2a', highlightthickness=0)
        scrollbar = tk.Scrollbar(
            parent, orient='vertical', command=canvas.yview)

        self.choices_frame = tk.Frame(canvas, bg='#1a1a2a')

        self.choices_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.choices_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)

        # Create choice buttons
        self.choice_buttons = []
        choices = [
            ("🚀 DEFCON 1", "Maximum nuclear alert", '#8b0000'),
            ("🔍 INTEL PROBE", "Deep intelligence gathering", '#4b0082'),
            ("⚡ ULTIMATUM", "Diplomatic threats", '#006400'),
            ("🏴 INVASION", "Preemptive strike Germany", '#8b4513'),
            ("✋ VIGILANCE", "Wait and observe", '#2f4f4f'),
            ("📡 HOTLINE", "Contact Reagan directly", '#800080'),
            ("💥 NUCLEAR DEMO", "Tactical nuke demonstration", '#008080'),
            ("🕵️ SABOTAGE", "Covert operations", '#4b0082'),
            ("🌐 UN APPEAL", "Address United Nations", '#008080'),
            ("🚫 STAND DOWN", "Reduce alert levels", '#006400'),
            ("📊 INTEL SYNTHESIS", "Analyze all data", '#4b0082'),
            ("⚔️ LIMITED STRIKE", "Targeted military action", '#8b0000')
        ]

        for i, (title, desc, color) in enumerate(choices):
            btn_frame = tk.Frame(self.choices_frame, bg='#1a1a2a')
            btn_frame.pack(fill='x', pady=3)

            btn = tk.Button(btn_frame,
                            text=f"{title}\n{desc}",
                            font=('Courier New', 9, 'bold'),
                            bg='#3a3a6a', fg='#e0e0ff',
                            activebackground=color,
                            activeforeground='white',
                            relief='raised', bd=2,
                            wraplength=380,
                            justify='center',
                            command=lambda c=i+1: self.make_choice(c))
            btn.pack(fill='x', ipady=8, padx=5)
            self.choice_buttons.append(btn)

    def create_stats_panel(self, parent):
        stats_title = tk.Label(parent, text="SOVIET METRICS",
                               font=('Courier New', 14, 'bold'),
                               fg='#00ffff', bg='#0f1a1a')
        stats_title.pack(pady=15)

        stats_container = tk.Frame(parent, bg='#0f1a1a')
        stats_container.pack(fill='both', expand=True, padx=15, pady=10)

        self.stat_bars = {}

        stats = [
            ('readiness', 'Military Readiness', '#ff0040'),
            ('trust', 'Diplomatic Trust', '#0040ff'),
            ('intel', 'Intelligence Network', '#40ff00'),
            ('paranoia', 'Politburo Paranoia', '#ff8000'),
            ('reputation', 'Global Reputation', '#8000ff'),
            ('crisis_level', 'Global Crisis', '#ff4444')
        ]

        for stat_key, stat_label, color in stats:
            self.create_stat_bar(stats_container, stat_key, stat_label, color)

    def create_stat_bar(self, parent, stat_key, label, color):
        stat_frame = tk.Frame(parent, bg='#0f1a1a')
        stat_frame.pack(fill='x', pady=6)

        label_widget = tk.Label(stat_frame, text=label,
                                font=('Courier New', 10, 'bold'),
                                fg='#e0e0ff', bg='#0f1a1a')
        label_widget.pack(anchor='w')

        bar_frame = tk.Frame(stat_frame, bg='#333333',
                             relief='sunken', bd=2, height=20)
        bar_frame.pack(fill='x', pady=2)
        bar_frame.pack_propagate(False)

        progress_bar = tk.Frame(bar_frame, bg=color, height=16)
        progress_bar.pack(side='left')

        value_label = tk.Label(bar_frame,
                               font=('Courier New', 8, 'bold'),
                               fg='white', bg='#333333')
        value_label.pack(side='right', padx=5)

        self.stat_bars[stat_key] = (progress_bar, bar_frame, value_label)

    def create_nato_response_section(self, parent):
        nato_frame = tk.Frame(parent, bg='#1a2a2a', relief='ridge', bd=3)
        nato_frame.pack(fill='both', expand=True, padx=15, pady=10)

        nato_title = tk.Label(nato_frame, text="🇺🇸 NATO RESPONSE",
                              font=('Courier New', 14, 'bold'),
                              fg='#ff4444', bg='#1a2a2a')
        nato_title.pack(pady=15)

        response_frame = tk.Frame(nato_frame, bg='#2a3a3a')
        response_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.nato_text = tk.Text(response_frame,
                                 height=8,
                                 font=('Courier New', 10),
                                 bg='#1a2a2a', fg='#ffaaaa',
                                 relief='ridge', bd=2,
                                 wrap='word',
                                 state='disabled')

        nato_scrollbar = tk.Scrollbar(
            response_frame, command=self.nato_text.yview)
        self.nato_text.config(yscrollcommand=nato_scrollbar.set)

        self.nato_text.pack(side='left', fill='both', expand=True)
        nato_scrollbar.pack(side='right', fill='y')

    def update_nato_response(self, response):
        self.game_state['last_nato_response'] = response
        self.nato_text.configure(state='normal')
        self.nato_text.delete('1.0', 'end')
        self.nato_text.insert('1.0', response)
        self.nato_text.configure(state='disabled')
        self.nato_text.see('end')

    def get_nato_response(self, choice_type):
        responses = self.nato_responses.get(choice_type, [])
        if responses:
            return random.choice(responses)
        return "NATO RESPONSE: Monitoring situation. No immediate reaction."

    def update_all_stats(self):
        for stat_key in ['readiness', 'trust', 'intel', 'paranoia', 'reputation', 'crisis_level']:
            value = self.game_state[stat_key]
            if stat_key in self.stat_bars:
                progress_bar, bar_frame, value_label = self.stat_bars[stat_key]

                # Update bar width
                bar_frame.update()
                bar_width = bar_frame.winfo_width()
                if bar_width > 0:  # Ensure bar_frame has been rendered
                    new_width = max(1, int((value / 100) * bar_width))
                    progress_bar.configure(width=new_width)

                value_label.configure(text=f"{value}/100")

        self.crisis_label.configure(
            text=f"CRISIS LEVEL: {self.game_state['crisis_level']}%")

    def modify_stats(self, **kwargs):
        for stat, change in kwargs.items():
            if stat in self.game_state:
                self.game_state[stat] = max(
                    0, min(100, self.game_state[stat] + change))
        self.update_all_stats()

    def update_story_text(self, new_text=None):
        if new_text is None:
            new_text = ("The crimson phone rings with an urgent klaxon. Your aide, Colonel Petrov, bursts through "
                        "the reinforced doors of the war room, clutching classified intelligence reports. His face is pale with terror.\n\n"
                        "\"Marshal! Emergency flash traffic from our agents in West Germany!\" His voice trembles. \"NATO forces are "
                        "moving with unprecedented coordination. Tank divisions repositioning under cover of darkness. Strategic bomber "
                        "squadrons have gone to DEFCON 2.\"\n\n"
                        "The massive display screens around you flicker with satellite imagery, radar contacts, and intercepted communications. "
                        "Is this the moment every Soviet strategist has prepared for—the capitalist first strike—or the most dangerous bluff "
                        "in human history?")

        self.story_text.configure(state='normal')
        self.story_text.delete('1.0', 'end')
        self.story_text.insert('1.0', new_text)
        self.story_text.configure(state='disabled')
        self.story_text.see('end')

    def show_event(self):
        if random.random() < 0.35 and not self.game_state['game_over']:
            event = random.choice(self.events)

            for widget in self.event_frame.winfo_children():
                widget.destroy()

            event_popup = tk.Frame(
                self.event_frame, bg='#ff4444', relief='ridge', bd=3)
            event_popup.pack(fill='x', pady=10)

            event_title = tk.Label(event_popup, text="🚨 URGENT FLASH",
                                   font=('Courier New', 12, 'bold'),
                                   fg='#ffffff', bg='#ff4444')
            event_title.pack(pady=5)

            event_text = tk.Label(event_popup, text=event['text'],
                                  font=('Courier New', 10),
                                  fg='#ffffff', bg='#ff4444',
                                  wraplength=500)
            event_text.pack(padx=10, pady=5)

            event['effect']()
            self.root.after(4000, lambda: event_popup.destroy())

    def make_choice(self, choice):
        if self.game_state['game_over']:
            return

        # Visual feedback
        for i, btn in enumerate(self.choice_buttons):
            if i == choice - 1:
                btn.configure(relief='sunken', bg='#ffaa00')
                self.root.after(500, lambda b=btn: b.configure(
                    relief='raised', bg='#3a3a6a'))

        # Choice type for NATO response
        choice_types = ['defcon1', 'intelligence', 'diplomatic', 'invasion', 'vigilance',
                        'hotline', 'nuclear_demo', 'sabotage', 'un_appeal', 'stand_down',
                        'intel_synthesis', 'limited_strike']
        choice_type = choice_types[choice-1]

        # Get NATO response
        nato_response = self.get_nato_response(choice_type)
        self.update_nato_response(nato_response)

        # Process choice effects
        story_update = ""
        if choice == 1:  # DEFCON 1
            self.modify_stats(readiness=25, trust=-15,
                              paranoia=10, crisis_level=15)
            story_update = "🚀 DEFCON 1 ALERT: All nuclear forces at maximum readiness. World holds its breath."

        elif choice == 2:  # Intelligence probe
            intel_gain = random.randint(15, 25)
            self.modify_stats(intel=intel_gain, reputation=5, crisis_level=3)
            story_update = f"🔍 INTELLIGENCE OPERATION: Gathered critical NATO data. (+{intel_gain} Intel)"

        elif choice == 3:  # Diplomatic ultimatum
            self.modify_stats(trust=10, readiness=8,
                              reputation=-10, crisis_level=8)
            story_update = "⚡ DIPLOMATIC ULTIMATUM: Western capitals respond with outrage and caution."

        elif choice == 4:  # Preemptive strike
            if self.game_state['readiness'] >= 70:
                self.modify_stats(readiness=20, trust=-20, crisis_level=12)
                story_update = "🏴 INVASION PREPARED: Tank divisions ready to strike through Fulda Gap."
            else:
                self.modify_stats(
                    readiness=-15, reputation=-20, crisis_level=8)
                story_update = "🏴 INVASION FAILED: Forces not ready for offensive operations."

        elif choice == 5:  # Maintain vigilance
            self.modify_stats(readiness=-5, trust=8,
                              paranoia=-10, crisis_level=-5)
            story_update = "✋ VIGILANCE MAINTAINED: Watching and waiting. Situation remains stable."

        elif choice == 6:  # Emergency hotline
            self.modify_stats(trust=20, reputation=10,
                              paranoia=-5, crisis_level=-8)
            story_update = "📡 HOTLINE ACTIVE: Direct communication with Reagan reduces tensions."

        elif choice == 7:  # Nuclear demonstration
            self.modify_stats(readiness=15, trust=-30,
                              reputation=-15, paranoia=20, crisis_level=20)
            story_update = "💥 NUCLEAR DEMONSTRATION: Arctic test sends shockwaves through international community."

        elif choice == 8:  # Covert sabotage
            self.modify_stats(intel=10, trust=-10, crisis_level=5)
            story_update = "🕵️ SABOTAGE OPERATION: NATO infrastructure disrupted. Deniable operations successful."

        elif choice == 9:  # UN Appeal
            self.modify_stats(reputation=15, trust=10, crisis_level=-10)
            story_update = "🌐 UN APPEAL: International community debates crisis. Diplomatic pressure mounts."

        elif choice == 10:  # Stand down
            self.modify_stats(readiness=-20, trust=25, crisis_level=-15)
            story_update = "🚫 STAND DOWN: De-escalation order issued. NATO reciprocates cautiously."

        elif choice == 11:  # Intel synthesis
            analysis_bonus = random.randint(20, 30)
            self.modify_stats(intel=analysis_bonus,
                              paranoia=-10, crisis_level=-5)
            story_update = f"📊 INTEL SYNTHESIS: Pattern analysis reveals NATO intentions. (+{analysis_bonus} Intel)"

        elif choice == 12:  # Limited strike
            self.modify_stats(readiness=15, trust=-15, crisis_level=10)
            story_update = "⚔️ LIMITED STRIKE: Targeted military action demonstrates Soviet capability."

        # Update game state
        self.game_state['turn'] += 1
        self.game_state['hour'] = (
            self.game_state['hour'] + random.randint(1, 3)) % 24
        if self.game_state['hour'] == 0:
            self.game_state['hour'] = 24

        self.turn_label.configure(
            text=f"DAY {self.game_state['turn']} - HOUR {self.game_state['hour']:02d}")

        # Update story with both perspectives
        full_story = f"SOVIET ACTION: {story_update}\n\n" \
            f"OUTCOME: Crisis level {'increased' if self.game_state['crisis_level'] > 50 else 'decreased'}.\n\n" \
            f"{nato_response}"

        self.update_story_text(full_story)
        self.show_event()
        self.check_game_end()

    def check_game_end(self):
        r, t, i, p, rep, c = (self.game_state['readiness'], self.game_state['trust'],
                              self.game_state['intel'], self.game_state['paranoia'],
                              self.game_state['reputation'], self.game_state['crisis_level'])

        if c >= 95:
            self.end_game("destruction",
                          "💀 GLOBAL NUCLEAR WAR ERUPTS!\n\n"
                          "The world ends in fire. Billions perish as Soviet and NATO nuclear arsenals "
                          "unleash unimaginable destruction. Civilization collapses in a single afternoon.\n\n"
                          "There are no winners in nuclear war. Only the radioactive silence of a dead planet.",
                          "ARMAGEDDON")
        elif t >= 90 and c <= 20:
            self.end_game("victory",
                          "🕊️ PEACEFUL RESOLUTION ACHIEVED!\n\n"
                          "Through masterful diplomacy and restraint, you navigate the crisis without bloodshed. "
                          "The Able Archer exercise concludes peacefully, and both superpowers step back from the brink.\n\n"
                          "History will remember you as the marshal who saved the world from nuclear annihilation.",
                          "DIPLOMATIC VICTORY")
        elif r <= 10 and c >= 80:
            self.end_game("defeat",
                          "💥 NATO FIRST STRIKE SUCCESSFUL!\n\n"
                          "Soviet hesitation proves fatal. NATO launches a devastating nuclear first strike that "
                          "catches Soviet forces unprepared. Moscow, Leningrad, and every major city burn.\n\n"
                          "The Soviet Union ceases to exist. The capitalist victory is complete and total.",
                          "CATASTROPHIC DEFEAT")

    def end_game(self, result_type, message, title):
        self.game_state['game_over'] = True
        for btn in self.choice_buttons:
            btn.configure(state='disabled')

        ending_window = tk.Toplevel(self.root)
        ending_window.title("HISTORICAL OUTCOME")
        ending_window.geometry("600x400")
        ending_window.configure(bg='#000000')
        ending_window.transient(self.root)
        ending_window.grab_set()

        colors = {
            'victory': ('#00ff00', '#002200'),
            'defeat': ('#ff0000', '#220000'),
            'destruction': ('#ff8800', '#221100')
        }
        text_color, bg_color = colors.get(result_type, ('#ffffff', '#000000'))
        ending_window.configure(bg=bg_color)

        title_label = tk.Label(ending_window, text=title,
                               font=('Courier New', 18, 'bold'),
                               fg=text_color, bg=bg_color)
        title_label.pack(pady=20)

        message_label = tk.Label(ending_window, text=message,
                                 font=('Courier New', 12),
                                 fg='white', bg=bg_color,
                                 wraplength=550, justify='left')
        message_label.pack(padx=20, pady=20)

        restart_btn = tk.Button(ending_window, text="COMMENCE NEW SIMULATION",
                                font=('Courier New', 14, 'bold'),
                                bg='#ffd700', fg='#000000',
                                command=lambda: self.restart_game(ending_window))
        restart_btn.pack(pady=20)

    def restart_game(self, ending_window=None):
        if ending_window:
            ending_window.destroy()

        self.game_state = {
            'readiness': 70,
            'trust': 25,
            'intel': 60,
            'paranoia': 40,
            'reputation': 50,
            'turn': 1,
            'hour': 3,
            'game_over': False,
            'choices': [],
            'crisis_level': 0,
            'last_nato_response': ""
        }

        for btn in self.choice_buttons:
            btn.configure(state='normal')

        for widget in self.event_frame.winfo_children():
            widget.destroy()

        self.update_all_stats()
        self.update_story_text()
        self.update_nato_response(
            "NATO STATUS: Able Archer 83 exercise continues as planned. Monitoring Soviet reactions.")
        self.turn_label.configure(text="DAY 1 - HOUR 03")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = ColdWarGame()
    game.run()
