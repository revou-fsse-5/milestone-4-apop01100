from flask import request
from app.services.seeds_service import SeedsService

def seeds_controller():
    if request.method == "GET":
        response = SeedsService.show_data()
        
        return response
    
    if request.method == "POST":
        response = SeedsService.generate_all_data()
        
        return response
    
    if request.method == "DELETE":
        response = SeedsService.clear_data()
        
        return response