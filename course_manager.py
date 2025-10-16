"""
Course Manager - Handles course data persistence
"""
import json
import os


class CourseManager:
    """Manages golf course data storage and retrieval"""
    
    def __init__(self, filename="golf_courses.json"):
        """
        Initialize course manager
        
        Args:
            filename: JSON file to store course data
        """
        self.filename = filename
        self.courses = self.load_courses()
    
    def load_courses(self):
        """
        Load courses from JSON file
        
        Returns:
            Dictionary of course data
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading courses: {e}")
                return {}
        return {}
    
    def save_courses(self):
        """Save courses to JSON file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.courses, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving courses: {e}")
            return False
    
    def add_course(self, course_name, course_data):
        """
        Add or update a course
        
        Args:
            course_name: Name of the course
            course_data: Dictionary containing course information
        """
        self.courses[course_name] = course_data
        return self.save_courses()
    
    def delete_course(self, course_name):
        """
        Delete a course
        
        Args:
            course_name: Name of the course to delete
        """
        if course_name in self.courses:
            del self.courses[course_name]
            return self.save_courses()
        return False
    
    def get_course(self, course_name):
        """
        Get course data
        
        Args:
            course_name: Name of the course
            
        Returns:
            Course data dictionary or None
        """
        return self.courses.get(course_name)
    
    def get_all_courses(self):
        """
        Get all course names
        
        Returns:
            List of course names
        """
        return list(self.courses.keys())
    
    def validate_course_data(self, course_data):
        """
        Validate course data structure
        
        Args:
            course_data: Dictionary to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ['tee_name', 'course_rating', 'slope_rating', 
                          'par_values', 'hole_handicaps', 'yardages']
        
        for field in required_fields:
            if field not in course_data:
                return False, f"Missing required field: {field}"
        
        # Validate list lengths
        if len(course_data['par_values']) != 18:
            return False, "Must have exactly 18 par values"
        
        if len(course_data['hole_handicaps']) != 18:
            return False, "Must have exactly 18 hole handicaps"
        
        if len(course_data['yardages']) != 18:
            return False, "Must have exactly 18 yardages"
        
        return True, None
