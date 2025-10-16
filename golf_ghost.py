import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

class GhostGolfer:
    def __init__(self, handicap_index, course_rating, slope_rating, par_values, hole_handicaps):
        self.handicap_index = handicap_index
        self.course_rating = course_rating
        self.slope_rating = slope_rating
        self.par_values = par_values
        self.hole_handicaps = hole_handicaps
        self.course_handicap = round((handicap_index * slope_rating) / 113)
        
    def generate_round(self):
        scores = []
        expected_strokes_over = self.course_handicap
        strokes_per_hole = expected_strokes_over / 18.0
        round_adjustment = random.gauss(0, 1.2)
        
        for i, (par, hole_hcp) in enumerate(zip(self.par_values, self.hole_handicaps)):
            strokes_received = 1 if hole_hcp <= self.course_handicap else 0
            if self.course_handicap > 18:
                extra_strokes = self.course_handicap - 18
                if hole_hcp <= extra_strokes:
                    strokes_received = 2
            
            base_score = par + strokes_per_hole
            hole_randomness = random.gauss(0, 1.1)
            
            if hole_hcp <= 6:
                difficulty_factor = 0.3
            elif hole_hcp >= 13:
                difficulty_factor = -0.2
            else:
                difficulty_factor = 0
            
            raw_score = base_score + (round_adjustment / 18.0) + hole_randomness + difficulty_factor
            raw_score = max(par - 1, min(par + 6, round(raw_score)))
            net_score = raw_score - strokes_received
            
            scores.append({
                'hole': i + 1,
                'par': par,
                'gross_score': int(raw_score),
                'strokes_received': strokes_received,
                'net_score': int(net_score)
            })
        
        return scores


class GolfGhostApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Golf Ghost Analytics")
        self.root.geometry("1100x750")
        
        # Dark theme colors
        self.colors = {
            'bg_primary': '#0f172a',      # Dark slate
            'bg_secondary': '#1e293b',    # Lighter slate
            'bg_card': '#1e293b',         # Card background
            'accent_blue': '#3b82f6',     # Electric blue
            'accent_cyan': '#06b6d4',     # Cyan
            'accent_green': '#10b981',    # Neon green
            'text_primary': '#f8fafc',    # Almost white
            'text_secondary': '#cbd5e1',  # Light gray
            'text_muted': '#64748b',      # Muted gray
            'border': '#334155',          # Border gray
            'success': '#10b981',         # Green
            'warning': '#f59e0b',         # Orange
            'danger': '#ef4444',          # Red
            'eagle': '#10b981',           # Green
            'birdie': '#22d3ee',          # Cyan
            'par': '#64748b',             # Gray
            'bogey': '#f59e0b',           # Orange
            'double': '#f97316',          # Deep orange
            'triple': '#ef4444'           # Red
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
        self.courses_file = "golf_courses.json"
        self.courses = self.load_courses()
        
        self.setup_styles()
        self.create_header()
        
        # Main container with tabs
        self.tab_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.tab_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Custom tab buttons
        self.create_custom_tabs()
        
        # Content area
        self.content_frame = tk.Frame(self.tab_container, bg=self.colors['bg_primary'])
        self.content_frame.pack(fill='both', expand=True)
        
        # Initialize tabs
        self.generate_frame = None
        self.manage_frame = None
        self.current_tab = None
        
        self.show_generate_tab()
        
    def setup_styles(self):
        """Setup custom styles for ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('.',
            background=self.colors['bg_primary'],
            foreground=self.colors['text_primary'],
            fieldbackground=self.colors['bg_secondary'],
            borderwidth=0)
        
        # Entry style
        style.configure('Dark.TEntry',
            fieldbackground=self.colors['bg_secondary'],
            foreground=self.colors['text_primary'],
            bordercolor=self.colors['border'],
            lightcolor=self.colors['bg_secondary'],
            darkcolor=self.colors['bg_secondary'],
            insertcolor=self.colors['text_primary'])
        
        # Combobox style
        style.configure('Dark.TCombobox',
            fieldbackground=self.colors['bg_secondary'],
            background=self.colors['bg_secondary'],
            foreground=self.colors['text_primary'],
            arrowcolor=self.colors['text_primary'],
            bordercolor=self.colors['border'])
        
    def create_header(self):
        """Create the header with gradient effect"""
        header = tk.Frame(self.root, bg=self.colors['accent_blue'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Title area
        title_frame = tk.Frame(header, bg=self.colors['accent_blue'])
        title_frame.pack(expand=True)
        
        # Icon/Logo
        icon_label = tk.Label(title_frame, text="🤖", font=('Arial', 32), 
                             bg=self.colors['accent_blue'], fg='white')
        icon_label.pack(side='left', padx=(0, 15))
        
        # Title and subtitle
        text_frame = tk.Frame(title_frame, bg=self.colors['accent_blue'])
        text_frame.pack(side='left')
        
        title = tk.Label(text_frame, text="GOLF GHOST ANALYTICS", 
                        font=('Arial', 24, 'bold'),
                        bg=self.colors['accent_blue'], fg='white')
        title.pack(anchor='w')
        
        subtitle = tk.Label(text_frame, text="AI-Powered Score Generation System", 
                           font=('Arial', 10),
                           bg=self.colors['accent_blue'], fg='#e0e7ff')
        subtitle.pack(anchor='w')
        
    def create_custom_tabs(self):
        """Create custom styled tab buttons"""
        tab_bar = tk.Frame(self.tab_container, bg=self.colors['bg_primary'], height=50)
        tab_bar.pack(fill='x', pady=(10, 20))
        
        self.tab_buttons = {}
        
        # Generate Round tab
        btn_generate = tk.Button(tab_bar, text="⚡ GENERATE ROUND", 
                                command=self.show_generate_tab,
                                font=('Arial', 11, 'bold'),
                                bg=self.colors['accent_blue'],
                                fg='white',
                                activebackground=self.colors['accent_cyan'],
                                activeforeground='white',
                                relief='flat',
                                padx=30, pady=12,
                                cursor='hand2',
                                borderwidth=0)
        btn_generate.pack(side='left', padx=(0, 10))
        self.tab_buttons['generate'] = btn_generate
        
        # Manage Courses tab
        btn_manage = tk.Button(tab_bar, text="⚙️ MANAGE COURSES", 
                              command=self.show_manage_tab,
                              font=('Arial', 11, 'bold'),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_secondary'],
                              activebackground=self.colors['accent_cyan'],
                              activeforeground='white',
                              relief='flat',
                              padx=30, pady=12,
                              cursor='hand2',
                              borderwidth=0)
        btn_manage.pack(side='left')
        self.tab_buttons['manage'] = btn_manage
        
    def update_tab_buttons(self, active_tab):
        """Update tab button styles"""
        for tab_name, button in self.tab_buttons.items():
            if tab_name == active_tab:
                button.config(bg=self.colors['accent_blue'], 
                            fg='white')
            else:
                button.config(bg=self.colors['bg_secondary'], 
                            fg=self.colors['text_secondary'])
        
    def show_generate_tab(self):
        """Show generate round tab"""
        self.clear_content()
        self.update_tab_buttons('generate')
        self.generate_frame = self.create_generate_tab()
        self.current_tab = 'generate'
        
    def show_manage_tab(self):
        """Show manage courses tab"""
        self.clear_content()
        self.update_tab_buttons('manage')
        self.manage_frame = self.create_manage_tab()
        self.current_tab = 'manage'
        
    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def load_courses(self):
        """Load saved courses from JSON file"""
        if os.path.exists(self.courses_file):
            try:
                with open(self.courses_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_courses(self):
        """Save courses to JSON file"""
        with open(self.courses_file, 'w') as f:
            json.dump(self.courses, f, indent=2)
            
    def create_stat_card(self, parent, label, value, color):
        """Create a stat card widget"""
        card = tk.Frame(parent, bg=self.colors['bg_card'], 
                       highlightbackground=self.colors['border'],
                       highlightthickness=1)
        card.pack(side='left', fill='both', expand=True, padx=8)
        
        value_label = tk.Label(card, text=str(value), 
                              font=('Arial', 28, 'bold'),
                              bg=self.colors['bg_card'], 
                              fg=color)
        value_label.pack(pady=(15, 5))
        
        label_label = tk.Label(card, text=label, 
                              font=('Arial', 9),
                              bg=self.colors['bg_card'], 
                              fg=self.colors['text_muted'])
        label_label.pack(pady=(0, 15))
        
        return card
        
    def create_generate_tab(self):
        """Create the generate round interface"""
        main = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        main.pack(fill='both', expand=True)
        
        # Left panel - Controls
        left_panel = tk.Frame(main, bg=self.colors['bg_primary'], width=350)
        left_panel.pack(side='left', fill='both', padx=(0, 15))
        left_panel.pack_propagate(False)
        
        # Control card
        control_card = tk.Frame(left_panel, bg=self.colors['bg_card'],
                               highlightbackground=self.colors['border'],
                               highlightthickness=1)
        control_card.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Card header
        header = tk.Label(control_card, text="⚙️ CONFIGURATION", 
                         font=('Arial', 12, 'bold'),
                         bg=self.colors['bg_card'], 
                         fg=self.colors['text_primary'])
        header.pack(pady=(20, 20), padx=20, anchor='w')
        
        # Course selection
        self.create_input_group(control_card, "COURSE", is_dropdown=True)
        
        # GHIN input
        self.ghin_var = tk.StringVar(value="15.0")
        ghin_entry = self.create_input_group(control_card, "GHOST GHIN INDEX", var=self.ghin_var)
        
        # Course info display
        self.info_display = tk.Frame(control_card, bg=self.colors['bg_secondary'],
                                    highlightbackground=self.colors['border'],
                                    highlightthickness=1)
        self.info_display.pack(fill='x', padx=20, pady=20)
        
        info_label = tk.Label(self.info_display, 
                             text="Select a course to view details", 
                             font=('Arial', 9, 'italic'),
                             bg=self.colors['bg_secondary'], 
                             fg=self.colors['text_muted'],
                             wraplength=280)
        info_label.pack(pady=15, padx=15)
        
        # Generate button
        btn_frame = tk.Frame(control_card, bg=self.colors['bg_card'])
        btn_frame.pack(fill='x', padx=20, pady=(10, 25))
        
        generate_btn = tk.Button(btn_frame, text="⚡ GENERATE ROUND", 
                                command=self.generate_round,
                                font=('Arial', 12, 'bold'),
                                bg=self.colors['accent_green'],
                                fg='white',
                                activebackground='#059669',
                                activeforeground='white',
                                relief='flat',
                                padx=20, pady=15,
                                cursor='hand2',
                                borderwidth=0)
        generate_btn.pack(fill='x')
        
        # Right panel - Results
        right_panel = tk.Frame(main, bg=self.colors['bg_primary'])
        right_panel.pack(side='left', fill='both', expand=True)
        
        # Stats cards container
        self.stats_container = tk.Frame(right_panel, bg=self.colors['bg_primary'], 
                                       height=100)
        self.stats_container.pack(fill='x', pady=(0, 15))
        self.stats_container.pack_propagate(False)
        
        # Scorecard container
        scorecard_card = tk.Frame(right_panel, bg=self.colors['bg_card'],
                                 highlightbackground=self.colors['border'],
                                 highlightthickness=1)
        scorecard_card.pack(fill='both', expand=True)
        
        # Scorecard header
        sc_header = tk.Label(scorecard_card, text="📊 SCORECARD", 
                            font=('Arial', 12, 'bold'),
                            bg=self.colors['bg_card'], 
                            fg=self.colors['text_primary'])
        sc_header.pack(pady=(15, 10), padx=20, anchor='w')
        
        # Create scorecard table
        self.create_scorecard_table(scorecard_card)
        
        return main
        
    def create_input_group(self, parent, label_text, var=None, is_dropdown=False):
        """Create an input field group"""
        group = tk.Frame(parent, bg=self.colors['bg_card'])
        group.pack(fill='x', padx=20, pady=(0, 20))
        
        label = tk.Label(group, text=label_text, 
                        font=('Arial', 9, 'bold'),
                        bg=self.colors['bg_card'], 
                        fg=self.colors['text_muted'])
        label.pack(anchor='w', pady=(0, 8))
        
        if is_dropdown:
            self.course_var = tk.StringVar()
            dropdown = ttk.Combobox(group, textvariable=self.course_var,
                                   style='Dark.TCombobox',
                                   font=('Arial', 11),
                                   state='readonly')
            dropdown['values'] = list(self.courses.keys())
            dropdown.pack(fill='x')
            dropdown.bind('<<ComboboxSelected>>', self.load_selected_course)
            
            # Style the dropdown
            self.root.option_add('*TCombobox*Listbox.background', self.colors['bg_secondary'])
            self.root.option_add('*TCombobox*Listbox.foreground', self.colors['text_primary'])
            self.root.option_add('*TCombobox*Listbox.selectBackground', self.colors['accent_blue'])
            self.root.option_add('*TCombobox*Listbox.selectForeground', 'white')
            
            return dropdown
        else:
            entry = tk.Entry(group, textvariable=var,
                           font=('Arial', 11),
                           bg=self.colors['bg_secondary'],
                           fg=self.colors['text_primary'],
                           insertbackground=self.colors['text_primary'],
                           relief='flat',
                           borderwidth=0)
            entry.pack(fill='x', ipady=8, ipadx=10)
            return entry
            
    def create_scorecard_table(self, parent):
        """Create the scorecard table"""
        table_container = tk.Frame(parent, bg=self.colors['bg_card'])
        table_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create canvas for custom styling
        canvas = tk.Canvas(table_container, bg=self.colors['bg_card'],
                          highlightthickness=0)
        scrollbar = tk.Scrollbar(table_container, orient='vertical', 
                                command=canvas.yview)
        
        self.scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_card'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Table header
        self.create_table_header()
        
    def create_table_header(self):
        """Create table header row"""
        header_row = tk.Frame(self.scrollable_frame, bg=self.colors['bg_secondary'],
                             height=40)
        header_row.pack(fill='x', pady=(0, 2))
        header_row.pack_propagate(False)
        
        headers = [
            ('HOLE', 60),
            ('YDS', 70),
            ('PAR', 60),
            ('HCP', 60),
            ('STR', 70),
            ('GROSS', 80),
            ('NET', 80)
        ]
        
        for header_text, width in headers:
            header = tk.Label(header_row, text=header_text,
                            font=('Arial', 9, 'bold'),
                            bg=self.colors['bg_secondary'],
                            fg=self.colors['text_muted'],
                            width=width//8)
            header.pack(side='left', padx=2)
            
    def load_selected_course(self, event):
        """Load course info when selected"""
        course_name = self.course_var.get()
        if course_name in self.courses:
            course_data = self.courses[course_name]
            total_yardage = sum(course_data.get('yardages', [0]*18))
            
            # Update info display
            for widget in self.info_display.winfo_children():
                widget.destroy()
                
            info_frame = tk.Frame(self.info_display, bg=self.colors['bg_secondary'])
            info_frame.pack(fill='both', expand=True, padx=15, pady=12)
            
            details = [
                ('TEE', course_data['tee_name']),
                ('RATING', str(course_data['course_rating'])),
                ('SLOPE', str(course_data['slope_rating'])),
                ('PAR', str(sum(course_data['par_values']))),
                ('YARDS', str(total_yardage))
            ]
            
            for label, value in details:
                row = tk.Frame(info_frame, bg=self.colors['bg_secondary'])
                row.pack(fill='x', pady=3)
                
                tk.Label(row, text=label + ':', 
                        font=('Arial', 9, 'bold'),
                        bg=self.colors['bg_secondary'],
                        fg=self.colors['text_muted'],
                        width=8, anchor='w').pack(side='left')
                
                tk.Label(row, text=value,
                        font=('Arial', 10, 'bold'),
                        bg=self.colors['bg_secondary'],
                        fg=self.colors['accent_cyan']).pack(side='left')
                        
    def generate_round(self):
        """Generate a round for the ghost player"""
        try:
            course_name = self.course_var.get()
            if not course_name or course_name not in self.courses:
                messagebox.showerror("Error", "Please select a course",
                                   parent=self.root)
                return
            
            ghin = float(self.ghin_var.get())
            course_data = self.courses[course_name]
            
            ghost = GhostGolfer(
                ghin,
                course_data['course_rating'],
                course_data['slope_rating'],
                course_data['par_values'],
                course_data['hole_handicaps']
            )
            
            scores = ghost.generate_round()
            
            # Calculate totals
            total_par = sum(course_data['par_values'])
            total_gross = sum(s['gross_score'] for s in scores)
            total_net = sum(s['net_score'] for s in scores)
            total_yardage = sum(course_data.get('yardages', [0]*18))
            
            # Update stats cards
            for widget in self.stats_container.winfo_children():
                widget.destroy()
                
            self.create_stat_card(self.stats_container, 'GROSS SCORE', 
                                 f"{total_gross} ({total_gross - total_par:+d})", 
                                 self.colors['accent_cyan'])
            self.create_stat_card(self.stats_container, 'NET SCORE', 
                                 f"{total_net} ({total_net - total_par:+d})", 
                                 self.colors['accent_green'])
            self.create_stat_card(self.stats_container, 'COURSE HCP', 
                                 ghost.course_handicap, 
                                 self.colors['text_primary'])
            
            # Clear and populate scorecard
            for widget in self.scrollable_frame.winfo_children():
                if widget != self.scrollable_frame.winfo_children()[0]:  # Keep header
                    widget.destroy()
                    
            self.create_table_header()
            
            yardages = course_data.get('yardages', [0]*18)
            
            # Track front/back 9
            front_nine = {'par': 0, 'gross': 0, 'net': 0, 'yards': 0}
            back_nine = {'par': 0, 'gross': 0, 'net': 0, 'yards': 0}
            total_strokes = 0
            
            for score in scores:
                hole_num = score['hole']
                par = score['par']
                gross = score['gross_score']
                net = score['net_score']
                strokes = score['strokes_received']
                hcp = course_data['hole_handicaps'][hole_num - 1]
                yardage = yardages[hole_num - 1]
                
                # Determine color based on score
                diff = gross - par
                if diff <= -2:
                    score_color = self.colors['eagle']
                elif diff == -1:
                    score_color = self.colors['birdie']
                elif diff == 0:
                    score_color = self.colors['par']
                elif diff == 1:
                    score_color = self.colors['bogey']
                elif diff == 2:
                    score_color = self.colors['double']
                else:
                    score_color = self.colors['triple']
                
                # Track totals
                if hole_num <= 9:
                    front_nine['par'] += par
                    front_nine['gross'] += gross
                    front_nine['net'] += net
                    front_nine['yards'] += yardage
                else:
                    back_nine['par'] += par
                    back_nine['gross'] += gross
                    back_nine['net'] += net
                    back_nine['yards'] += yardage
                    
                total_strokes += strokes
                
                # Create row
                self.create_score_row(hole_num, yardage, par, hcp, strokes, 
                                    gross, net, score_color, False)
                
                # Add subtotal after hole 9
                if hole_num == 9:
                    self.create_score_row('OUT', front_nine['yards'], 
                                        front_nine['par'], '', '',
                                        front_nine['gross'], front_nine['net'],
                                        self.colors['accent_blue'], True)
            
            # Add back 9 and total
            self.create_score_row('IN', back_nine['yards'], back_nine['par'], 
                                '', '', back_nine['gross'], back_nine['net'],
                                self.colors['accent_blue'], True)
            
            self.create_score_row('TOT', total_yardage, total_par, '', 
                                total_strokes, total_gross, total_net,
                                self.colors['accent_green'], True)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid GHIN handicap",
                               parent=self.root)
                               
    def create_score_row(self, hole, yardage, par, hcp, strokes, gross, net, 
                        color, is_total):
        """Create a score row in the table"""
        bg_color = self.colors['bg_secondary'] if is_total else self.colors['bg_card']
        row = tk.Frame(self.scrollable_frame, bg=bg_color, height=35)
        row.pack(fill='x', pady=1)
        row.pack_propagate(False)
        
        font_style = ('Arial', 10, 'bold') if is_total else ('Arial', 10)
        
        values = [
            (str(hole), 60),
            (str(yardage) if yardage else '', 70),
            (str(par) if par else '', 60),
            (str(hcp) if hcp else '', 60),
            (str(strokes) if strokes else '', 70),
            (str(gross), 80),
            (str(net), 80)
        ]
        
        for i, (value, width) in enumerate(values):
            fg_color = color if i >= 5 else self.colors['text_primary']
            if is_total and i == 0:
                fg_color = self.colors['text_primary']
                
            label = tk.Label(row, text=value,
                           font=font_style,
                           bg=bg_color,
                           fg=fg_color,
                           width=width//8)
            label.pack(side='left', padx=2)
            
    def create_manage_tab(self):
        """Create the manage courses interface"""
        main = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        main.pack(fill='both', expand=True)
        
        # Left panel - Course list
        left_panel = tk.Frame(main, bg=self.colors['bg_primary'], width=300)
        left_panel.pack(side='left', fill='both', padx=(0, 15))
        left_panel.pack_propagate(False)
        
        list_card = tk.Frame(left_panel, bg=self.colors['bg_card'],
                            highlightbackground=self.colors['border'],
                            highlightthickness=1)
        list_card.pack(fill='both', expand=True, padx=5, pady=5)
        
        list_header = tk.Label(list_card, text="💾 SAVED COURSES", 
                              font=('Arial', 12, 'bold'),
                              bg=self.colors['bg_card'], 
                              fg=self.colors['text_primary'])
        list_header.pack(pady=(20, 15), padx=20, anchor='w')
        
        # Listbox
        self.courses_listbox = tk.Listbox(list_card,
                                          font=('Arial', 10),
                                          bg=self.colors['bg_secondary'],
                                          fg=self.colors['text_primary'],
                                          selectbackground=self.colors['accent_blue'],
                                          selectforeground='white',
                                          relief='flat',
                                          borderwidth=0,
                                          highlightthickness=0)
        self.courses_listbox.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        self.courses_listbox.bind('<<ListboxSelect>>', self.load_course_to_edit)
        self.update_courses_list()
        
        # Right panel - Course editor
        right_panel = tk.Frame(main, bg=self.colors['bg_primary'])
        right_panel.pack(side='left', fill='both', expand=True)
        
        editor_card = tk.Frame(right_panel, bg=self.colors['bg_card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        editor_card.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollable editor content
        canvas = tk.Canvas(editor_card, bg=self.colors['bg_card'],
                          highlightthickness=0)
        scrollbar = tk.Scrollbar(editor_card, orient='vertical', 
                                command=canvas.yview)
        
        editor_frame = tk.Frame(canvas, bg=self.colors['bg_card'])
        
        editor_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=editor_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Editor header
        editor_header = tk.Label(editor_frame, text="✏️ COURSE EDITOR", 
                                font=('Arial', 12, 'bold'),
                                bg=self.colors['bg_card'], 
                                fg=self.colors['text_primary'])
        editor_header.pack(pady=(20, 20), padx=30, anchor='w')
        
        # Course Name
        self.new_course_name = tk.StringVar()
        self.create_editor_field(editor_frame, "COURSE NAME", self.new_course_name)
        
        # Tee Name
        self.tee_name = tk.StringVar(value="Blue")
        self.create_editor_field(editor_frame, "TEE NAME", self.tee_name)
        
        # Course Rating
        self.course_rating = tk.StringVar(value="72.3")
        self.create_editor_field(editor_frame, "COURSE RATING", self.course_rating)
        
        # Slope Rating
        self.slope_rating = tk.StringVar(value="130")
        self.create_editor_field(editor_frame, "SLOPE RATING", self.slope_rating)
        
        # Par Values
        self.par_values = tk.StringVar(value="4,4,3,5,4,4,3,4,5,4,5,4,3,4,4,3,5,4")
        self.create_editor_field(editor_frame, "PAR VALUES (18 holes)", 
                                self.par_values,
                                hint="e.g., 4,4,3,5,4,4,3,4,5,4,5,4,3,4,4,3,5,4")
        
        # Hole Handicaps
        self.hole_handicaps = tk.StringVar(value="7,5,15,1,11,9,17,13,3,8,2,10,16,6,12,18,4,14")
        self.create_editor_field(editor_frame, "HOLE HANDICAPS (1-18)", 
                                self.hole_handicaps,
                                hint="e.g., 7,5,15,1,11,9,17,13,3,8,2,10,16,6,12,18,4,14")
        
        # Yardages
        self.yardages = tk.StringVar(value="395,405,185,520,380,410,165,390,535,400,545,385,175,395,420,190,510,410")
        self.create_editor_field(editor_frame, "YARDAGES (18 holes)", 
                                self.yardages,
                                hint="e.g., 395,405,185,520,380,410,165,390,535,400,545,385,175,395,420,190,510,410")
        
        # Buttons
        button_frame = tk.Frame(editor_frame, bg=self.colors['bg_card'])
        button_frame.pack(fill='x', padx=30, pady=(20, 30))
        
        save_btn = tk.Button(button_frame, text="💾 SAVE COURSE", 
                            command=self.save_course,
                            font=('Arial', 11, 'bold'),
                            bg=self.colors['accent_green'],
                            fg='white',
                            activebackground='#059669',
                            activeforeground='white',
                            relief='flat',
                            padx=25, pady=12,
                            cursor='hand2',
                            borderwidth=0)
        save_btn.pack(side='left', padx=(0, 10))
        
        delete_btn = tk.Button(button_frame, text="🗑️ DELETE", 
                              command=self.delete_course,
                              font=('Arial', 11, 'bold'),
                              bg=self.colors['danger'],
                              fg='white',
                              activebackground='#dc2626',
                              activeforeground='white',
                              relief='flat',
                              padx=25, pady=12,
                              cursor='hand2',
                              borderwidth=0)
        delete_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = tk.Button(button_frame, text="CLEAR", 
                             command=self.clear_fields,
                             font=('Arial', 11, 'bold'),
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['text_secondary'],
                             activebackground=self.colors['border'],
                             activeforeground=self.colors['text_primary'],
                             relief='flat',
                             padx=25, pady=12,
                             cursor='hand2',
                             borderwidth=0)
        clear_btn.pack(side='left')
        
        return main
        
    def create_editor_field(self, parent, label_text, var, hint=None):
        """Create an editor field"""
        container = tk.Frame(parent, bg=self.colors['bg_card'])
        container.pack(fill='x', padx=30, pady=(0, 20))
        
        label = tk.Label(container, text=label_text, 
                        font=('Arial', 9, 'bold'),
                        bg=self.colors['bg_card'], 
                        fg=self.colors['text_muted'])
        label.pack(anchor='w', pady=(0, 8))
        
        if hint:
            hint_label = tk.Label(container, text=hint, 
                                 font=('Arial', 8),
                                 bg=self.colors['bg_card'], 
                                 fg=self.colors['text_muted'])
            hint_label.pack(anchor='w', pady=(0, 5))
        
        entry = tk.Entry(container, textvariable=var,
                        font=('Arial', 10),
                        bg=self.colors['bg_secondary'],
                        fg=self.colors['text_primary'],
                        insertbackground=self.colors['text_primary'],
                        relief='flat',
                        borderwidth=0)
        entry.pack(fill='x', ipady=10, ipadx=12)
        
        return entry
        
    def save_course(self):
        """Save a new course or update existing"""
        try:
            course_name = self.new_course_name.get().strip()
            if not course_name:
                messagebox.showerror("Error", "Please enter a course name",
                                   parent=self.root)
                return
            
            par_list = [int(x.strip()) for x in self.par_values.get().split(',')]
            hcp_list = [int(x.strip()) for x in self.hole_handicaps.get().split(',')]
            yardage_list = [int(x.strip()) for x in self.yardages.get().split(',')]
            
            if len(par_list) != 18 or len(hcp_list) != 18 or len(yardage_list) != 18:
                messagebox.showerror("Error", "Must have exactly 18 par values, 18 hole handicaps, and 18 yardages",
                                   parent=self.root)
                return
            
            course_data = {
                'tee_name': self.tee_name.get(),
                'course_rating': float(self.course_rating.get()),
                'slope_rating': int(self.slope_rating.get()),
                'par_values': par_list,
                'hole_handicaps': hcp_list,
                'yardages': yardage_list
            }
            
            self.courses[course_name] = course_data
            self.save_courses()
            self.update_courses_list()
            
            # Update dropdown in generate tab if it exists
            if hasattr(self, 'course_dropdown'):
                self.course_dropdown['values'] = list(self.courses.keys())
            
            messagebox.showinfo("Success", f"✓ Course '{course_name}' saved successfully!",
                              parent=self.root)
            
        except ValueError:
            messagebox.showerror("Error", "Please check your input values.",
                               parent=self.root)
    
    def delete_course(self):
        """Delete selected course"""
        course_name = self.new_course_name.get().strip()
        if course_name in self.courses:
            if messagebox.askyesno("Confirm Delete", 
                                  f"Delete course '{course_name}'?",
                                  parent=self.root):
                del self.courses[course_name]
                self.save_courses()
                self.update_courses_list()
                
                # Update dropdown in generate tab if it exists
                if hasattr(self, 'course_dropdown'):
                    self.course_dropdown['values'] = list(self.courses.keys())
                    
                self.clear_fields()
                messagebox.showinfo("Success", "Course deleted",
                                  parent=self.root)
        else:
            messagebox.showerror("Error", "Course not found",
                               parent=self.root)
    
    def clear_fields(self):
        """Clear all input fields"""
        self.new_course_name.set("")
        self.tee_name.set("Blue")
        self.course_rating.set("72.3")
        self.slope_rating.set("130")
        self.par_values.set("4,4,3,5,4,4,3,4,5,4,5,4,3,4,4,3,5,4")
        self.hole_handicaps.set("7,5,15,1,11,9,17,13,3,8,2,10,16,6,12,18,4,14")
        self.yardages.set("395,405,185,520,380,410,165,390,535,400,545,385,175,395,420,190,510,410")
    
    def update_courses_list(self):
        """Update the listbox with saved courses"""
        self.courses_listbox.delete(0, tk.END)
        for course_name in sorted(self.courses.keys()):
            self.courses_listbox.insert(tk.END, f"  {course_name}")
    
    def load_course_to_edit(self, event):
        """Load selected course data for editing"""
        selection = self.courses_listbox.curselection()
        if selection:
            course_name = self.courses_listbox.get(selection[0]).strip()
            course_data = self.courses[course_name]
            
            self.new_course_name.set(course_name)
            self.tee_name.set(course_data['tee_name'])
            self.course_rating.set(str(course_data['course_rating']))
            self.slope_rating.set(str(course_data['slope_rating']))
            self.par_values.set(','.join(map(str, course_data['par_values'])))
            self.hole_handicaps.set(','.join(map(str, course_data['hole_handicaps'])))
            
            # Handle backward compatibility for courses without yardages
            if 'yardages' in course_data:
                self.yardages.set(','.join(map(str, course_data['yardages'])))
            else:
                self.yardages.set("395,405,185,520,380,410,165,390,535,400,545,385,175,395,420,190,510,410")


if __name__ == "__main__":
    root = tk.Tk()
    app = GolfGhostApp(root)
    root.mainloop()