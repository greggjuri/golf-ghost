"""
Manage Tab - UI for managing golf courses
"""
import tkinter as tk
from tkinter import messagebox

from ui_components import (
    create_button,
    create_card_frame,
    create_section_header
)


class ManageTab:
    """Tab for managing golf course data"""
    
    def __init__(self, parent, theme, course_manager, on_update_callback):
        self.parent = parent
        self.theme = theme
        self.course_manager = course_manager
        self.on_update_callback = on_update_callback
        
        self.main_frame = tk.Frame(parent, bg=theme.colors['bg_primary'])
        self.main_frame.pack(fill='both', expand=True)
        
        # Variables
        self.new_course_name = tk.StringVar()
        self.tee_name = tk.StringVar(value="Blue")
        self.course_rating = tk.StringVar(value="72.3")
        self.slope_rating = tk.StringVar(value="130")
        self.hole_inputs = []
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create the manage tab UI"""
        # Left panel - Course list
        left_panel = tk.Frame(self.main_frame, bg=self.theme.colors['bg_primary'], width=300)
        left_panel.pack(side='left', fill='both', padx=(0, 15))
        left_panel.pack_propagate(False)
        
        list_card = create_card_frame(left_panel, self.theme)
        list_card.pack(fill='both', expand=True, padx=5, pady=5)
        
        list_header = create_section_header(list_card, "💾 SAVED COURSES", self.theme)
        list_header.pack(pady=(20, 15), padx=20, anchor='w')
        
        # Listbox
        self.courses_listbox = tk.Listbox(
            list_card,
            font=('Arial', 10),
            bg=self.theme.colors['bg_secondary'],
            fg=self.theme.colors['text_primary'],
            selectbackground=self.theme.colors['accent_blue'],
            selectforeground='white',
            relief='flat',
            borderwidth=0,
            highlightthickness=0
        )
        self.courses_listbox.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        self.courses_listbox.bind('<<ListboxSelect>>', self.load_course_to_edit)
        self.update_courses_list()
        
        # Right panel - Course editor
        self.create_editor_panel()
    
    def create_editor_panel(self):
        """Create the course editor panel"""
        right_panel = tk.Frame(self.main_frame, bg=self.theme.colors['bg_primary'])
        right_panel.pack(side='left', fill='both', expand=True)
        
        editor_card = create_card_frame(right_panel, self.theme)
        editor_card.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollable editor content
        canvas = tk.Canvas(editor_card, bg=self.theme.colors['bg_card'],
                          highlightthickness=0)
        scrollbar = tk.Scrollbar(editor_card, orient='vertical',
                                command=canvas.yview)
        
        editor_frame = tk.Frame(canvas, bg=self.theme.colors['bg_card'])
        
        editor_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=editor_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Editor header
        editor_header = create_section_header(editor_frame, "✏️ COURSE EDITOR", self.theme)
        editor_header.pack(pady=(20, 20), padx=30, anchor='w')
        
        # Course info fields
        self.create_simple_field(editor_frame, "COURSE NAME", self.new_course_name)
        self.create_simple_field(editor_frame, "TEE NAME", self.tee_name)
        self.create_simple_field(editor_frame, "COURSE RATING", self.course_rating)
        self.create_simple_field(editor_frame, "SLOPE RATING", self.slope_rating)
        
        # Divider
        divider = tk.Frame(editor_frame, bg=self.theme.colors['border'], height=2)
        divider.pack(fill='x', padx=30, pady=20)
        
        # Hole-by-hole section
        holes_header = tk.Label(
            editor_frame, text="🏌️ HOLE DETAILS",
            font=('Arial', 11, 'bold'),
            bg=self.theme.colors['bg_card'],
            fg=self.theme.colors['text_primary']
        )
        holes_header.pack(pady=(0, 15), padx=30, anchor='w')
        
        # Create 18 hole inputs
        for hole_num in range(1, 19):
            self.create_hole_input_group(editor_frame, hole_num)
            
            # Divider after hole 9
            if hole_num == 9:
                nine_divider = tk.Frame(editor_frame, bg=self.theme.colors['border'], height=1)
                nine_divider.pack(fill='x', padx=30, pady=15)
        
        # Buttons
        self.create_button_panel(editor_frame)
    
    def create_simple_field(self, parent, label_text, var):
        """Create a simple input field"""
        container = tk.Frame(parent, bg=self.theme.colors['bg_card'])
        container.pack(fill='x', padx=30, pady=(0, 15))
        
        label = tk.Label(
            container, text=label_text,
            font=('Arial', 9, 'bold'),
            bg=self.theme.colors['bg_card'],
            fg=self.theme.colors['text_muted']
        )
        label.pack(anchor='w', pady=(0, 5))
        
        # Create frame for border effect
        entry_border = tk.Frame(container, bg=self.theme.colors['border'], padx=1, pady=1)
        entry_border.pack(fill='x')
        
        entry = tk.Entry(
            entry_border, textvariable=var,
            font=('Arial', 11),
            bg=self.theme.colors['bg_primary'],
            fg=self.theme.colors['text_primary'],
            insertbackground=self.theme.colors['accent_cyan'],
            relief='flat',
            borderwidth=0
        )
        entry.pack(fill='x', ipady=8, ipadx=12)
        
        # Add hover effects
        def on_enter(e):
            entry_border.config(bg=self.theme.colors['accent_blue'])
        
        def on_leave(e):
            entry_border.config(bg=self.theme.colors['border'])
        
        def on_focus_in(e):
            entry_border.config(bg=self.theme.colors['accent_cyan'])
        
        def on_focus_out(e):
            entry_border.config(bg=self.theme.colors['border'])
        
        entry.bind('<Enter>', on_enter)
        entry.bind('<Leave>', on_leave)
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry
    
    def create_hole_input_group(self, parent, hole_num):
        """Create input fields for a single hole"""
        # Container
        hole_container = tk.Frame(
            parent,
            bg=self.theme.colors['bg_secondary'],
            highlightbackground=self.theme.colors['border'],
            highlightthickness=1
        )
        hole_container.pack(fill='x', padx=30, pady=(0, 8))
        
        # Header
        header_frame = tk.Frame(hole_container, bg=self.theme.colors['bg_secondary'])
        header_frame.pack(fill='x', padx=12, pady=(8, 8))
        
        hole_label = tk.Label(
            header_frame, text=f"HOLE {hole_num}",
            font=('Arial', 9, 'bold'),
            bg=self.theme.colors['bg_secondary'],
            fg=self.theme.colors['accent_cyan']
        )
        hole_label.pack(side='left')
        
        # Input fields
        fields_frame = tk.Frame(hole_container, bg=self.theme.colors['bg_secondary'])
        fields_frame.pack(fill='x', padx=12, pady=(0, 10))
        
        # Par input
        par_var = tk.StringVar(value="4")
        self.create_hole_field(fields_frame, "Par", par_var, 5)
        
        # Yardage input
        yardage_var = tk.StringVar(value="400")
        self.create_hole_field(fields_frame, "Yardage", yardage_var, 8)
        
        # Handicap input
        hcp_var = tk.StringVar(value=str(hole_num))
        self.create_hole_field(fields_frame, "HCP", hcp_var, 5, is_last=True)
        
        # Store references
        self.hole_inputs.append({
            'par': par_var,
            'yardage': yardage_var,
            'handicap': hcp_var
        })
    
    def create_hole_field(self, parent, label_text, var, width, is_last=False):
        """Create a single hole input field"""
        field_frame = tk.Frame(parent, bg=self.theme.colors['bg_secondary'])
        field_frame.pack(side='left', fill='x', expand=True, padx=(0, 0 if is_last else 8))
        
        label = tk.Label(
            field_frame, text=label_text,
            font=('Arial', 8),
            bg=self.theme.colors['bg_secondary'],
            fg=self.theme.colors['text_muted']
        )
        label.pack(anchor='w', pady=(0, 3))
        
        # Create border frame
        entry_border = tk.Frame(field_frame, bg=self.theme.colors['border'], padx=1, pady=1)
        entry_border.pack(fill='x')
        
        entry = tk.Entry(
            entry_border, textvariable=var,
            font=('Arial', 10, 'bold'),
            bg=self.theme.colors['bg_card'],
            fg=self.theme.colors['text_primary'],
            insertbackground=self.theme.colors['accent_cyan'],
            relief='flat',
            borderwidth=0,
            width=width,
            justify='center'
        )
        entry.pack(fill='x', ipady=6)
        
        # Add hover and focus effects
        def on_enter(e):
            entry_border.config(bg=self.theme.colors['accent_blue'])
        
        def on_leave(e):
            if entry != entry.focus_get():
                entry_border.config(bg=self.theme.colors['border'])
        
        def on_focus_in(e):
            entry_border.config(bg=self.theme.colors['accent_cyan'])
        
        def on_focus_out(e):
            entry_border.config(bg=self.theme.colors['border'])
        
        entry.bind('<Enter>', on_enter)
        entry.bind('<Leave>', on_leave)
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
    
    def create_button_panel(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg=self.theme.colors['bg_card'])
        button_frame.pack(fill='x', padx=30, pady=(30, 30))
        
        save_btn = create_button(button_frame, "💾 SAVE COURSE", self.save_course,
                                 self.theme, 'primary')
        save_btn.pack(side='left', padx=(0, 10))
        
        delete_btn = create_button(button_frame, "🗑️ DELETE", self.delete_course,
                                   self.theme, 'danger')
        delete_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = create_button(button_frame, "CLEAR", self.clear_fields,
                                  self.theme, 'secondary')
        clear_btn.pack(side='left')
    
    def save_course(self):
        """Save the current course"""
        try:
            course_name = self.new_course_name.get().strip()
            if not course_name:
                messagebox.showerror("Error", "Please enter a course name")
                return
            
            # Collect hole data
            par_list = []
            yardage_list = []
            hcp_list = []
            
            for i, hole_data in enumerate(self.hole_inputs):
                try:
                    par = int(hole_data['par'].get())
                    yardage = int(hole_data['yardage'].get())
                    hcp = int(hole_data['handicap'].get())
                    
                    par_list.append(par)
                    yardage_list.append(yardage)
                    hcp_list.append(hcp)
                except ValueError:
                    messagebox.showerror("Error", f"Invalid value in Hole {i+1}")
                    return
            
            course_data = {
                'tee_name': self.tee_name.get(),
                'course_rating': float(self.course_rating.get()),
                'slope_rating': int(self.slope_rating.get()),
                'par_values': par_list,
                'hole_handicaps': hcp_list,
                'yardages': yardage_list
            }
            
            # Validate
            is_valid, error_msg = self.course_manager.validate_course_data(course_data)
            if not is_valid:
                messagebox.showerror("Error", error_msg)
                return
            
            # Save
            if self.course_manager.add_course(course_name, course_data):
                self.update_courses_list()
                self.on_update_callback()
                messagebox.showinfo("Success", f"✓ Course '{course_name}' saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save course")
        
        except ValueError as e:
            messagebox.showerror("Error", f"Please check your input values: {e}")
    
    def delete_course(self):
        """Delete the selected course"""
        course_name = self.new_course_name.get().strip()
        if course_name in self.course_manager.courses:
            if messagebox.askyesno("Confirm Delete",
                                  f"Delete course '{course_name}'?"):
                if self.course_manager.delete_course(course_name):
                    self.update_courses_list()
                    self.on_update_callback()
                    self.clear_fields()
                    messagebox.showinfo("Success", "Course deleted")
                else:
                    messagebox.showerror("Error", "Failed to delete course")
        else:
            messagebox.showerror("Error", "Course not found")
    
    def clear_fields(self):
        """Clear all input fields"""
        self.new_course_name.set("")
        self.tee_name.set("Blue")
        self.course_rating.set("72.3")
        self.slope_rating.set("130")
        
        # Clear hole inputs
        default_pars = [4, 4, 3, 5, 4, 4, 3, 4, 5, 4, 5, 4, 3, 4, 4, 3, 5, 4]
        default_yards = [395, 405, 185, 520, 380, 410, 165, 390, 535, 400, 545, 385, 175, 395, 420, 190, 510, 410]
        
        for i, hole_data in enumerate(self.hole_inputs):
            hole_data['par'].set(str(default_pars[i]))
            hole_data['yardage'].set(str(default_yards[i]))
            hole_data['handicap'].set(str(i + 1))
    
    def update_courses_list(self):
        """Update the courses listbox"""
        self.courses_listbox.delete(0, tk.END)
        for course_name in sorted(self.course_manager.get_all_courses()):
            self.courses_listbox.insert(tk.END, f"  {course_name}")
    
    def load_course_to_edit(self, event):
        """Load selected course for editing"""
        selection = self.courses_listbox.curselection()
        if selection:
            course_name = self.courses_listbox.get(selection[0]).strip()
            course_data = self.course_manager.get_course(course_name)
            
            if course_data:
                self.new_course_name.set(course_name)
                self.tee_name.set(course_data['tee_name'])
                self.course_rating.set(str(course_data['course_rating']))
                self.slope_rating.set(str(course_data['slope_rating']))
                
                # Load hole data
                for i, hole_data in enumerate(self.hole_inputs):
                    hole_data['par'].set(str(course_data['par_values'][i]))
                    hole_data['handicap'].set(str(course_data['hole_handicaps'][i]))
                    
                    if 'yardages' in course_data:
                        hole_data['yardage'].set(str(course_data['yardages'][i]))
                    else:
                        hole_data['yardage'].set("400")
