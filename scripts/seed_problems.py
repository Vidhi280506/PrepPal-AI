import json
import os
import sys

# Ensure the root project directory is in the Python path to allow absolute imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from database.connection import SessionLocal
from models.db_models import Problem

def seed_problems():
    dataset_path = os.path.join(project_root, 'datasets', 'problems.json')
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        return

    # 3. Read datasets/problems.json
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            problems_data = json.load(f)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in problems.json")
        return

    # 1. Use SessionLocal from database.connection
    session = SessionLocal()
    
    inserted_count = 0
    skipped_count = 0

    try:
        # 5. Skip duplicate problems using the title field
        # Load existing titles into a set for O(1) lookup
        existing_titles = {title[0] for title in session.query(Problem.title).all()}

        for item in problems_data:
            title = item.get('title')
            
            if not title:
                continue  # Skip entries missing a title

            if title in existing_titles:
                skipped_count += 1
            else:
                # 4. Insert every problem into the Problem table
                problem_data = item.copy()
                # Remove the id so SQLite auto-generates it
                problem_data.pop("id", None)
                new_problem = Problem(**problem_data)
                
                session.add(new_problem)
                
                # Add to set to prevent duplicates if the JSON itself contains duplicate titles
                existing_titles.add(title)
                inserted_count += 1

        # 7. Commit only once after all inserts
        session.commit()
        
        # 6. Print results exactly as requested
        print(f"Inserted {inserted_count} problems.")
        print(f"Skipped {skipped_count} duplicates.")

    except Exception as e:
        # 8. Roll back on exception
        session.rollback()
        print(f"Database error during seeding: {e}")
        print("Transaction rolled back. No changes were saved.")
        
    finally:
        # 9. Close the database session properly
        session.close()

if __name__ == "__main__":
    seed_problems()