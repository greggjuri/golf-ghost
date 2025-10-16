"""
Ghost Golfer - Score generation logic
"""
import random


class GhostGolfer:
    """Generates realistic golf scores for a ghost player based on handicap"""
    
    def __init__(self, handicap_index, course_rating, slope_rating, par_values, hole_handicaps):
        """
        Initialize a ghost golfer
        
        Args:
            handicap_index: Player's GHIN handicap index
            course_rating: Course rating from the tees
            slope_rating: Course slope rating
            par_values: List of 18 par values
            hole_handicaps: List of 18 handicap indexes (1-18)
        """
        self.handicap_index = handicap_index
        self.course_rating = course_rating
        self.slope_rating = slope_rating
        self.par_values = par_values
        self.hole_handicaps = hole_handicaps
        self.course_handicap = round((handicap_index * slope_rating) / 113)
        
    def generate_round(self):
        """
        Generate a realistic round of golf scores
        
        Returns:
            List of dictionaries containing hole-by-hole scores
        """
        scores = []
        expected_strokes_over = self.course_handicap
        strokes_per_hole = expected_strokes_over / 18.0
        round_adjustment = random.gauss(0, 1.2)
        
        for i, (par, hole_hcp) in enumerate(zip(self.par_values, self.hole_handicaps)):
            # Calculate strokes received based on course handicap
            strokes_received = 1 if hole_hcp <= self.course_handicap else 0
            if self.course_handicap > 18:
                extra_strokes = self.course_handicap - 18
                if hole_hcp <= extra_strokes:
                    strokes_received = 2
            
            # Generate score with some randomness
            base_score = par + strokes_per_hole
            hole_randomness = random.gauss(0, 1.1)
            
            # Adjust difficulty based on hole handicap
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
