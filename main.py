"""
Golf Ghost Analytics - Main Application
"""
import tkinter as tk
from tkinter import ttk, messagebox

from ghost_golfer import GhostGolfer
from course_manager import CourseManager
from ui_theme import DarkAnalyticsTheme
from ui_components import (
    create_header,
    create_stat_card,
    create_button,
    create_input_field,
    create_tab_button
)
from generate_tab import GenerateTab
from manage_tab import ManageTab


class GolfGhostApp:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Golf Ghost Analytics")
        self.root.geometry("1100x750")
        
        # Initialize theme and course manager
        self.theme = DarkAnalyticsTheme()
        self.course_manager = CourseManager()
        
        # Apply theme
        self.root.configure(bg=self.theme.colors['bg_primary'])
        self.theme.setup_styles(self.root)
        
        # Create header
        create_header(self.root, self.theme)
        
        # Main container
        self.tab_container = tk.Frame(self.root, bg=self.theme.colors['bg_primary'])
        self.tab_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create tab buttons
        self.create_tab_bar()
        
        # Content area
        self.content_frame = tk.Frame(self.tab_container, bg=self.theme.colors['bg_primary'])
        self.content_frame.pack(fill='both', expand=True)
        
        # Initialize tabs
        self.generate_tab = None
        self.manage_tab = None
        self.current_tab = None
        
        # Show generate tab by default
        self.show_generate_tab()
    
    def create_tab_bar(self):
        """Create tab navigation bar"""
        tab_bar = tk.Frame(self.tab_container, bg=self.theme.colors['bg_primary'], height=50)
        tab_bar.pack(fill='x', pady=(10, 20))
        
        self.tab_buttons = {}
        
        # Generate Round tab
        self.tab_buttons['generate'] = create_tab_button(
            tab_bar, "⚡ GENERATE ROUND", self.show_generate_tab,
            self.theme, is_active=True
        )
        self.tab_buttons['generate'].pack(side='left', padx=(0, 10))
        
        # Manage Courses tab
        self.tab_buttons['manage'] = create_tab_button(
            tab_bar, "⚙️ MANAGE COURSES", self.show_manage_tab,
            self.theme, is_active=False
        )
        self.tab_buttons['manage'].pack(side='left')
    
    def update_tab_buttons(self, active_tab):
        """Update tab button styles to show active tab"""
        for tab_name, button in self.tab_buttons.items():
            if tab_name == active_tab:
                button.config(
                    bg=self.theme.colors['accent_blue'],
                    fg='white'
                )
            else:
                button.config(
                    bg=self.theme.colors['bg_secondary'],
                    fg=self.theme.colors['text_secondary']
                )
    
    def show_generate_tab(self):
        """Display the generate round tab"""
        self.clear_content()
        self.update_tab_buttons('generate')
        self.generate_tab = GenerateTab(
            self.content_frame, 
            self.theme, 
            self.course_manager
        )
        self.current_tab = 'generate'
    
    def show_manage_tab(self):
        """Display the manage courses tab"""
        self.clear_content()
        self.update_tab_buttons('manage')
        self.manage_tab = ManageTab(
            self.content_frame,
            self.theme,
            self.course_manager,
            self.on_course_updated
        )
        self.current_tab = 'manage'
    
    def on_course_updated(self):
        """Callback when courses are updated in manage tab"""
        if self.generate_tab:
            self.generate_tab.refresh_course_list()
    
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = GolfGhostApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
