"""
Generate Tab - UI for generating ghost rounds
"""
import tkinter as tk
from tkinter import ttk, messagebox

from ghost_golfer import GhostGolfer
from ui_components import (
    create_stat_card,
    create_button,
    create_card_frame,
    create_section_header
)


class GenerateTab:
    """Tab for generating ghost golf rounds"""
    
    def __init__(self, parent, theme, course_manager):
        self.parent = parent
        self.theme = theme
        self.course_manager = course_manager
        
        self.main_frame = tk.Frame(parent, bg=theme.colors['bg_primary'])
        self.main_frame.pack(fill='both', expand=True)
        
        # Variables
        self.course_var = tk.StringVar()
        self.ghin_var = tk.StringVar(value="15.0")
        
        # UI elements
        self.scorecard_rows = []
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create the generate tab UI"""
        # Left panel - Controls
        left_panel = tk.Frame(self.main_frame, bg=self.theme.colors['bg_primary'], width=350)
        left_panel.pack(side='left', fill='both', padx=(0, 15))
        left_panel.pack_propagate(False)
        
        # Control card
        control_card = create_card_frame(left_panel, self.theme)
        control_card.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Header
        header = create_section_header(control_card, "⚙️ CONFIGURATION", self.theme)
        header.pack(pady=(20, 20), padx=20, anchor='w')
        
        # Course selection
        self.create_course_selector(control_card)
        
        # GHIN input
        self.create_ghin_input(control_card)
        
        # Course info display
        self.info_display = tk.Frame(
            control_card,
            bg=self.theme.colors['bg_secondary'],
            highlightbackground=self.theme.colors['border'],
            highlightthickness=1
        )
        self.info_display.pack(fill='x', padx=20, pady=20)
        
        info_label = tk.Label(
            self.info_display,
            text="Select a course to view details",
            font=('Arial', 9, 'italic'),
            bg=self.theme.colors['bg_secondary'],
            fg=self.theme.colors['text_muted'],
            wraplength=280
        )
        info_label.pack(pady=15, padx=15)
        
        # Generate button
        btn_frame = tk.Frame(control_card, bg=self.theme.colors['bg_card'])
        btn_frame.pack(fill='x', padx=20, pady=(10, 25))
        
        generate_btn = create_button(
            btn_frame, "⚡ GENERATE ROUND",
            self.generate_round, self.theme, 'primary'
        )
        generate_btn.config(font=('Arial', 12, 'bold'), pady=15)
        generate_btn.pack(fill='x')
        
        # Right panel - Results
        self.create_results_panel()
    
    def create_course_selector(self, parent):
        """Create course selection dropdown"""
        group = tk.Frame(parent, bg=self.theme.colors['bg_card'])
        group.pack(fill='x', padx=20, pady=(0, 20))
        
        label = tk.Label(
            group, text="COURSE",
            font=('Arial', 9, 'bold'),
            bg=self.theme.colors['bg_card'],
            fg=self.theme.colors['text_muted']
        )
        label.pack(anchor='w', pady=(0, 8))
        
        self.course_dropdown = ttk.Combobox(
            group, textvariable=self.course_var,
            style='Dark.TCombobox',
            font=('Arial', 11),
            state='readonly'
        )
        self.course_dropdown['values'] = self.course_manager.get_all_courses()
        self.course_dropdown.pack(fill='x')
        self.course_dropdown.bind('<<ComboboxSelected>>', self.load_selected_course)
    
    def create_ghin_input(self, parent):
        """Create GHIN index input"""
        group = tk.Frame(parent, bg=self.theme.colors['bg_card'])
        group.pack(fill='x', padx=20, pady=(0, 20))
        
        label = tk.Label(
            group, text="GHOST GHIN INDEX",
            font=('Arial', 9, 'bold'),
            bg=self.theme.colors['bg_card'],
            fg=self.theme.colors['text_muted']
        )
        label.pack(anchor='w', pady=(0, 8))
        
        # Create frame for border effect
        entry_border = tk.Frame(group, bg=self.theme.colors['accent_blue'], padx=2, pady=2)
        entry_border.pack(fill='x')
        
        entry = tk.Entry(
            entry_border, textvariable=self.ghin_var,
            font=('Arial', 12, 'bold'),
            bg=self.theme.colors['bg_primary'],
            fg=self.theme.colors['text_primary'],
            insertbackground=self.theme.colors['accent_cyan'],
            relief='flat',
            borderwidth=0
        )
        entry.pack(fill='x', ipady=10, ipadx=12)
        
        # Add hover effects
        def on_enter(e):
            entry_border.config(bg=self.theme.colors['accent_cyan'])
        
        def on_leave(e):
            entry_border.config(bg=self.theme.colors['accent_blue'])
        
        entry.bind('<Enter>', on_enter)
        entry.bind('<Leave>', on_leave)
    
    def create_results_panel(self):
        """Create the results display panel"""
        right_panel = tk.Frame(self.main_frame, bg=self.theme.colors['bg_primary'])
        right_panel.pack(side='left', fill='both', expand=True)
        
        # Stats cards container
        self.stats_container = tk.Frame(
            right_panel, bg=self.theme.colors['bg_primary'],
            height=100
        )
        self.stats_container.pack(fill='x', pady=(0, 15))
        self.stats_container.pack_propagate(False)
        
        # Scorecard container
        scorecard_card = create_card_frame(right_panel, self.theme)
        scorecard_card.pack(fill='both', expand=True)
        
        # Scorecard header
        sc_header = create_section_header(scorecard_card, "📊 SCORECARD", self.theme)
        sc_header.pack(pady=(15, 10), padx=20, anchor='w')
        
        # Create scorecard table
        self.create_scorecard_table(scorecard_card)
    
    def create_scorecard_table(self, parent):
        """Create the scorecard display table"""
        table_container = tk.Frame(parent, bg=self.theme.colors['bg_card'])
        table_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create canvas for scrolling
        self.scorecard_canvas = tk.Canvas(
            table_container, bg=self.theme.colors['bg_card'],
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            table_container, orient='vertical',
            command=self.scorecard_canvas.yview
        )
        
        self.scrollable_frame = tk.Frame(self.scorecard_canvas, bg=self.theme.colors['bg_card'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.scorecard_canvas.configure(scrollregion=self.scorecard_canvas.bbox("all"))
        )
        
        self.canvas_window = self.scorecard_canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        self.scorecard_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.scorecard_canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind canvas width
        self.scorecard_canvas.bind(
            '<Configure>',
            lambda e: self.scorecard_canvas.itemconfig(self.canvas_window, width=e.width)
        )
        
        # Create header
        self.create_table_header()
    
    def create_table_header(self):
        """Create the scorecard table header"""
        # Clear any existing header
        if hasattr(self, 'header_row') and self.header_row:
            self.header_row.destroy()
        
        self.header_row = tk.Frame(
            self.scrollable_frame,
            bg=self.theme.colors['bg_secondary'],
            height=40
        )
        self.header_row.pack(fill='x', pady=(0, 2))
        self.header_row.pack_propagate(False)
        
        # Define column widths (proportions that add up to 1.0)
        self.column_weights = {
            'hole': 0.10,    # 10%
            'yds': 0.12,     # 12%
            'par': 0.10,     # 10%
            'hcp': 0.10,     # 10%
            'str': 0.10,     # 10%
            'gross': 0.24,   # 24%
            'net': 0.24      # 24%
        }
        
        headers = ['HOLE', 'YDS', 'PAR', 'HCP', 'STR', 'GROSS', 'NET']
        weights = list(self.column_weights.values())
        
        for header_text, weight in zip(headers, weights):
            header = tk.Label(
                self.header_row, text=header_text,
                font=('Arial', 9, 'bold'),
                bg=self.theme.colors['bg_secondary'],
                fg=self.theme.colors['text_muted'],
                anchor='center'
            )
            header.place(relx=sum(weights[:headers.index(header_text)]), 
                        rely=0, 
                        relwidth=weight, 
                        relheight=1.0)
    
    def load_selected_course(self, event):
        """Load and display course information"""
        course_name = self.course_var.get()
        course_data = self.course_manager.get_course(course_name)
        
        if course_data:
            total_yardage = sum(course_data.get('yardages', [0]*18))
            
            # Update info display
            for widget in self.info_display.winfo_children():
                widget.destroy()
            
            info_frame = tk.Frame(self.info_display, bg=self.theme.colors['bg_secondary'])
            info_frame.pack(fill='both', expand=True, padx=15, pady=12)
            
            details = [
                ('TEE', course_data['tee_name']),
                ('RATING', str(course_data['course_rating'])),
                ('SLOPE', str(course_data['slope_rating'])),
                ('PAR', str(sum(course_data['par_values']))),
                ('YARDS', str(total_yardage))
            ]
            
            for label, value in details:
                row = tk.Frame(info_frame, bg=self.theme.colors['bg_secondary'])
                row.pack(fill='x', pady=3)
                
                tk.Label(
                    row, text=label + ':',
                    font=('Arial', 9, 'bold'),
                    bg=self.theme.colors['bg_secondary'],
                    fg=self.theme.colors['text_muted'],
                    width=8, anchor='w'
                ).pack(side='left')
                
                tk.Label(
                    row, text=value,
                    font=('Arial', 10, 'bold'),
                    bg=self.theme.colors['bg_secondary'],
                    fg=self.theme.colors['accent_cyan']
                ).pack(side='left')
    
    def generate_round(self):
        """Generate a ghost golf round"""
        try:
            course_name = self.course_var.get()
            if not course_name:
                messagebox.showerror("Error", "Please select a course")
                return
            
            course_data = self.course_manager.get_course(course_name)
            if not course_data:
                messagebox.showerror("Error", "Course data not found")
                return
            
            ghin = float(self.ghin_var.get())
            
            # Create ghost golfer and generate round
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
            
            create_stat_card(
                self.stats_container, 'GROSS SCORE',
                f"{total_gross} ({total_gross - total_par:+d})",
                self.theme.colors['accent_cyan'], self.theme
            )
            create_stat_card(
                self.stats_container, 'NET SCORE',
                f"{total_net} ({total_net - total_par:+d})",
                self.theme.colors['accent_green'], self.theme
            )
            create_stat_card(
                self.stats_container, 'COURSE HCP',
                ghost.course_handicap,
                self.theme.colors['text_primary'], self.theme
            )
            
            # Clear existing scorecard
            for row in self.scorecard_rows:
                row.destroy()
            self.scorecard_rows = []
            
            # Recreate header (only once)
            self.create_table_header()
            
            # Display scores
            yardages = course_data.get('yardages', [0]*18)
            
            # Track totals
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
                
                # Get score color
                score_color = self.theme.get_score_color(gross, par)
                
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
                                         self.theme.colors['accent_blue'], True)
            
            # Add back 9 and total
            self.create_score_row('IN', back_nine['yards'], back_nine['par'],
                                 '', '', back_nine['gross'], back_nine['net'],
                                 self.theme.colors['accent_blue'], True)
            
            self.create_score_row('TOT', total_yardage, total_par, '',
                                 total_strokes, total_gross, total_net,
                                 self.theme.colors['accent_green'], True)
        
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid GHIN value: {e}")
    
    def create_score_row(self, hole, yardage, par, hcp, strokes, gross, net,
                        color, is_total):
        """Create a score row in the table"""
        bg_color = self.theme.colors['bg_secondary'] if is_total else self.theme.colors['bg_card']
        row = tk.Frame(self.scrollable_frame, bg=bg_color, height=35)
        row.pack(fill='x', pady=1)
        row.pack_propagate(False)
        
        self.scorecard_rows.append(row)
        
        font_style = ('Arial', 10, 'bold') if is_total else ('Arial', 10)
        
        # Prepare values - use empty string for missing data
        values = [
            str(hole),
            str(yardage) if yardage else '',
            str(par) if par else '',
            str(hcp) if hcp else '',
            str(strokes) if strokes else '',
            str(gross),
            str(net)
        ]
        
        weights = list(self.column_weights.values())
        
        for i, value in enumerate(values):
            # Determine color
            fg_color = self.theme.colors['text_primary']
            if i >= 5 and not is_total:  # GROSS and NET columns for regular holes
                fg_color = color
            elif is_total and i >= 5:  # GROSS and NET for totals
                fg_color = color
            
            label = tk.Label(
                row, text=value,
                font=font_style,
                bg=bg_color,
                fg=fg_color,
                anchor='center'
            )
            label.place(relx=sum(weights[:i]), 
                       rely=0, 
                       relwidth=weights[i], 
                       relheight=1.0)
    
    def refresh_course_list(self):
        """Refresh the course dropdown list"""
        self.course_dropdown['values'] = self.course_manager.get_all_courses()