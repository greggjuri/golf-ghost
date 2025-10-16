"""
UI Theme - Color scheme and styling for the application
"""
from tkinter import ttk


class DarkAnalyticsTheme:
    """Sports Analytics Dashboard theme colors and styles"""
    
    def __init__(self):
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
    
    def setup_styles(self, root):
        """
        Setup ttk styles for the application
        
        Args:
            root: Tkinter root window
        """
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure base colors
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
        
        # Configure combobox dropdown
        root.option_add('*TCombobox*Listbox.background', self.colors['bg_secondary'])
        root.option_add('*TCombobox*Listbox.foreground', self.colors['text_primary'])
        root.option_add('*TCombobox*Listbox.selectBackground', self.colors['accent_blue'])
        root.option_add('*TCombobox*Listbox.selectForeground', 'white')
    
    def get_score_color(self, gross, par):
        """
        Get color based on score vs par
        
        Args:
            gross: Gross score
            par: Par for the hole
            
        Returns:
            Color hex code
        """
        diff = gross - par
        if diff <= -2:
            return self.colors['eagle']
        elif diff == -1:
            return self.colors['birdie']
        elif diff == 0:
            return self.colors['par']
        elif diff == 1:
            return self.colors['bogey']
        elif diff == 2:
            return self.colors['double']
        else:
            return self.colors['triple']
