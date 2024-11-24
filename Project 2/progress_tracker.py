#progress_tracker.py

class ProgressTracker:
    def __init__(self, plan_name, start_date, completion_date=None, current_status="Not Started", progress_percentage=0):
        """Initialize progress tracker"""
        self.plan_name = plan_name
        self.start_date = start_date
        self.completion_date = completion_date
        self.current_status = current_status
        self.progress_percentage = progress_percentage
    
    def update_progress(self, percentage):
        """Update the business plan's progress"""
        self.progress_percentage = percentage
        if self.progress_percentage >= 100:
            self.current_status = "Completed"
            
    def update_status(self, status):
        """Update the plan's status"""
        self.current_status = status
    
    def __str__(self):
        """Return the progress"""
        return f"{self.plan_name}: {self.current_status} - {self.progress_percentage}% completed"