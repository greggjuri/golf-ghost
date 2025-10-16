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
        self.root.title("⛳ Golf Ghost Player - Score Generator")
        self.root.geometry("950x650")
        self.root.configure(bg='#f0f4f8')
        
        self.courses_file = "golf_courses.json"
        self.courses = self.load_courses()
        
        # Configure modern style
        self.setup_styles()
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=8, pady=8)
        
        # Create tabs
        self.generate_tab = ttk.Frame(self.notebook, style='Card.TFrame')
        self.manage_tab = ttk.Frame(self.notebook, style='Card.TFrame')
        
        self.notebook.add(self.generate_tab, text='  Generate Round  ')
        self.notebook.add(self.manage_tab, text='  Manage Courses  ')
        
        self.setup_generate_tab()
        self.setup_manage_tab()
        
    def setup_styles(self):
        """Setup modern UI styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors
        bg_color = '#f0f4f8'
        card_color = '#ffffff'
        primary_color = '#2563eb'
        secondary_color = '#64748b'
        success_color = '#10b981'
        danger_color = '#ef4444'
        
        # Frame styles
        style.configure('Card.TFrame', background=card_color)
        style.configure('Header.TFrame', background=primary_color)
        
        # Label styles
        style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'), 
                       background=card_color, foreground='#1e293b')
        style.configure('Header.TLabel', font=('Segoe UI', 10, 'bold'), 
                       background=card_color, foreground='#334155')
        style.configure('Info.TLabel', font=('Segoe UI', 9), 
                       background=card_color, foreground='#64748b')
        style.configure('Value.TLabel', font=('Segoe UI', 10, 'bold'), 
                       background=card_color, foreground=primary_color)
        
        # Button styles
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'),
                       background=primary_color, foreground='white', 
                       borderwidth=0, padding=(15, 8))
        style.map('Primary.TButton',
                 background=[('active', '#1d4ed8')])
        
        style.configure('Secondary.TButton', font=('Segoe UI', 9),
                       background=secondary_color, foreground='white',
                       borderwidth=0, padding=(12, 6))
        
        # Entry and Combobox
        style.configure('Custom.TEntry', fieldbackground='white', 
                       borderwidth=1, relief='solid')
        style.configure('TCombobox', fieldbackground='white')
        
        # Notebook
        style.configure('Custom.TNotebook', background=bg_color, borderwidth=0)
        style.configure('Custom.TNotebook.Tab', font=('Segoe UI', 10),
                       padding=[15, 8])
        
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
    
    def setup_generate_tab(self):
        """Setup the Generate Round tab"""
        main_frame = ttk.Frame(self.generate_tab, style='Card.TFrame', padding="12")
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_frame = ttk.Frame(main_frame, style='Card.TFrame')
        title_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(title_frame, text="⛳ Generate Ghost Round", 
                 style='Title.TLabel').pack(side='left')
        
        # Input Section
        input_frame = ttk.LabelFrame(main_frame, text=" Course & Player Setup ", 
                                     padding="10", style='Card.TFrame')
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Course Selection
        course_frame = ttk.Frame(input_frame, style='Card.TFrame')
        course_frame.pack(fill='x', pady=5)
        ttk.Label(course_frame, text="Select Course:", 
                 style='Header.TLabel').pack(side='left', padx=(0, 10))
        self.course_var = tk.StringVar()
        self.course_dropdown = ttk.Combobox(course_frame, textvariable=self.course_var, 
                                           width=45, state='readonly', font=('Segoe UI', 10))
        self.course_dropdown['values'] = list(self.courses.keys())
        self.course_dropdown.pack(side='left', fill='x', expand=True)
        self.course_dropdown.bind('<<ComboboxSelected>>', self.load_selected_course)
        
        # GHIN Input
        ghin_frame = ttk.Frame(input_frame, style='Card.TFrame')
        ghin_frame.pack(fill='x', pady=5)
        ttk.Label(ghin_frame, text="Ghost GHIN Index:", 
                 style='Header.TLabel').pack(side='left', padx=(0, 10))
        self.ghin_var = tk.StringVar(value="15.0")
        ghin_entry = ttk.Entry(ghin_frame, textvariable=self.ghin_var, 
                              width=15, font=('Segoe UI', 11))
        ghin_entry.pack(side='left')
        
        # Course Info Display
        self.info_frame = ttk.Frame(input_frame, style='Card.TFrame')
        self.info_frame.pack(fill='x', pady=(10, 5))
        
        self.course_info_text = ttk.Label(self.info_frame, 
                                         text="← Select a course to begin", 
                                         style='Info.TLabel', font=('Segoe UI', 10, 'italic'))
        self.course_info_text.pack()
        
        # Generate Button
        btn_frame = ttk.Frame(main_frame, style='Card.TFrame')
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="🎯 Generate Round", command=self.generate_round,
                  style='Primary.TButton').pack()
        
        # Results Display with Treeview
        results_frame = ttk.LabelFrame(main_frame, text=" Scorecard ", 
                                      padding="10", style='Card.TFrame')
        results_frame.pack(fill='both', expand=True)
        
        # Summary labels
        self.summary_frame = ttk.Frame(results_frame, style='Card.TFrame')
        self.summary_frame.pack(fill='x', pady=(0, 10))
        
        # Scorecard table
        self.setup_scorecard_table(results_frame)
        
    def setup_scorecard_table(self, parent):
        """Create the scorecard table"""
        # Create frame for table and scrollbar
        table_frame = ttk.Frame(parent, style='Card.TFrame')
        table_frame.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview for scorecard
        columns = ('hole', 'yardage', 'par', 'hcp', 'strokes', 'gross', 'net')
        self.scorecard_tree = ttk.Treeview(table_frame, columns=columns, 
                                          show='headings', height=20,
                                          yscrollcommand=scrollbar.set)
        
        # Column headers
        self.scorecard_tree.heading('hole', text='Hole')
        self.scorecard_tree.heading('yardage', text='Yards')
        self.scorecard_tree.heading('par', text='Par')
        self.scorecard_tree.heading('hcp', text='HCP')
        self.scorecard_tree.heading('strokes', text='Strokes')
        self.scorecard_tree.heading('gross', text='Gross')
        self.scorecard_tree.heading('net', text='Net')
        
        # Column widths
        self.scorecard_tree.column('hole', width=60, anchor='center')
        self.scorecard_tree.column('yardage', width=70, anchor='center')
        self.scorecard_tree.column('par', width=60, anchor='center')
        self.scorecard_tree.column('hcp', width=60, anchor='center')
        self.scorecard_tree.column('strokes', width=75, anchor='center')
        self.scorecard_tree.column('gross', width=75, anchor='center')
        self.scorecard_tree.column('net', width=75, anchor='center')
        
        # Configure tags for coloring (score-based)
        self.scorecard_tree.tag_configure('eagle', background='#86efac', foreground='#065f46')
        self.scorecard_tree.tag_configure('birdie', background='#bef264', foreground='#365314')
        self.scorecard_tree.tag_configure('par', background='#ffffff', foreground='#000000')
        self.scorecard_tree.tag_configure('bogey', background='#fde68a', foreground='#713f12')
        self.scorecard_tree.tag_configure('double', background='#fed7aa', foreground='#7c2d12')
        self.scorecard_tree.tag_configure('triple', background='#fca5a5', foreground='#7f1d1d')
        self.scorecard_tree.tag_configure('total', background='#dbeafe', foreground='#1e40af',
                                         font=('Segoe UI', 10, 'bold'))
        
        self.scorecard_tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.scorecard_tree.yview)
        
    def setup_manage_tab(self):
        """Setup the Manage Courses tab"""
        main_frame = ttk.Frame(self.manage_tab, style='Card.TFrame', padding="12")
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        ttk.Label(main_frame, text="🏌️ Manage Golf Courses", 
                 style='Title.TLabel').pack(anchor='w', pady=(0, 10))
        
        # Input Section
        input_frame = ttk.LabelFrame(main_frame, text=" Course Details ", 
                                    padding="10", style='Card.TFrame')
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Create grid for inputs
        # Course Name
        ttk.Label(input_frame, text="Course Name:", style='Header.TLabel').grid(
            row=0, column=0, sticky='w', pady=5, padx=(0, 10))
        self.new_course_name = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.new_course_name, 
                 width=40, font=('Segoe UI', 10)).grid(row=0, column=1, columnspan=2, 
                                                        sticky='ew', pady=5)
        
        # Tee Name
        ttk.Label(input_frame, text="Tee Name:", style='Header.TLabel').grid(
            row=1, column=0, sticky='w', pady=5, padx=(0, 10))
        self.tee_name = tk.StringVar(value="Blue")
        ttk.Entry(input_frame, textvariable=self.tee_name, 
                 width=20, font=('Segoe UI', 10)).grid(row=1, column=1, sticky='w', pady=5)
        
        # Course Rating
        ttk.Label(input_frame, text="Course Rating:", style='Header.TLabel').grid(
            row=2, column=0, sticky='w', pady=5, padx=(0, 10))
        self.course_rating = tk.StringVar(value="72.3")
        ttk.Entry(input_frame, textvariable=self.course_rating, 
                 width=15, font=('Segoe UI', 10)).grid(row=2, column=1, sticky='w', pady=5)
        
        # Slope Rating
        ttk.Label(input_frame, text="Slope Rating:", style='Header.TLabel').grid(
            row=3, column=0, sticky='w', pady=5, padx=(0, 10))
        self.slope_rating = tk.StringVar(value="130")
        ttk.Entry(input_frame, textvariable=self.slope_rating, 
                 width=15, font=('Segoe UI', 10)).grid(row=3, column=1, sticky='w', pady=5)
        
        # Par Values
        ttk.Label(input_frame, text="Par Values (18):", style='Header.TLabel').grid(
            row=4, column=0, sticky='w', pady=5, padx=(0, 10))
        ttk.Label(input_frame, text="e.g., 4,4,3,5,4,4,3,4,5,4,5,4,3,4,4,3,5,4", 
                 style='Info.TLabel', font=('Segoe UI', 8)).grid(
            row=4, column=1, columnspan=2, sticky='w')
        self.par_values = tk.StringVar(value="4,4,3,5,4,4,3,4,5,4,5,4,3,4,4,3,5,4")
        ttk.Entry(input_frame, textvariable=self.par_values, 
                 width=50, font=('Segoe UI', 10)).grid(row=5, column=0, columnspan=3, 
                                                        sticky='ew', pady=(0, 5))
        
        # Hole Handicaps
        ttk.Label(input_frame, text="Hole Handicaps:", style='Header.TLabel').grid(
            row=6, column=0, sticky='w', pady=5, padx=(0, 10))
        ttk.Label(input_frame, text="e.g., 7,5,15,1,11,9,17,13,3,8,2,10,16,6,12,18,4,14", 
                 style='Info.TLabel', font=('Segoe UI', 8)).grid(
            row=6, column=1, columnspan=2, sticky='w')
        self.hole_handicaps = tk.StringVar(value="7,5,15,1,11,9,17,13,3,8,2,10,16,6,12,18,4,14")
        ttk.Entry(input_frame, textvariable=self.hole_handicaps, 
                 width=50, font=('Segoe UI', 10)).grid(row=7, column=0, columnspan=3, 
                                                        sticky='ew', pady=(0, 5))
        
        # Yardages
        ttk.Label(input_frame, text="Yardages (18):", style='Header.TLabel').grid(
            row=8, column=0, sticky='w', pady=5, padx=(0, 10))
        ttk.Label(input_frame, text="e.g., 395,405,185,520,380,410,165,390,535,400,545,385,175,395,420,190,510,410", 
                 style='Info.TLabel', font=('Segoe UI', 8)).grid(
            row=8, column=1, columnspan=2, sticky='w')
        self.yardages = tk.StringVar(value="395,405,185,520,380,410,165,390,535,400,545,385,175,395,420,190,510,410")
        ttk.Entry(input_frame, textvariable=self.yardages, 
                 width=50, font=('Segoe UI', 10)).grid(row=9, column=0, columnspan=3, 
                                                        sticky='ew', pady=(0, 5))
        
        input_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(main_frame, style='Card.TFrame')
        button_frame.pack(fill='x', pady=10)
        ttk.Button(button_frame, text="💾 Save Course", 
                  command=self.save_course, style='Primary.TButton').pack(
            side='left', padx=5)
        ttk.Button(button_frame, text="🗑️ Delete", 
                  command=self.delete_course, style='Secondary.TButton').pack(
            side='left', padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_fields, style='Secondary.TButton').pack(
            side='left', padx=5)
        
        # Saved Courses List
        list_frame = ttk.LabelFrame(main_frame, text=" Saved Courses ", 
                                   padding="10", style='Card.TFrame')
        list_frame.pack(fill='both', expand=True)
        
        self.courses_listbox = tk.Listbox(list_frame, height=10, 
                                          font=('Segoe UI', 10),
                                          bg='white', selectbackground='#2563eb',
                                          selectforeground='white', 
                                          borderwidth=0, highlightthickness=1,
                                          highlightcolor='#cbd5e1')
        self.courses_listbox.pack(fill='both', expand=True)
        self.courses_listbox.bind('<<ListboxSelect>>', self.load_course_to_edit)
        
        self.update_courses_list()
        
    def save_course(self):
        """Save a new course or update existing"""
        try:
            course_name = self.new_course_name.get().strip()
            if not course_name:
                messagebox.showerror("Error", "Please enter a course name")
                return
            
            par_list = [int(x.strip()) for x in self.par_values.get().split(',')]
            hcp_list = [int(x.strip()) for x in self.hole_handicaps.get().split(',')]
            yardage_list = [int(x.strip()) for x in self.yardages.get().split(',')]
            
            if len(par_list) != 18 or len(hcp_list) != 18 or len(yardage_list) != 18:
                messagebox.showerror("Error", "Must have exactly 18 par values, 18 hole handicaps, and 18 yardages")
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
            self.course_dropdown['values'] = list(self.courses.keys())
            
            messagebox.showinfo("Success", f"✓ Course '{course_name}' saved successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please check your input values.")
    
    def delete_course(self):
        """Delete selected course"""
        course_name = self.new_course_name.get().strip()
        if course_name in self.courses:
            if messagebox.askyesno("Confirm Delete", 
                                  f"Delete course '{course_name}'?"):
                del self.courses[course_name]
                self.save_courses()
                self.update_courses_list()
                self.course_dropdown['values'] = list(self.courses.keys())
                self.clear_fields()
                messagebox.showinfo("Success", "Course deleted")
        else:
            messagebox.showerror("Error", "Course not found")
    
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
            self.courses_listbox.insert(tk.END, course_name)
    
    def load_course_to_edit(self, event):
        """Load selected course data for editing"""
        selection = self.courses_listbox.curselection()
        if selection:
            course_name = self.courses_listbox.get(selection[0])
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
    
    def load_selected_course(self, event):
        """Load course info when selected in dropdown"""
        course_name = self.course_var.get()
        if course_name in self.courses:
            course_data = self.courses[course_name]
            total_yardage = sum(course_data.get('yardages', [0]*18))
            info_text = (f"🏌️ {course_data['tee_name']} Tees  |  "
                        f"Rating: {course_data['course_rating']}  |  "
                        f"Slope: {course_data['slope_rating']}  |  "
                        f"Par: {sum(course_data['par_values'])}  |  "
                        f"Yardage: {total_yardage}")
            self.course_info_text.config(text=info_text, 
                                        font=('Segoe UI', 10, 'normal'))
    
    def generate_round(self):
        """Generate a round for the ghost player"""
        try:
            course_name = self.course_var.get()
            if not course_name or course_name not in self.courses:
                messagebox.showerror("Error", "Please select a course")
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
            
            # Clear existing items
            for item in self.scorecard_tree.get_children():
                self.scorecard_tree.delete(item)
            
            # Populate table
            front_par = 0
            front_gross = 0
            front_net = 0
            front_yardage = 0
            back_par = 0
            back_gross = 0
            back_net = 0
            back_yardage = 0
            total_strokes = 0
            
            # Get yardages, use default if not present (backward compatibility)
            yardages = course_data.get('yardages', [0]*18)
            
            for score in scores:
                hole_num = score['hole']
                par = score['par']
                gross = score['gross_score']
                net = score['net_score']
                strokes = score['strokes_received']
                hcp = course_data['hole_handicaps'][hole_num - 1]
                yardage = yardages[hole_num - 1]
                
                # Determine score vs par for coloring
                diff = gross - par
                if diff <= -2:
                    tag = 'eagle'
                elif diff == -1:
                    tag = 'birdie'
                elif diff == 0:
                    tag = 'par'
                elif diff == 1:
                    tag = 'bogey'
                elif diff == 2:
                    tag = 'double'
                else:
                    tag = 'triple'
                
                # Track front/back 9 totals
                if hole_num <= 9:
                    front_par += par
                    front_gross += gross
                    front_net += net
                    front_yardage += yardage
                else:
                    back_par += par
                    back_gross += gross
                    back_net += net
                    back_yardage += yardage
                
                total_strokes += strokes
                
                self.scorecard_tree.insert('', 'end', values=(
                    hole_num, yardage, par, hcp, strokes, gross, net
                ), tags=(tag,))
                
                # Add subtotal after hole 9
                if hole_num == 9:
                    self.scorecard_tree.insert('', 'end', values=(
                        'OUT', front_yardage, front_par, '', '', front_gross, front_net
                    ), tags=('total',))
            
            # Add back 9 total
            self.scorecard_tree.insert('', 'end', values=(
                'IN', back_yardage, back_par, '', '', back_gross, back_net
            ), tags=('total',))
            
            # Add final total
            total_par = front_par + back_par
            total_gross = front_gross + back_gross
            total_net = front_net + back_net
            total_yardage = front_yardage + back_yardage
            
            self.scorecard_tree.insert('', 'end', values=(
                'TOTAL', total_yardage, total_par, '', total_strokes, total_gross, total_net
            ), tags=('total',))
            
            # Update summary
            for widget in self.summary_frame.winfo_children():
                widget.destroy()
            
            summary_text = f"📊 {course_name} ({course_data['tee_name']}) - {total_yardage} yards  |  "
            summary_text += f"GHIN: {ghin} → Course Handicap: {ghost.course_handicap}  |  "
            summary_text += f"Gross: {total_gross} ({total_gross - total_par:+d})  |  "
            summary_text += f"Net: {total_net} ({total_net - total_par:+d})"
            
            ttk.Label(self.summary_frame, text=summary_text, 
                     font=('Segoe UI', 10, 'bold'), foreground='#2563eb',
                     background='#ffffff').pack()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid GHIN handicap")


if __name__ == "__main__":
    root = tk.Tk()
    app = GolfGhostApp(root)
    root.mainloop()
